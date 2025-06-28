#!/bin/sh

set -e

uv run ruff check &&
uv run pyright &&
uv run pytest -vv
