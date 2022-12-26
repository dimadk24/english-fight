#!/usr/bin/env bash
# Usage: cd to project root and run ./scripts/bandit.sh
bandit -r -c ".bandit.yaml" .
