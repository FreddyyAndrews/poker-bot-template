# Shortcuts for the improvement loop (see CLAUDE.md). Run ./setup.sh first.
.PHONY: setup match brief test snapshot compare mock connect-mock connect check clean

ARENA  := .venv/bin/arena
HANDS  ?= 300
FIELD  := $(foreach o,tight aggressive station chaos,--field opponents/$(o).py)
LATEST  = $(shell ls -d versions/mybot-v* 2>/dev/null | sort -V | tail -1)

setup:
	./setup.sh

match:                        ## mybot vs every opponent, recorded in runs/
	$(ARENA) match run mybot/bot.py opponents/*.py --hands $(HANDS) --reset-stacks

brief:                        ## result, leaks and costliest hands
	$(ARENA) brief mybot

test:                         ## spots with expected answers (basics + your own)
	$(ARENA) test mybot/bot.py --suite basics
	@if ls spots/suites/mine/*.yaml >/dev/null 2>&1; then $(ARENA) test mybot/bot.py --suite mine; fi

snapshot:                     ## copy mybot/ to versions/mybot-vN before changing it
	@n=$$(ls -d versions/mybot-v* 2>/dev/null | sed 's/.*-v//' | sort -n | tail -1); \
	 n=$$(( $${n:-0} + 1 )); cp -r mybot versions/mybot-v$$n; \
	 rm -rf versions/mybot-v$$n/__pycache__; echo "saved versions/mybot-v$$n"

compare:                      ## is mybot better than the latest snapshot? (duplicate deals)
	@if [ -z "$(LATEST)" ]; then echo "no snapshot yet: run make snapshot first"; exit 2; fi
	$(ARENA) compare mybot/bot.py $(LATEST)/bot.py $(FIELD) --hands $(HANDS)

mock:                         ## a local arena (bot mybot, token dev-token)
	$(ARENA) serve-mock

connect-mock:                 ## play one match on the local arena (run make mock first)
	$(ARENA) connect --config config.mock.yml --max-matches 1

connect:                      ## play on the real arena (needs config.yml and a token)
	$(ARENA) connect

check:                        ## test the token in config.yml
	$(ARENA) connect --check

clean:                        ## delete recorded runs and stepped hands
	rm -rf runs .arena
