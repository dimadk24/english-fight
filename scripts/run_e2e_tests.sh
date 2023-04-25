#!/usr/bin/env bash

FRONTEND_URL="http://localhost:3000/english-fight"

# Clean up screenshots to ensure to remove not used screenshots
yarn --cwd frontend rimraf ../backend/tests/e2e/screenshots

yarn --cwd=frontend start:e2e &
# wait till frontend compiles up to 3 min, with delay 10s (as it takes time) and interval 1s
yarn --cwd=frontend wait-on "$FRONTEND_URL" --delay 10000 --timeout 180000 --interval 1000 &&
  (cd backend && IS_E2E_TESTS=1 poetry run pytest tests/e2e)
#  braces to don't change current shell directory
#  See https://stackoverflow.com/a/786419/7119080
