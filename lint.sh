#!/usr/bin/env bash

set -eu
set -o pipefail


cd "$(dirname "$0")" || exit 1

FILES=(
  bot.py
  )

mypy --ignore-missing-imports -- "${FILES[@]}"
