#!/usr/bin/env bash

cd ~/workspace/python-study
source .venv/bin/activate

python3 -c "
from docx import Document
doc = Document('SII_python_Colab_praktika.docx')
with open('SII_python_Colab_praktika.txt', 'w') as f:
    for para in doc.paragraphs:
        if para.text.strip():
            f.write(para.text + '\n')
print('Done')
"
