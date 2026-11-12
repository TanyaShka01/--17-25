#!/usr/bin/env bash
# Запуск утилиты depvis: ./run.sh [путь_к_конфигу]
set -euo pipefail

CONFIG="${1:-config.ini}"
export PYTHONPATH="${PYTHONPATH:-}:$(cd "$(dirname "$0")" && pwd)/src"

python3 -m depvis.cli --config "$CONFIG"
