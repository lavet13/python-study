#!/usr/bin/env bash
#
# Generates codebase.md — a single AI-friendly file containing the entire
# project codebase, suitable for attaching to an LLM alongside the lab prompt.
#
# Run from the PROJECT ROOT:
#   bash build-codebase.sh
#
# Output: codebase.md (at project root)
#
# What gets excluded:
#   *.md files — report.md, README.md, guides (LLM should not copy these)
#   .git/       — repomix respects .gitignore automatically
#   node_modules/ — same

set -e

OUTPUT="codebase.md"
HEADER="This file contains the entire mysql-study project codebase packed into a single file by repomix. Use it as context when generating lab reports and init.sql files."

echo "Generating $OUTPUT..."

docker compose -f docker-compose.docs.yml run --rm repomix \
  --style markdown \
  --ignore "*.md" \
  --output "$OUTPUT" \
  --parsable-style \
  --header-text "$HEADER"

echo "Done: $OUTPUT"
