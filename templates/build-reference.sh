#!/usr/bin/env bash

# Regenerates templates/reference.docx from templates/make_reference.js
# Run from the PROJECT ROOT:
#   bash templates/build_reference.sh
#
# When to run this:
#   Only when you change make_reference.js (font, spacing, style definitions).
#   The generated reference.docx should be committed to git.

set -e  # exit immediately on any error

echo "[1/2] Building node image..."
docker compose -f docker-compose.docs.yml build node

echo "[2/2] Generating reference.docx..."
docker compose -f docker-compose.docs.yml run --rm node make_reference.js

echo "Done: templates/reference.docx"
