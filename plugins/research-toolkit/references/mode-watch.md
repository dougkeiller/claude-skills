# Watch — Monitors

Moved out of SKILL.md so it loads only when this mode runs. `$S` is the script path set in SKILL.md.

**Before creating a scheduled monitor, state the recurring cost and wait for
a go-ahead** — this is the one place in the toolkit where money recurs without
a session open: about USD 0.015 a run, roughly USD 0.45 a month at daily
(list price read 2026-10-06; assume each run bills). Omit `--period` for a
manual-only monitor that costs nothing until triggered. The script's default
webhook is a no-op URL on the user's own domain; Exa rejects `example.com`,
localhost and private hosts.

```bash
python3 "$S" monitor-create "what to watch for, described richly" \
  --name <slug> --num 15 --period 1d --describe "one line per new development, naming who and what"
python3 "$S" monitor-list
python3 "$S" monitor-run <id>       # trigger now, poll, print what is new
python3 "$S" monitor-delete <id>
```

Each run deduplicates against previous runs, so it surfaces only what is new;
a run that returns nothing is a real answer — "nothing new since <date>",
never an empty section. The API requires a
webhook URL even though runs are readable over the API; the script's placeholder
is a public host where deliveries fail harmlessly. Whether Exa disables a
monitor whose deliveries keep failing is unverified — if a scheduled monitor
goes quiet, check that first. For a digest that runs without a session open,
a Cowork scheduled task can call `monitor-run` and write the note.

