#!/bin/sh
# Use the installed local environment without uv replacing the wxPython binary.
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
export LD_LIBRARY_PATH="$ROOT/.venv/pyfa-compat/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec "$ROOT/.venv/bin/python" "$ROOT/pyfa.py" "$@"
