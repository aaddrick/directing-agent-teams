# Communication

How agents find each other, and why content travels in files rather than in messages.

## The Roster is the only directory

Background subagents have no `ListAgents`, at any depth. They do have `SendMessage`, and messaging works by agent ID across the whole session: siblings, parent and child, and across branches. So BOARD → Roster is the only way any agent below the main session can find another.

- **Whoever spawns an agent writes its ID into the Roster at once,** with its role and "spawned by". The main session writes the Director's row right after spawning it.
- **Write a verifier's row before its builder needs it.** In one run, builders couldn't reach verifiers whose rows weren't written yet.
- **Message by ID, never by description.** Descriptions don't resolve, and a send by name is refused if the name now points to a newer agent.

## Who talks to whom

- **Status goes up one level:** workers to their lead, leads to the Director, the Director to the main session. Never straight to the main session from below.
- **The main session talks to the Director** and, for your requirement changes, directly to every affected lead as well.
- **Pointers, not payloads.** Content goes in files (`qa/…`, `notes/…`, `handoff/…`); messages carry paths and one-line verdicts.

## When a message arrives

A message is delivered at the receiver's **next tool round**. An agent inside a long blocking call doesn't see anything until the call returns. That's one reason long jobs and lock waits run in the background (see [resources-and-locks.md](resources-and-locks.md)).

## The delivery rule

From [`rules.md`](../../skills/directing-agent-teams/rules.md):

1. If `SendMessage` fails, or there's no reply by the time you need one, check the Roster. The role may have handed off. Resend to the current ID.
2. If the role is handing off or empty, append the message under `Inbox → <role>` on BOARD, marked `(undelivered)`, and tell the level above. Only the role's owner clears its Inbox.
3. Check the Roster before messaging a role after a long gap.
4. **Never message a handed-off agent's old ID.** Messaging a finished agent resumes it with its full old context. If that happens anyway, the resumed agent files the message in its old role's Inbox, tells the level above, and stops.

## Misrouted replies

Nested replies and completion notices sometimes land at the root session instead of the parent (open Claude Code bugs #83599, #90463, #90256). The main session expects this: it forwards each one by ID to the right agent and doesn't act on it.

Completion notices aren't reliable in another way too: in an interactive session, a parent's completion is held until its background children finish. So nobody waits on a notice. Results land in files and in BOARD status, and everyone reads those.

## Decisions

Every user decision and every call the Director makes is a D-number in BOARD → Decisions, with your exact words or the Director's reason. Later agents read the decision instead of reopening it.

Two rules keep decisions from getting lost on the way down:

- **A change goes to the Director and every affected lead,** and the Director confirms in one line. In the AR run, a flight-path change sent to only one place was missed by a storyboard already in progress.
- **Follow-ups get their own confirmation.** If you add to a change after it was relayed, and the confirmation doesn't mention the addition, the main session asks again.

## Time

Timestamps come from `date`, never from an agent's estimate. In the mech run, agents guessed times, and BOARD timestamps and ETAs ended up hours off.
