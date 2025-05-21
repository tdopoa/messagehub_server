#!/bin/sh
set -e

exec uvicorn \
  --factory "${UVI_APP:-src.main:create_app}" \
  --host "${UVI_HOST:-0.0.0.0}" \
  --port "${UVI_PORT:-8000}" \
  --workers "${UVI_WORKERS:-2}" \
  --limit-max-requests "${UVI_LIMIT_MAX_REQUESTS:-10000}" \
  --timeout-keep-alive "${UVI_TIMEOUT_KEEP_ALIVE:-600}" \
  --env-file "${UVI_ENV_FILE:-.env}"