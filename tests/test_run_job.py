"""run-job.sh does what rules.md promises agents it does.

Each case runs the real script against a tiny command and checks the files it
leaves behind: the exit code, the recorded process group, the lock owner file,
and that nothing it started is still running.
"""

import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "directing-agent-teams" / "tools" / "run-job.sh"
NEEDS = ("bash", "flock", "setsid", "timeout")


def group_alive(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False


@unittest.skipUnless(sys.platform.startswith("linux") and all(shutil.which(n) for n in NEEDS),
                     "run-job.sh needs Linux with bash, flock, setsid and timeout")
class TeamRunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="run-job-test-"))
        self.out = self.tmp / "out"

    def tearDown(self):
        pg = self.out / "pgid"
        if pg.exists() and pg.read_text().strip():
            try:
                os.killpg(int(pg.read_text()), signal.SIGKILL)
            except (ProcessLookupError, ValueError):
                pass
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_it(self, *args, timeout=60):
        return subprocess.run([str(SCRIPT), *args], capture_output=True, text=True, timeout=timeout)

    def result(self):
        return int((self.out / "exit").read_text()), (self.out / "run.log").read_text()

    def test_passes_the_commands_exit_code_and_output(self):
        p = self.run_it("--out", str(self.out), "--timeout", "30s", "--",
                        "bash", "-c", "echo hello; exit 3")
        self.assertEqual(p.returncode, 3)
        rc, log = self.result()
        self.assertEqual(rc, 3)
        self.assertIn("hello", log)
        self.assertIn("DONE rc=3 reason=exit", log)

    def test_records_the_real_process_group(self):
        p = self.run_it("--out", str(self.out), "--timeout", "30s", "--",
                        "bash", "-c", "ps -o pgid= -p $$")
        self.assertEqual(p.returncode, 0)
        recorded = (self.out / "pgid").read_text().strip()
        _, log = self.result()
        self.assertIn(recorded, log.split())

    def test_timeout_stops_the_whole_group(self):
        p = self.run_it("--out", str(self.out), "--timeout", "2s", "--",
                        "bash", "-c", "sleep 300 & sleep 300; wait")
        self.assertEqual(p.returncode, 124)
        self.assertIn("reason=timeout", self.result()[1])
        time.sleep(0.5)
        self.assertFalse(group_alive(int((self.out / "pgid").read_text())))

    def test_stall_watchdog_stops_a_hung_process(self):
        start = time.monotonic()
        p = self.run_it("--out", str(self.out), "--timeout", "5m", "--stall", "10", "--",
                        "sleep", "300")
        self.assertEqual(p.returncode, 125)
        self.assertLess(time.monotonic() - start, 40)
        self.assertIn("reason=stall", self.result()[1])

    def test_stall_watchdog_leaves_a_busy_process_alone(self):
        p = self.run_it("--out", str(self.out), "--timeout", "5m", "--stall", "5", "--",
                        "timeout", "12", "bash", "-c", "while :; do :; done")
        # the inner timeout ends the busy loop with 124 after 12 s; the watchdog never fired
        self.assertEqual(p.returncode, 124)
        self.assertNotIn("stall:", self.result()[1])

    def test_lock_owner_file_is_written_and_cleared(self):
        lock = self.tmp / ".gpu.lock"
        proc = subprocess.Popen([str(SCRIPT), "--out", str(self.out), "--timeout", "30s",
                                 "--lock", str(lock), "--role", "verifier", "--agent", "a1",
                                 "--", "sleep", "3"])
        owner = Path(str(lock) + ".owner")
        for _ in range(50):
            if owner.exists() and owner.read_text().strip():
                break
            time.sleep(0.1)
        line = owner.read_text()
        self.assertTrue(line.startswith("verifier a1 pgid "), line)
        self.assertIn(" expires ", line)
        self.assertEqual(proc.wait(timeout=30), 0)
        self.assertEqual(owner.read_text(), "")

    def test_lock_wait_times_out_when_held(self):
        lock = self.tmp / ".gpu.lock"
        holder = subprocess.Popen(["flock", str(lock), "sleep", "30"])
        try:
            time.sleep(0.3)
            p = self.run_it("--out", str(self.out), "--timeout", "30s", "--lock", str(lock),
                            "--lock-wait", "1", "--", "true")
            self.assertEqual(p.returncode, 75)
            self.assertIn("reason=lock", self.result()[1])
        finally:
            holder.kill()
            holder.wait()

    def test_timeout_reaches_a_child_in_its_own_process_group(self):
        # a nested `timeout` moves its child to a new process group; it must still be stopped
        p = self.run_it("--out", str(self.out), "--timeout", "2s", "--",
                        "bash", "-c", "timeout 300 sleep 300 & echo $! > " + str(self.tmp / "inner") + "; wait")
        self.assertEqual(p.returncode, 124)
        time.sleep(1)
        inner = int((self.tmp / "inner").read_text())
        alive = subprocess.run(["pgrep", "-x", "sleep", "-g", str(os.getpgid(inner))]
                               if Path(f"/proc/{inner}").exists() else ["false"])
        self.assertNotEqual(alive.returncode, 0)

    def test_stopping_the_launcher_stops_its_group(self):
        proc = subprocess.Popen([str(SCRIPT), "--out", str(self.out), "--timeout", "5m",
                                 "--", "bash", "-c", "sleep 300 & sleep 300; wait"])
        pgid_file = self.out / "pgid"
        for _ in range(50):
            if pgid_file.exists() and pgid_file.read_text().strip():
                break
            time.sleep(0.1)
        time.sleep(0.5)
        pgid = int(pgid_file.read_text())
        proc.terminate()
        self.assertEqual(proc.wait(timeout=30), 143)
        time.sleep(0.5)
        self.assertFalse(group_alive(pgid))

    def test_rejects_a_relative_output_folder(self):
        p = self.run_it("--out", "relative/out", "--timeout", "5s", "--", "true")
        self.assertEqual(p.returncode, 64)
        self.assertFalse(Path("relative").exists())


if __name__ == "__main__":
    unittest.main()
