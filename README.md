# poker-bot-template

Start here to build a No-Limit Hold'em bot for the poker arena: use this
template (or fork it), drop a coding agent in it, and let it improve the
bot with full god-view tools locally, then run it on the arena from
anywhere. The [lichess-bot](https://github.com/lichess-bot-devs/lichess-bot)
of poker.

## Quick start

```bash
# "Use this template" on GitHub, then clone your copy, and:
./setup.sh                   # installs the toolkit into .venv and checks the bot
source .venv/bin/activate
make match                   # mybot vs the dummy opponents
make brief                   # what to improve
```

Then open the repo in Claude Code (or a Claude cloud session) and give the
agent a goal, for example *"improve mybot; follow CLAUDE.md"*. CLAUDE.md
tells it the loop: find a leak, study it, turn it into a test, change the
bot, prove the change with a duplicate-deal comparison, and keep notes in
NOTES.md for the next session.

Requirements: Python 3.10+ (3.12 recommended). Linux x86_64 works up to
Python 3.15; macOS and Windows up to 3.12. Nothing to compile.

## What's here

| Path | What it is |
|---|---|
| `mybot/bot.py` | the bot: `decide(state, ctx)` returns an action. A simple starter strategy to improve |
| `opponents/` | dummy bots to practise against: `tight`, `aggressive`, `station` (calling station), `chaos` (random). Add more |
| `spots/suites/basics/` | sanity tests with expected answers (don't fold the nuts, ...) |
| `spots/suites/mine/` | the bot's own tests, added as leaks are found |
| `versions/` | snapshots of earlier versions, to compare against |
| `CLAUDE.md` | instructions for the coding agent |
| `NOTES.md` | the agent's lab notebook, kept between sessions |
| `config.yml.default` | settings for playing on the arena |
| `config.mock.yml` | settings for rehearsing against a local arena |
| `setup.sh`, `Makefile` | setup and shortcuts |

Everything else comes from the
[Poker-Harness](https://github.com/FreddyyAndrews/Poker-Harness) toolkit,
installed by `setup.sh`: `arena guide` explains it.

## Make targets

| Command | What it does |
|---|---|
| `make match` | mybot against every opponent (stacks reset each hand); recorded in `runs/` (`HANDS=300`) |
| `make brief` | the result, the biggest leaks and the costliest hands |
| `make test` | the basics suite plus your own spots |
| `make snapshot` | save `mybot/` as `versions/mybot-vN` before changing it |
| `make compare` | mybot vs the latest snapshot, duplicate deals with a confidence interval |
| `make mock` / `make connect-mock` | rehearse on a local arena |
| `make check` / `make connect` | play on the real arena |

## Playing on the arena

1. Register the bot on the arena website and create a token for it.
2. `cp config.yml.default config.yml`, set `url`, and either put the
   token in `config.yml` or `export ARENA_TOKEN=...`. Both `config.yml`
   and `.env` are gitignored.
3. `make check` tests the token; `make connect` plays until Ctrl-C (once
   finishes current matches, twice leaves them).

Your bot runs on your machine and can use any model, tool or hardware.
The arena only sends it its own view of each match. Every arena match is
recorded in `runs/arena/` and can be analysed with the same tools
(`arena match hand arena/<id>:N`, `arena brief mybot`).

To rehearse first: `make mock` in one terminal (a local arena with house
bots), then `make connect-mock` in another.

## Keeping the toolkit current

`setup.sh` installs the Poker-Harness version pinned at the top of the
script (`HARNESS_VERSION`). To upgrade, change it and run `./setup.sh`
again, or run `HARNESS_VERSION=vX.Y.Z ./setup.sh` with a newer release.
