# poker-bot-template

Fork this repo, drop a coding agent in it, and get a No-Limit Hold'em bot
that you can develop locally and run on the poker arena. The
[lichess-bot](https://github.com/lichess-bot-devs/lichess-bot) of poker.

**Status:** planning. The layout and workflow below are the target; the
files arrive with milestone 1 (see [Plan](#plan)).

---

## The idea

- **Develop locally with full god view.** Your bot plays matches against
  dummy bots, and you see everything: every player's cards, every
  decision, your bot's notes. You can probe it in any situation, run test
  suites with expected answers, and compare versions with duplicate deals
  and confidence intervals. All of this comes from the
  [Poker-Harness](https://github.com/FreddyyAndrews/Poker-Harness)
  toolkit, installed as a dependency.
- **Play in production from anywhere.** Register your bot on the arena
  website, create a token, and run the bridge (`arena connect`) on any
  machine. It connects to the arena, accepts challenges or joins tables,
  and answers each decision by running your `bot.py`. Your bot can use any
  model, tool or hardware you like.
- **Watch it play** on the arena website, look through your own match
  history (your cards plus showdowns), or play against it yourself.

## Target layout

```
bot/bot.py             your bot: decide(state, ctx) -> action
opponents/             dummy bots to practise against (copy, edit, add more)
spots/                 situations and test suites with expected answers
config.yml.default     bridge settings: server, token, challenges, matchmaking
CLAUDE.md              instructions for the coding agent working on the bot
NOTES.md               the agent's lab notebook, kept across sessions
setup.sh               one-command setup (works in a fresh cloud session)
Makefile               make setup | test | match | compare | brief | connect
```

## Target workflow

```bash
./setup.sh                                  # install the toolkit and dependencies
arena match run bot/bot.py opponents/*.py   # local matches, everything recorded
arena brief bot                             # result, leaks, costliest hands
arena probe bot/bot.py --from MATCH:HAND    # what does it do here, and why?
arena test bot/bot.py --suite basics        # expected answers; exit 1 on failure
arena compare bot/bot.py bot-prev/bot.py    # did the change help? (duplicate deals)
cp config.yml.default config.yml            # add your token
arena connect                               # play on the arena
```

---

## Plan

**P1. Skeleton**
- `bot/bot.py`: a reasonable starter bot that uses `ctx.log` to explain
  its decisions.
- `opponents/`: a few varied dummy bots (tight, loose-aggressive, calling
  station, random).
- `spots/`: the toolkit's basics suite plus an empty suite for the bot's
  own tests.
- `.gitignore` covering `runs/`, `.arena/`, `config.yml` and `.env`, so
  tokens and run logs are never committed.

**P2. One-command setup**
- `setup.sh` / `make setup`: install Python and the toolkit (pinned) in a
  fresh environment. Verified in a fresh Claude cloud session.
- Depends on how the toolkit's hand-evaluator install question is
  resolved (eval7 needs Python 3.10 and a special build).

**P3. Agent instructions**
- `CLAUDE.md`: the goal, the rules (what the bot receives, legal actions,
  time limits), the improvement loop (brief, investigate, probe, change,
  test, compare), how to keep `NOTES.md`, and how to connect to the arena.
  Refined by dropping fresh agents into the template and watching where
  they struggle.
- `NOTES.md`: a structured lab notebook the agent maintains: hypotheses,
  experiments, results, what to try next. It carries context between
  sessions, which is part of what the arena studies.

**P4. Bridge config**
- `config.yml.default`, modelled on lichess-bot's: server URL, token,
  bot entry point, concurrency, which challenges to accept (formats, time
  controls, opponents), and optional matchmaking (challenge online bots,
  join seeks for table formats).
- Tested against the toolkit's mock server first, then the real arena.

**P5. Optional CI**
- A GitHub Action that runs `arena test` on every push, so a bot that
  breaks its test suite is caught before it's connected.

### Milestones (shared with the other repos)

1. **Protocol and local loop:** P1-P3, plus P4 against the toolkit's mock
   server.
2. **Arena alpha:** P4 against a local arena instance.
3. **Public beta:** the template is made public and linked from the arena
   website.
