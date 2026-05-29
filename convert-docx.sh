#!/usr/bin/env bash

set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <input.docx> [output.txt]"
  echo "Example: $0 SII_python_Colab_praktika.docx"
  exit 1
fi

INPUT_DOCX=$1

# Optional: second argument for output file, otherwise auto-generate
if [ $# -ge 2 ]; then
    OUTPUT_TXT="$2"
else
    OUTPUT_TXT="${INPUT_DOCX%.docx}.txt"
fi

# Check if input file exists
if [[ ! -f "$INPUT_DOCX" ]]; then
  echo "Error: File '$INPUT_DOCX' not found!"
  exit 1
fi

cd ~/workspace/python-study
source .venv/bin/activate

echo "Converting: $INPUT_DOCX → $OUTPUT_TXT"

python3 -c '
from docx import Document
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

doc = Document(input_file)
with open(output_file, "w", encoding="utf-8") as f:
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            f.write(text + "\n")

print(f"Done! Saved to {output_file}")
' "$INPUT_DOCX" "$OUTPUT_TXT"
