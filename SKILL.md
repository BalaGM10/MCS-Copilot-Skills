---
name: axtr-to-markdown
description: Converts Microsoft Dynamics 365 AXTR task recording files into structured Level 4 Process Training Documents in Markdown format. Parses the XML-based AXTR file, extracts all recorded user steps, and formats them into a professional training document ready for use as a knowledge source or user guide.
version: 1.0.0
author: Copilot Studio Skill Package
tags:
  - dynamics365
  - process-documentation
  - training
  - axtr
  - markdown
  - level4
---

# AXTR to Markdown — Skill

## What This Skill Does

This skill takes a **Microsoft Dynamics 365 Task Recorder AXTR file** as input and produces a **Level 4 Process Training Document** in Markdown format.

It is designed to be used by an agent that helps users convert screen recordings of Dynamics 365 processes into structured, professional documentation — without manual effort.

---

## When to Use This Skill

Use this skill when the user:
- Uploads or references an `.axtr` file
- Asks to "convert a task recording to a training document"
- Asks to "generate a Level 4 process document"
- Asks to "create documentation from a Dynamics 365 recording"
- Wants to produce a step-by-step guide from a screen recording

---

## How to Run This Skill

### Step 1 — Get the AXTR File
Ask the user for one of the following:
- A **file path** to the `.axtr` file on their local machine or network share
- A **SharePoint or OneDrive URL** to the `.axtr` file
- The **raw XML content** pasted directly

### Step 2 — Run the Conversion Script
Execute the Python script located in `scripts/axtr_to_markdown.py` with the appropriate arguments:

```bash
# From a local file path
python scripts/axtr_to_markdown.py --file "path/to/recording.axtr" --output "output/ProcessName-L4.md"

# With optional metadata
python scripts/axtr_to_markdown.py \
  --file "path/to/recording.axtr" \
  --title "Vendor Invoice Creation" \
  --author "Jane Smith" \
  --department "Finance" \
  --level L4 \
  --output "output/VendorInvoice-L4.md"
```

### Step 3 — Return Output to User
- Present the generated Markdown content to the user
- Offer to save the file to SharePoint, OneDrive, or local disk
- Optionally suggest uploading the `.md` file as a Copilot Studio knowledge source

---

## Input Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `--file` | Yes* | — | Path or URL to the `.axtr` file |
| `--content` | Yes* | — | Raw XML string (alternative to `--file`) |
| `--title` | No | Extracted from AXTR | Custom title for the document |
| `--author` | No | `Unknown` | Author name for document header |
| `--department` | No | `Not Specified` | Department / process owner |
| `--level` | No | `L4` | Process level: `L3` or `L4` |
| `--output` | No | `output.md` | Output file path for the Markdown file |
| `--screenshots` | No | `false` | Include embedded screenshots if present in AXTR |

*Either `--file` or `--content` must be provided.

---

## Output

The skill produces a **Markdown file** (`.md`) with the following structure:

```
# [Process Title] — Level 4 Process Document
## 1. Purpose
## 2. L4 Process Description
## 3. SIPOC Analysis
   ### 3.1 Suppliers
   ### 3.2 Inputs
   ### 3.3 Process (High-Level)
   ### 3.4 Outputs
   ### 3.5 Customers
## 4. Scope
## 5. Prerequisites
## 6. Roles & Responsibilities
## 7. Step-by-Step Procedure
   ### Step 1: ...
   ### Step 2: ...
   ...
## 8. Expected Outcomes
## 9. Troubleshooting
## 10. Related Documents
## 11. Revision History
```

---

## Example Agent Conversation

```
User:  "Can you convert this AXTR file into a training document?"
Agent: "Sure! Please share the path or URL to your .axtr file."
User:  "Here it is: C:/Recordings/VendorInvoice.axtr"
Agent: [runs scripts/axtr_to_markdown.py --file "C:/Recordings/VendorInvoice.axtr"]
Agent: "Done! Your Level 4 training document has been created.
        📄 Title: Vendor Invoice Creation
        📋 Steps documented: 14
        📁 Output: output/VendorInvoice-L4.md
        Would you like me to save this to SharePoint?"
```

---

## Script Location

```
axtr-to-markdown/
├── SKILL.md                            ← You are here
├── scripts/
│   ├── axtr_to_markdown.py             ← Main conversion script
│   └── helpers.py                      ← Parsing & formatting utilities
├── references/
│   ├── axtr-format-reference.md        ← AXTR XML structure guide
│   └── level4-process-guide.md         ← What is a Level 4 process?
└── assets/
    ├── level4-template.md              ← Blank L4 template
    └── sample.axtr                     ← Sample AXTR file for testing
```

---

## Error Handling

If the script encounters an issue, it will return a clear error message:

| Error | Cause | Resolution |
|---|---|---|
| `File not found` | Invalid path or URL | Ask user to verify the file location |
| `XML parse error` | Corrupted or non-AXTR file | Ask user to re-export from Task Recorder |
| `No steps found` | Empty recording | Ask user to check the recording |
| `Permission denied` | File access issue | Ask user to check file permissions |
