#!/usr/bin/env bash
set -e

LAB_NUMBER="—"
LAB_TITLE="Разработка прикладных решений на Python с применением методов машинного обучения на данных рынка недвижимости Москвы"
SUBJECT="Разработка прикладных решений на Python"
GROUP="ИТИм-25"
STUDENT="Скиндер И.П."
TEACHER="доц. Харитонов Ю.Е."
CITY="Донецк"
YEAR="2026"

REPORT="term-paper/report.md"
CONTENT_TMP="term-paper/_content_tmp.docx"
OUTPUT="term-paper/Курсовая.docx"
REFERENCE="templates/reference.docx"

echo "[1/2] Converting report.md to content.docx via Pandoc..."

docker compose -f docker-compose.docs.yml run --rm docs \
  "$REPORT" \
  -o "$CONTENT_TMP" \
  --reference-doc="$REFERENCE" \
  --resource-path="term-paper"

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
