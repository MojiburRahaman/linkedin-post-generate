#!/usr/bin/env sh
set -e

if [ "$#" -eq 0 ]; then
  exec tail -f /dev/null
fi

if [ "${WATCH_MODE}" = "true" ]; then
  exec python /app/watch_entrypoint.py "$@"
else
  exec python -m src.cli "$@"
fi


