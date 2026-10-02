# CLAUDE.md

You are developing a No-Limit Hold'em poker bot. Your job is to make
`mybot` win more, prove it with evidence, and keep a record of what you
learn so the next session can build on it.

## First, every session

1. If `.venv/` is missing, run `./setup.sh` (one command; installs the
   Poker-Harness toolkit and checks the bot). Then `source .venv/bin/activate`.
2. Read `NOTES.md`: what was tried, what worked, what to try next.
3. Run `make match` and `make brief` to see where the bot stands now.

`arena guide` explains the toolkit; `arena COMMAND -h` has options and
examples for every command.

## The bot

`mybot/bot.py` defines `decide(state, ctx)`, called once per decision.
`arena guide bot` lists every field of `state`. In short:
- Return `{"action": "fold" | "check" | "call" | "all_in"}` or
  `{"action": "raise", "amount": TOTAL}`, where TOTAL is the whole bet for
  the street, not the increase. Use `state["legal_actions"]` for the legal
  range.
- Explain decisions with `ctx.log("why", key=value, ...)`. The notes show
  up in `arena match hand` and `arena decisions`, and they're how you (and
  the next session) understand what the bot was thinking.
- Answer within the time limit: 2 seconds per decision in local matches by
  default (`--timeout`), and the arena's clock in production
  (`ctx.time_left()` says how long is left). Timeouts and crashes check or
  fold for you and restart the bot.
- Module-level variables persist for the whole match (one process per
  match), so you can track opponents across hands. `state["match_action_log"]`
  has the last 200 actions.
- Put slow setup (loading tables, models) in an optional `warmup(ctx)`,
  which runs once before the first hand.
- Anything installed in `.venv` is available, and the bot may call LLMs or
  other services. Keep within the clock, and seed any randomness from the
  deal, for example `random.Random(f"{state['hand_num']}:{state['your_cards']}")`,
  not from `hand_id` (it contains the match id). Then `make compare`, which
  replays the same deals, sees the same choices for the same cards.

## The improvement loop

```bash
make match                      # mybot vs every opponent; recorded in runs/
make brief                      # the result, the biggest leaks, the costliest hands
```

1. **Pick one leak** from the brief. Look at the evidence:
   ```bash
   arena decisions --bot mybot --action fold --equity-above 0.5 --sort pot
   arena hands --bot mybot --lost-more 2000
   arena match hand MATCH:HAND            # every card, plus mybot's notes for each decision
   ```
2. **Understand it.** Ask the bot about the exact situation:
   ```bash
   arena probe mybot/bot.py --from MATCH:HAND --at K --warm
   arena sweep mybot/bot.py --from MATCH:HAND --at K --vary bet=100..2000:100
   ```
3. **Lock it in as a test.** Save the situation and say what a good bot
   does there:
   ```bash
   arena match hand MATCH:HAND --at K --save suites/mine/short-name
   ```
   Then add an `expect:` block to `spots/suites/mine/short-name.yaml`
   (`arena test -h` shows the syntax, e.g. `expect: {not: [fold]}`).
4. **Change the bot.** Run `make snapshot` first, so the old version is
   kept in `versions/` to compare against. Change one thing at a time.
5. **Check it.**
   ```bash
   make test                       # basics + your own spots; must pass
   make compare                    # mybot vs the latest snapshot, duplicate deals
   ```
   Keep the change only if `make compare` says mybot is better, or at
   least not worse while fixing a test that matters. If it's "no
   significant difference", run more hands (`make compare HANDS=1000`)
   or drop the change.
6. **Record it** in `NOTES.md` and commit.

## Rules of evidence

- A single match's chip count is mostly card luck. Never claim an
  improvement from `make match`; use `make compare`, which replays the
  same deals with seats rotated and gives a 95% confidence interval.
- Quote the comparison id (`c-...`) in `NOTES.md` and the commit message.
- Hindsight equity (in `arena decisions` and the brief) uses cards the bot
  couldn't see. It finds mistakes; it isn't a target to optimise directly.
- `make test` must pass before you commit.

## NOTES.md

`NOTES.md` is your lab notebook, and the only memory that carries from one
session to the next. Keep it short and current:
- **Current bot:** what the strategy does now, in a few lines.
- **Results:** the latest comparisons (id, versions, bb/100, interval).
- **Log:** one entry per experiment: hypothesis, change, evidence,
  verdict (kept or reverted).
- **Next:** the most promising things to try.

Update it before you finish, even when an experiment failed. Failed
experiments are worth recording so they aren't repeated.

## Don't

- Don't edit the existing opponents to make mybot look better. Add new
  opponents to `opponents/` instead, if you need to test against a style.
- Don't commit `runs/`, `.arena/`, `config.yml`, `.env` or tokens.
- Don't make a change you can't measure. If there's no test or comparison
  for it, write one first.

## Playing on the arena

- **Rehearse locally:** `make mock` in one terminal, `make connect-mock` in
  another. That plays one match against a house bot through the real
  protocol.
- **For real:** copy `config.yml.default` to `config.yml`, set `url`, put
  the bot's token in `ARENA_TOKEN` (or in `config.yml`, which is
  gitignored), then `make check` and `make connect`.
- Arena matches are recorded from mybot's own view in `runs/arena/` and
  show up in every tool as `arena/<id>`. Opponents' unshown cards stay
  hidden (`????`), so hindsight equity there is limited to hands that
  reached showdown.

## Git

- Commit after each experiment that's kept, with what changed and the
  evidence (the comparison id and result), and update NOTES.md in the same
  commit.
- `versions/` snapshots are small; commit them, so comparisons can be
  repeated.
