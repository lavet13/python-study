# Gemini Python Lab Workflow

## First session ever (setup)

```
# 1. Navigate to your python-study project
cd ~/workspace/python-study

# 2. Start gemini
gemini

# 3. Activate python lab mode
/python

# 4. Feed the lab task document
@SII_python_Colab_praktika.docx this is the full lab task document.
Read it and tell me how many labs there are, what each one requires,
and what order we should work through them.

# 5. Feed the dataset
@learn_dataset.csv this is the dataset we will use for all labs.
Describe its structure — columns, data types, what each column
likely represents.
```

After step 5, Gemini knows everything it needs. Start lab 1.

---

## Ending a session

At the end of every session, ask Gemini to summarize:

```
We completed lab 1 today. Summarize what we did so I can
paste it into our progress file.
```

Copy the summary into `progress.md` in the repo root.

---

## Starting subsequent sessions

```
cd ~/workspace/python-study
gemini
/python
@progress.md here is our progress so far. What's next?
```

Gemini reads the progress file and continues from where you left off.

---

## Feeding reference files when needed

```
# Python syntax reference
@SII_Osnovy_Python.pdf explain the section on [topic] from this manual

# Lab tasks (if you need to re-check requirements)
@SII_python_Colab_praktika.docx what exactly does lab 3 require?

# Current codebase state
@codebase.md review what we have so far for this lab
```

You don't need to feed these every session — only when relevant.
Gemini will ask you to feed a file if it needs it.

---

## Generating the report after each lab

```
# After finishing the code for a lab:
The lab code is complete. Now help me write report.md in Russian
academic style for Отчет. Structure: цель работы, задание,
ход выполнения, выводы. Use the output we produced as the basis.
```

Then run pandoc to generate the .docx:

```bash
# From project root — this is all you need, build.sh handles everything
bash lab-XX/build.sh
```

---

## Курсовой workflow

After all labs are done:

```
/python
@progress.md all labs are complete. Now I need to write the Курсовой.
I have a new dataset: @курсовой_dataset.csv
Help me plan the structure of the Курсовой and what analysis
to perform on this dataset.
```

---

## Progress file template (progress.md)

Create this at project root and update after each lab:

```markdown
# Progress

## Completed labs

### Lab 1 — [title]
- Date: YYYY-MM-DD
- What we did: [summary from Gemini]
- Files: lab-01/main.py, lab-01/Отчет.docx

## Current status
Working on: Lab 2
Next step: [what Gemini said to do next]

## Notes
- [anything worth remembering between sessions]
```
