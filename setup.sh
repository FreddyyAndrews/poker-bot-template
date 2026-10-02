#!/usr/bin/env bash
# One-command setup: a .venv with the Poker-Harness toolkit, then a smoke test.
# Works in a fresh Claude cloud session, on Linux x86_64 (Python 3.10+) and
# macOS (Python 3.10-3.12). Re-run any time; it's idempotent.
set -euo pipefail
cd "$(dirname "$0")"

HARNESS_VERSION="${HARNESS_VERSION:-v0.7.0}"
HARNESS_URL="https://github.com/FreddyyAndrews/Poker-Harness/archive/refs/tags/${HARNESS_VERSION}.tar.gz"

# the hand evaluator (eval7) has wheels for Python 3.10-3.12 everywhere and
# up to 3.15 on Linux x86_64, so prefer 3.12 and fall back from there
PYTHON=""
for candidate in python3.12 python3.11 python3.10 python3.13 python3.14 python3; do
  if command -v "$candidate" >/dev/null 2>&1 &&
     "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    PYTHON="$candidate"
    break
  fi
done
if [ -z "$PYTHON" ]; then
  echo "setup: needs Python 3.10 or newer (python3.12 recommended)" >&2
  exit 1
fi

echo "setup: using $($PYTHON --version) ($PYTHON)"
if [ ! -x .venv/bin/python ]; then
  "$PYTHON" -m venv .venv
fi
.venv/bin/python -m pip install --quiet --upgrade pip
echo "setup: installing poker-harness $HARNESS_VERSION"
.venv/bin/pip install --quiet "poker-harness[mock] @ $HARNESS_URL"

mkdir -p spots/suites/mine versions
echo "setup: checking the bot against the basics suite"
.venv/bin/arena test mybot/bot.py --suite basics -n 2 || {
  echo "setup: installed, but mybot fails some basics spots (see above)" >&2
}

cat <<'MSG'

setup: done. Next:
  source .venv/bin/activate
  arena guide          # how the toolkit works
  make match           # mybot vs the opponents in opponents/
  make brief           # what to work on
See CLAUDE.md for the full workflow.
MSG
