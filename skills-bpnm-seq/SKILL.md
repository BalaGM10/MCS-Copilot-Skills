---
# =============================================================================
# Skill: bpmn-to-mermaid-sequence
# Version: 1.0.0
# Date: 2026-09-09
# Original Author: Bala Madhusoodhanan
# Enhanced By: Antigravity AI (Peer Coding)
# Changelog:
#   1.0.0 (2026-09-09) - Antigravity peer coding enhancement. Added PDF visual
#                        input, sequence diagram output, JSON IR architecture,
#                        LLM Vision parsing, reference docs, and examples.
#   0.1.0 (2026-09-09) - Initial draft by Bala Madhusoodhanan. Visio-to-Mermaid
#                        flowchart converter with swimlane/subgraph support.
# =============================================================================
name: bpmn-to-mermaid-sequence
description: >
  Convert BPMN process diagrams from Visio (.vsdx) files or visual PDF documents
  into Mermaid sequence diagram code. Accepts user-uploaded files, parses shapes,
  connectors, swimlanes, and process flows, and outputs renderable Mermaid sequence
  diagrams that capture all participants (users, systems), process steps, and
  decision trees. Activate this skill when the user asks to convert a Visio diagram,
  BPMN process, or PDF process document to a Mermaid sequence diagram.
---

### Prerequisites
- Python 3.9+
- `vsdx` library (auto-installed) — for .vsdx parsing
- `PyMuPDF` / `pymupdf` (auto-installed) — for PDF rendering
- LLM Vision capabilities — for analyzing rendered PDF images
- Optional: SharePoint MCP connector for fetching files by process name

### Supported Input Formats
- `.vsdx` — Microsoft Visio files with BPMN notation
- `.pdf` — PDF documents containing visual BPMN diagrams

### Output Format
- Always produces Mermaid **sequence diagrams**
- Captures: all participants (users, systems, roles), process steps as messages, decision trees as alt/else blocks, parallel work as par/and blocks

### Workflow (4 Steps)

#### Step 1 — Receive Input File
The user uploads a `.vsdx` or `.pdf` file directly. Detect format by file extension.
- If user provides a local file path → use directly
- If user drags and drops a file → use the provided path
- **Optional fallback**: If user provides a process name, use SharePoint MCP to search and download

#### Step 2 — Parse to JSON Intermediate Representation

**For .vsdx files:**
Run the parse_vsdx.py script:
```bash
python <skill-dir>/scripts/parse_vsdx.py "<path>.vsdx" --output parsed.json
```
This deterministically extracts shapes, connectors, swimlanes into JSON IR.

**For .pdf files:**
1. Run parse_pdf.py to render pages to images and extract text:
```bash
python <skill-dir>/scripts/parse_pdf.py "<path>.pdf" --output-dir temp_images/
```
2. View the rendered PNG image(s) using vision capabilities
3. Using the structured prompt from [pdf_vision_guide.md](references/pdf_vision_guide.md), analyze the image to identify:
   - Participants (pools, swimlanes, actors, systems)
   - Activities (tasks with owning participant)
   - Gateways (decision points with conditions)
   - Events (start, end, intermediate)
   - Flows (sequence and message flows)
4. Construct the JSON IR from the vision analysis
5. Use the text_overlay.json to validate/correct extracted labels

**What the JSON IR contains:**
- Metadata (source file, type, title)
- Processes array, each with:
  - Participants (id, name, display order)
  - Nodes (id, BPMN type, label, owning participant)
  - Edges (id, source, target, label, flow type)

See [examples/sample_bpmn_input.json](examples/sample_bpmn_input.json) for the full schema.

#### Step 3 — Convert to Mermaid Sequence Diagram
Run convert_to_sequence.py:
```bash
python <skill-dir>/scripts/convert_to_sequence.py parsed.json --output diagram.md
```

Conversion rules (include the full mapping table):

| BPMN Element | Mermaid Sequence Element |
|---|---|
| Pool / Swimlane | `participant` declaration |
| Task crossing lanes | `LaneA->>LaneB: Task Label` |
| Task within lane | `Lane->>Lane: Task Label` |
| Start Event | `Note over Participant: 🟢 Start: Label` |
| End Event | `Note over Participant: 🔴 End: Label` |
| Exclusive Gateway (XOR) | `alt Condition` / `else Condition` / `end` |
| Parallel Gateway (AND) | `par Label` / `and Label` / `end` |
| Intermediate Timer Event | `Note over Participant: ⏱ Wait: Label` |
| Data Object | `Note right of Participant: 📄 Label` |
| Message Flow (cross-pool) | `A-)B: message` (async) |
| Sub-Process | `rect rgb(200,220,255)` block |
| Loop | `loop Condition` block |

See [references/bpmn_to_sequence_mapping.md](references/bpmn_to_sequence_mapping.md) for complete mapping details.

#### Step 4 — Present Output
1. Create an artifact (markdown file) with:
   - A heading for each process/page
   - The Mermaid sequence diagram in a fenced ```mermaid code block
2. Show the artifact to the user
3. Offer to refine: adjust participant names, reorder participants, add activation markers, etc.

See [examples/sample_sequence_output.md](examples/sample_sequence_output.md) for a complete example.

### Troubleshooting Table
| Issue | Resolution |
|---|---|
| `ModuleNotFoundError: No module named 'vsdx'` | Run `pip install vsdx` |
| `ModuleNotFoundError: No module named 'fitz'` | Run `pip install pymupdf` |
| No shapes extracted from VSDX | Check for grouped/nested shapes — they may be inside group containers |
| Connectors not detected in VSDX | Some files store connections in `<Connects>` sections; unusual connector types may need manual mapping |
| Swimlanes not detected | May be stored as `FunctionBand` or custom containers — check master shape name |
| PDF renders as blank | The PDF may be password-protected or corrupted |
| Vision analysis misses shapes | Try rendering at higher DPI (400+) or zoom into specific areas |
| Legacy `.vsd` format | Not supported by vsdx library — convert to .vsdx first or use PDF export + vision |
| Too many participants | Mermaid renders poorly with >8 participants — consider grouping with `box` blocks |

### Reference Documentation
- [vsdx_format.md](references/vsdx_format.md) — .vsdx file internals
- [mermaid_syntax.md](references/mermaid_syntax.md) — Mermaid sequence diagram syntax
- [bpmn_to_sequence_mapping.md](references/bpmn_to_sequence_mapping.md) — BPMN→Sequence mapping rules
- [pdf_vision_guide.md](references/pdf_vision_guide.md) — LLM Vision PDF parsing guide
