<!-- ==========================================================================
  pdf_vision_guide.md — LLM Vision PDF BPMN Extraction Guide
  Version: 1.0.0 | Date: 2026-09-09
  Original Author: Bala Madhusoodhanan | Enhanced By: Antigravity AI (Peer Coding)
  Changelog:
    1.0.0 (2026-09-09) - Created by Antigravity during peer coding enhancement.
========================================================================== -->

# PDF Vision Guide for BPMN Extraction

## Overview
When translating visual BPMN PDFs into structured formats, we employ a hybrid approach:
1. Render the PDF pages to high-resolution (300 DPI) PNG images.
2. Extract the textual overlay directly from the PDF for exact label accuracy.
3. An LLM agent views the images (incorporating text hints) to deduce the structural graph using a structured JSON extraction prompt.

## PDF Rendering with PyMuPDF

Use `PyMuPDF` (`fitz`) to render documents.

**Installation:**
```bash
pip install pymupdf
```

**Code Example:**
```python
import fitz  # PyMuPDF

def process_pdf(path):
    doc = fitz.open(path)
    for i, page in enumerate(doc):
        # 1. Render to Image
        pix = page.get_pixmap(dpi=300)
        pix.save(f"page_{i}.png")
        
        # 2. Extract Text
        words = page.get_text('words')
        for w in words:
            # w is (x0, y0, x1, y1, "word", block_no, line_no, word_no)
            print(w)
```

## Structured Vision Prompt Template

When querying the LLM Vision model, use the following structured prompt to enforce uniform JSON extraction:

```text
You are an expert BPMN analyst. Analyze the provided BPMN diagram image.
1. Identify all pools and swimlanes (with their exact names).
2. List all activities/tasks, identifying which lane owns each.
3. Identify all gateways. Specify their type (XOR, AND, OR) based on their internal marker (X, +, O) and note any condition labels on outgoing edges.
4. Identify start and end events.
5. Trace all sequence flows (solid arrows) from source to target, including edge labels.
6. Identify message flows (dashed arrows) crossing pools.
7. Output EVERYTHING strictly matching the JSON schema below. Do not include markdown formatting or explanations.

SCHEMA:
{
  "metadata": { "source_file": "...", "source_type": "pdf", "title": "...", "pages": 1 },
  "processes": [{
    "name": "...", 
    "page": 1,
    "participants": [{ "id": "...", "name": "...", "order": 1 }],
    "nodes": [{ "id": "...", "type": "start_event|end_event|task|exclusive_gateway|parallel_gateway|inclusive_gateway", "label": "...", "participant_id": "..." }],
    "edges": [{ "id": "...", "source": "...", "target": "...", "label": "...", "type": "sequence_flow|message_flow" }]
  }]
}
```

## Text Overlay Supplementation
Vision models often hallucinate slight misspellings of diagram labels.
- **Spatial Matching:** Extract `get_text('words')` bounds.
- If the Vision model reports a task label as "Aprove Request", look at the bounding box geometry heuristics. If the PDF text overlay contains "Approve Request" in that vicinity, correct the extracted JSON to use the perfectly accurate text string.

## Common Visual BPMN Patterns
Instruct the agent/logic to recognize standard BPMN conventions:
- **Rounded rectangles** = Tasks / Activities.
- **Diamonds** = Gateways.
  - *Empty or X inside* = Exclusive (XOR).
  - *+ inside* = Parallel (AND).
  - *O inside* = Inclusive (OR).
- **Circles** = Events.
  - *Thin border* = Start event.
  - *Thick border* = End event.
  - *Double border* = Intermediate event.
- **Arrows**:
  - *Solid line, filled head* = Sequence Flow (within process).
  - *Dashed line, open head* = Message Flow (cross-pool).
- **Layout**:
  - Large encompassing boxes (horizontal or vertical) = Pools / Lanes.
  - Text inside shapes denotes the label.
