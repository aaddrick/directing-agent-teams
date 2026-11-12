#!/usr/bin/env bash
# run-job.sh: run one long job the way rules.md asks, so agents don't have to
# remember the traps. Linux only (reads /proc).
#
#   run-job.sh --out /abs/dir --timeout 45m [--lock /repo/.gpu.lock] [--lock-wait 1800]
#               [--role ROLE] [--agent ID] [--stall 300] [--mem-mb N] [--nice 10] -- cmd args...
#
# What it does:
#   - takes the lock (flock) if given, and writes <lock>.owner: role, agent, pgid, expiry
#   - runs the command in its own session/process group and records the real pgid in
#     <out>/pgid (never `$!` of a setsid chain)
#   - stops it at --timeout (TERM, then KILL 30 s later)
#   - with --stall N: stops it when the CPU ticks of every process in its session haven't
#     moved for N seconds (catches "finished, then hung at quit" while holding a slot)
#   - stopping covers the whole session, so children that moved to their own process
#     group (a nested `timeout`, some sandboxes) are stopped too
#   - with --mem-mb N: applies `ulimit -v` to the command. For small analysis scripts only;
#     never for the program under test or anything with thread pools.
#   - when the job ends, for any reason, stops whatever it left running in its session
#   - writes <out>/run.log (command output plus a final "DONE rc=<n> reason=<r>" line)
#     and <out>/exit (the exit code), releases the lock and clears the owner file
#   - if it is itself stopped (TERM/INT/HUP), stops the whole session first
#
# Exit codes: the command's own, or 124 timeout, 125 stall, 75 lock wait timed out,
# 64 usage error. Run it with Bash run_in_background and wait for its notification,
# or watch <out>/exit.

set -u

usage() { sed -n '2,25p' "$0" >&2; exit 64; }

out="" dur="" lock="" lock_wait=1800 role="${TEAM_ROLE:-unknown}" agent="${TEAM_AGENT:-unknown}"
stall=0 mem_mb=0 nice_n=10
while [ $# -gt 0 ]; do
  case "$1" in
    --out) out="$2"; shift 2 ;;
    --timeout) dur="$2"; shift 2 ;;
    --lock) lock="$2"; shift 2 ;;
    --lock-wait) lock_wait="$2"; shift 2 ;;
    --role) role="$2"; shift 2 ;;
    --agent) agent="$2"; shift 2 ;;
    --stall) stall="$2"; shift 2 ;;
    --mem-mb) mem_mb="$2"; shift 2 ;;
    --nice) nice_n="$2"; shift 2 ;;
    --) shift; break ;;
    -h|--help) usage ;;
    *) echo "run-job: unknown option $1" >&2; usage ;;
  esac
done
[ $# -gt 0 ] || { echo "run-job: no command after --" >&2; usage; }
[ -n "$dur" ] || { echo "run-job: --timeout is required" >&2; usage; }
case "$out" in /*) ;; *) echo "run-job: --out must be an absolute path" >&2; usage ;; esac
case "$dur" in *[!0-9.smhd]*|'') echo "run-job: --timeout looks like 90s, 45m or 2h" >&2; usage ;; esac
for n in "$lock_wait" "$stall" "$mem_mb" "$nice_n"; do
  case "$n" in ''|*[!0-9]*) echo "run-job: numeric option expected, got '$n'" >&2; usage ;; esac
done

mkdir -p "$out"
log="$out/run.log"
rm -f "$out/exit" "$out/pgid"
now() { date '+%Y-%m-%d %H:%M:%S'; }

finish() {  # finish <rc> <reason>
  echo "DONE rc=$1 reason=$2 at $(now)" >> "$log"
  echo "$1" > "$out/exit"
  if [ -n "$lock" ] && [ -f "$lock.owner" ] && grep -q " pgid ${pgid:-none} " "$lock.owner" 2>/dev/null; then
    : > "$lock.owner"
  fi
  exit "$1"
}

if [ -n "$lock" ]; then
  exec 9>"$lock"
  echo "lock wait $lock (up to ${lock_wait}s) from $(now)" >> "$log"
  if ! flock -w "$lock_wait" 9; then
    echo "lock wait timed out; holder: $(cat "$lock.owner" 2>/dev/null)" >> "$log"
    finish 75 lock
  fi
fi

# Start the command as the leader of a new session; the leader writes its own pid
# (= pgid) before exec, so nobody has to guess it.
pgid=""
ulimit_cmd=""
[ "$mem_mb" -gt 0 ] && ulimit_cmd="ulimit -v $((mem_mb * 1024));"
setsid -w bash -c "echo \$\$ > '$out/pgid'; $ulimit_cmd exec nice -n $nice_n timeout --kill-after=30 $dur \"\$@\"" run-job "$@" >> "$log" 2>&1 &
waiter=$!
for _ in $(seq 1 100); do [ -s "$out/pgid" ] && break; sleep 0.05; done
pgid=$(cat "$out/pgid" 2>/dev/null)

session_pids() {  # every process in the job's session, including children that moved
  local f line rest      # to their own process group (nested `timeout`, some sandboxes)
  for f in /proc/[0-9]*/stat; do
    read -r line < "$f" 2>/dev/null || continue
    rest=${line##*) }
    # shellcheck disable=SC2086
    set -- $rest
    [ "$4" = "$pgid" ] && echo "${f//[^0-9]/}"
  done
}

stop_group() {
  [ -n "$pgid" ] || return
  local p
  for p in $(session_pids); do kill -TERM "$p" 2>/dev/null; done
  for _ in $(seq 1 20); do [ -n "$(session_pids)" ] || return; sleep 0.5; done
  for p in $(session_pids); do kill -KILL "$p" 2>/dev/null; done
}
trap 'stop_group; finish 143 stopped' TERM INT HUP

if [ -n "$lock" ]; then
  expires=$(date -d "now + $(echo "$dur" | sed 's/s$/ seconds/; s/m$/ minutes/; s/h$/ hours/; s/d$/ days/')" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "?")
  echo "$role $agent pgid $pgid started $(now) expires $expires out $out" > "$lock.owner"
fi
echo "start pgid $pgid at $(now): $*" >> "$log"

group_ticks() {  # utime+stime+cutime+cstime of every process in the session
  local f line rest total=0
  for f in /proc/[0-9]*/stat; do
    read -r line < "$f" 2>/dev/null || continue
    rest=${line##*) }
    # shellcheck disable=SC2086
    set -- $rest
    [ "$4" = "$pgid" ] && total=$((total + ${12} + ${13} + ${14} + ${15}))
  done
  echo "$total"
}

reason="exit"
if [ "$stall" -gt 0 ] && [ -n "$pgid" ]; then
  last=-1 still=0 step=5
  while kill -0 "$waiter" 2>/dev/null; do
    sleep "$step" & wait $!
    t=$(group_ticks)
    if [ "$t" = "$last" ]; then still=$((still + step)); else still=0; last=$t; fi
    if [ "$still" -ge "$stall" ]; then
      echo "stall: no CPU ticks for ${still}s in session $pgid" >> "$log"
      reason=stall; stop_group; break
    fi
  done
fi
wait "$waiter"; rc=$?
# Nothing the job started outlives it: sweep the session (leftover pollers, children in
# their own process group that the timeout's signal didn't reach).
if [ -n "$pgid" ] && [ -n "$(session_pids)" ]; then
  echo "sweep: stopping leftover processes in session $pgid: $(session_pids | tr '\n' ' ')" >> "$log"
  stop_group
fi
[ "$reason" = stall ] && finish 125 stall
[ "$rc" = 124 ] && finish 124 timeout
finish "$rc" exit
