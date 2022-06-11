#!/usr/bin/env bash
# Usage: cd to project root and run ./scripts/export_requirements.sh
poetry export --without-hashes > requirements.txt
