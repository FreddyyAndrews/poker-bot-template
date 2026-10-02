# NOTES.md: lab notebook

The memory between sessions. Read it first; update it before you finish.
Keep it short: replace stale text instead of piling up.

## Current bot

mybot v0 (the template's starter bot):
- Preflop: a hand-strength score. Raise >= 0.75 (shove when 15bb or
  less), call >= 0.45 for up to 3bb, otherwise check/fold.
- Postflop: equity against random hands vs pot odds. Bet/raise 2/3 pot at
  70%+ equity, call when equity beats the price by 5%, else check/fold.
- Known weaknesses: assumes random opponent hands, never bluffs, one bet
  size, ignores position and match history.

## Results

| Comparison | New vs old | bb/100 (95% CI) | Verdict |
|---|---|---|---|
| (none yet) | | | |

## Log

<!-- One entry per experiment, newest first:

### YYYY-MM-DD: short title
- Hypothesis: ...
- Change: ...
- Evidence: make compare -> c-..., +X bb/100 (CI a..b); make test: pass
- Verdict: kept / reverted, because ...
-->

## Next

- Run `make match` and `make brief` to find the first leak to work on.
