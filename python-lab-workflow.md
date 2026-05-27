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

### Step 1 — Start the session and set context

```
/python
@progress.md all 4 labs complete. Starting Курсовой now.
@AI_Курсовая_Работа_Dataset_Generation.docx this is the dataset
analysis document from deep research. It contains the generation
script, 6 analytical questions, and the full ML pipeline description.
I have already generated moscow_housing_study.csv from the script.
Help me plan the Курсовой structure and what to tackle first.
```

### Step 2 — Feed the dataset

```
@moscow_housing_study.csv here is the dataset. Describe what you see.
```

### Step 3 — Confirm the structure

```
@term-paper-structure.md this is the planned structure for the Курсовой.
Does it need adjusting based on the dataset and analytical questions?
```

### During the Курсовой — reference the deep search document anytime

```
# When you need the clustering technique explained:
@AI_Курсовая_Работа_Dataset_Generation.docx explain the clustering section

# When you need the imputation approach:
@AI_Курсовая_Работа_Dataset_Generation.docx explain missing value imputation

# When you need the full ML pipeline:
@AI_Курсовая_Работа_Dataset_Generation.docx explain the supervised learning section
```

The deep research document has exact Python snippets for each technique
aligned to your specific dataset columns — use it as a persistent reference
throughout the Курсовой rather than feeding it only once.

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
