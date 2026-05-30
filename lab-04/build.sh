#!/usr/bin/env bash
set -e

LAB_NUMBER="4"
LAB_TITLE="Основы машинного обучения (часть 2)"
SUBJECT="Разработка прикладных решений на Python"
GROUP="ИТИм-25"
STUDENT="Скиндер И.П."
TEACHER="доц. Харитонов Ю.Е."
CITY="Донецк"
YEAR="2026"

REPORT="lab-04/report.md"
CONTENT_TMP="lab-04/_content_tmp.docx"
OUTPUT="lab-04/Отчет.docx"
REFERENCE="templates/reference.docx"

echo "[1/2] Converting report.md to content.docx via Pandoc..."

docker compose -f docker-compose.docs.yml run --rm docs \
  "$REPORT" \
  -o "$CONTENT_TMP" \
  --reference-doc="$REFERENCE" \
  --resource-path="lab-04"

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

rm -f "$CONTENT_TMP"
echo "Done: $OUTPUT"
