#!/usr/bin/env bash

cd ~/workspace/python-study
source .venv/bin/activate

python3 -c "
import fitz
doc = fitz.open('SII_Osnovy_Python.pdf')
with open('SII_Osnovy_Python.txt', 'w') as f:
    for page in doc:
        f.write(page.get_text())
print('Done')
"
