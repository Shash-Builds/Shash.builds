# Power: Operator

For big jobs that span days or chats: projects, agent teams, handovers, repo housekeeping.

## Builds on
**agent-team**, **economy-mode** (memory sheet and helpers), **careful-mode**.

## Method
1. Plan in a progress file in the project (goal, rounds, what is done, what is next). Update it as you go,
   so any new chat can pick up where the last one stopped.
2. Run the fan-out: 2 to 4 helpers on even slices, steer them with new rules mid-run instead of restarting,
   merge and check their work yourself.
3. Heavy projects get a resume kit: a setup script that installs the tools, a prepare script that rebuilds
   the working files that are not in git, and a short skill or README that says where everything is.
4. Save every decision to memory the moment it is made.
5. Before deleting or moving anything: back it up in full (every branch and its history), test the
   restore, and tell the user what is safe to delete. Prefer archiving.
6. Push after every block of work.

## Done when
The progress file and memory are current, the work is pushed, and the user knows the next step.
