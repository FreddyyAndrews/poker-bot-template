# CLAUDE.md

This repo is being built. Once it's ready, this file becomes the
instructions for the coding agent that develops the poker bot (see
README.md, P3). Until then it holds the conventions for building the
template itself.

## Git workflow

- After each body of work is complete, commit and push to `main` (no
  feature branches for now).
- Logical commits with Conventional Commits messages; the body says why.
- No Claude Code attribution in commits or PRs.

## Ground rules

- The template must stay easy to drop an agent into: one setup command,
  clear instructions, nothing that needs a human to edit config except
  adding a token.
- Never commit tokens, config.yml, .env or run logs.
- Tooling belongs in Poker-Harness (installed as a dependency), not here;
  this repo holds the bot, its opponents, its spots and its config.
