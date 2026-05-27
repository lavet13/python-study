#!/usr/bin/env bash
#
# Builds lab-**/Отчет.docx from lab-**/report.md and templates/lab-template.docx
#
# Run from the PROJECT ROOT (not from inside lab-01/):
#   bash lab-01/build.sh
#
# What happens:
#   Step 1 — Pandoc converts report.md → content.docx (content only, no title page)
#   Step 2 — merge.py fills lab-template.docx with this lab's variables
#             and appends the content, producing the final Отчет.docx
#   Step 3 — Temporary content.docx is deleted

set -e  # exit immediately if any command fails

# == Lab-specific variables ====================================================
# Change these for each lab

LAB_NUMBER="1"
LAB_TITLE="Разработка базы данных. Основы работы в MySQL"
SUBJECT="Инжиниринг и управление данными"
GROUP="ИТИм-25"
STUDENT="Скиндер И.П."
TEACHER="доц. Романюк В.В."
CITY="Донецк"
YEAR="2026"

# == Paths (relative to project root) =========================================

REPORT="lab-01/report.md"
CONTENT_TMP="lab-01/_content_tmp.docx"   # intermediate file, deleted at end
OUTPUT="lab-01/Отчет.docx"
REFERENCE="templates/reference.docx"

# == Step 1: Pandoc — markdown to docx ========================================

echo "[1/2] Converting report.md to content.docx via Pandoc..."

docker compose -f docker-compose.docs.yml run --rm docs \
  "$REPORT" \
  -o "$CONTENT_TMP" \
  --reference-doc="$REFERENCE" \
  --resource-path="lab-01"

# == Step 2: Merge title page with content ====================================

echo "[2/2] Merging title page with content..."

docker compose -f docker-compose.docs.yml run --rm \
  --entrypoint python3 docs \
  templates/merge.py \
  --lab     "$LAB_NUMBER" \
  --title   "$LAB_TITLE" \
  --subject "$SUBJECT" \
  --group   "$GROUP" \
  --student "$STUDENT" \
  --teacher "$TEACHER" \
  --city    "$CITY" \
  --year    "$YEAR" \
  --content "$CONTENT_TMP" \
  --output  "$OUTPUT"

# == Step 3: Cleanup ===========================================================

rm -f "$CONTENT_TMP"

echo "Done: $OUTPUT"

