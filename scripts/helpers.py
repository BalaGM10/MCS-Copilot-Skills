#!/usr/bin/env python3
"""
=============================================================
 AXTR to Markdown — Helper Functions
 Copilot Studio Skill — scripts/helpers.py
 Version : 1.0.0
 Date    : 2026-07-10
=============================================================
 Provides utility functions for:
  - Loading AXTR files
  - Parsing AXTR XML structure
  - Building the Markdown document
  - Saving output files
  - Console output helpers
=============================================================
"""

import os
import sys
import xml.etree.ElementTree as ET
# antigravity review: import timezone alongside datetime to replace deprecated utcnow()
from datetime import datetime, timezone


# ─────────────────────────────────────────────────────────
#  CONSOLE OUTPUT HELPERS
# ─────────────────────────────────────────────────────────

def print_banner():
    """Prints the application banner to stdout."""
    # antigravity review: replaced Unicode box-drawing characters with ASCII
    # to avoid UnicodeEncodeError on Windows cp1252 consoles
    print("""
+==================================================+
|       AXTR to Markdown Converter  v1.0.0         |
|       Copilot Studio Skill Package               |
+==================================================+
    """)

def print_info(message: str):
    """Prints an informational message to stdout."""
    print(f"  [INFO]    {message}")

def print_success(message: str):
    """Prints a success message to stdout."""
    # antigravity review: use ASCII checkmark for Windows cp1252 compatibility
    print(f"  [OK]      {message}")

def print_error(message: str):
    """Prints an error message to stderr."""
    print(f"  [ERROR]   {message}", file=sys.stderr)

def print_warning(message: str):
    """Prints a warning message to stdout."""
    print(f"  [WARN]    {message}")


# ─────────────────────────────────────────────────────────
#  FILE LOADER
# ─────────────────────────────────────────────────────────

def load_axtr_file(file_path: str) -> str | None:
    """
    Loads the content of an AXTR file from a local path.
    Returns the raw XML string or None if the file cannot be read.
    """
    if not os.path.exists(file_path):
        print_error(f"File not found: {file_path}")
        return None

    # antigravity review: warn but don't block on non-.axtr extensions —
    # allows flexibility for renamed or alternative file extensions
    if not file_path.lower().endswith(".axtr"):
        print_warning(f"File does not have .axtr extension: {file_path}")
        print_warning("Attempting to parse anyway...")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # antigravity review: fallback to latin-1 for files exported with
        # non-UTF-8 encoding (common in some D365 locales)
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()
        except Exception as e:
            print_error(f"Encoding error reading file: {e}")
            return None
    except Exception as e:
        print_error(f"Error reading file: {e}")
        return None


# ─────────────────────────────────────────────────────────
#  AXTR XML PARSER
# ─────────────────────────────────────────────────────────

def get_text(element, tag_names: list) -> str | None:
    """
    Searches an XML element for the first matching tag in tag_names list.
    Returns the stripped text content, or None if not found.
    """
    # antigravity review: iterates through tag name variants to support
    # different D365 Task Recorder versions that use different XML schemas
    for tag in tag_names:
        el = element.find(f".//{tag}")
        if el is not None and el.text:
            return el.text.strip()
    return None


def parse_axtr_xml(xml_content: str) -> dict | None:
    """
    Parses the AXTR XML content and returns a structured dict:
    {
        "task_name": str,
        "description": str,
        "version": str,
        "steps": [ { index, caption, comment, action_type, form, control, step_type, screenshot }, ... ]
    }
    Returns None if parsing fails.
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print_error(f"XML parse error: {e}")
        return None

    # ── Extract Metadata ────────────────────────────────
    task_name   = get_text(root, ["TaskName", "Name", "Title", "ProcessName"]) or "Unnamed Process"
    description = get_text(root, ["Description", "Desc", "Summary", "Help"]) or "No description available."
    version     = get_text(root, ["Version", "VersionNumber", "Ver"]) or "1.0"

    # ── Locate Steps ────────────────────────────────────
    # antigravity review: tries multiple known AXTR step container tag names
    # to handle schema differences across D365 versions
    step_tag_candidates = [
        "TaskRecordingStep",
        "Step",
        "RecordingStep",
        "UserAction",
        "Action",
        "TaskStep",
        "RecordedStep"
    ]

    step_elements = []
    for tag in step_tag_candidates:
        found = root.findall(f".//{tag}")
        if found:
            step_elements = found
            break

    if not step_elements:
        print_warning("No step elements found using standard tags. Attempting generic child scan...")
        # antigravity review: generic fallback — scans common container tags
        # and takes their direct children as step elements
        for container_tag in ["Steps", "Actions", "Recording", "TaskRecording"]:
            container = root.find(f".//{container_tag}")
            if container is not None:
                step_elements = list(container)
                if step_elements:
                    break

    # ── Extract Each Step ───────────────────────────────
    steps = []
    for i, el in enumerate(step_elements, 1):
        # antigravity review: each field tries multiple tag name variants
        # with sensible defaults so the output is always usable
        step = {
            "index":       get_text(el, ["StepIndex", "Index", "Order", "Sequence"]) or str(i),
            "caption":     get_text(el, ["Caption", "Title", "Name", "Label", "StepTitle"]) or f"Step {i}",
            "comment":     get_text(el, ["Comment", "Description", "Instruction", "Help", "Note"]) or "",
            "action_type": get_text(el, ["ActionType", "Action", "Type", "Interaction"]) or "Action",
            "form":        get_text(el, ["FormId", "Form", "Screen", "Page", "Module", "View"]) or "",
            "control":     get_text(el, ["ControlName", "Control", "Field", "Element", "Widget"]) or "",
            "step_type":   get_text(el, ["TaskStepType", "StepType", "Category", "Kind"]) or "UserAction",
            "value":       get_text(el, ["Value", "InputValue", "FieldValue", "Data"]) or "",
            "screenshot":  get_text(el, ["Screenshot", "Image", "ScreenCapture", "Thumbnail"]) or None,
        }
        steps.append(step)

    return {
        "task_name":   task_name,
        "description": description,
        "version":     version,
        "steps":       steps
    }


# ─────────────────────────────────────────────────────────
#  SIPOC GENERATOR
# ─────────────────────────────────────────────────────────

# antigravity review: generates a SIPOC analysis by intelligently inferring
# Suppliers, Inputs, Process, Outputs, and Customers from the AXTR step data
def generate_sipoc(steps: list, title: str, department: str) -> dict:
    """
    Generates a SIPOC (Suppliers, Inputs, Process, Outputs, Customers)
    analysis by inferring each element from the recorded AXTR steps.

    Returns a dict with keys: suppliers, inputs, process, outputs, customers.
    Each value is a list of strings.
    """

    # ── Suppliers: systems, modules, and data sources that feed the process ──
    forms_used = list(dict.fromkeys([s["form"] for s in steps if s["form"]]))
    suppliers = []
    suppliers.append("Microsoft Dynamics 365 (ERP System)")
    for form in forms_used[:4]:
        suppliers.append(f"D365 Module: `{form}`")
    if department:
        suppliers.append(f"{department} Department (process owner)")

    # ── Inputs: data, fields, and values entered during the process ──
    inputs = []
    input_steps = [s for s in steps if s["action_type"] in ("Input", "Select", "Search")]
    for s in input_steps:
        field_name = s["control"] or s["caption"]
        if s["value"]:
            inputs.append(f"`{field_name}` (e.g. `{s['value']}`")
        else:
            inputs.append(f"`{field_name}` (user-provided value)")
    if not inputs:
        inputs.append("User-provided data as required by the process screens")
    # Add system access as an input
    inputs.append("Valid D365 user credentials with appropriate security role")

    # ── Process: condense steps into 4-7 high-level phases ──
    # antigravity review: groups consecutive steps by form/screen to create
    # a high-level process summary rather than listing every click
    process_phases = []
    current_form = None
    phase_steps = []
    for s in steps:
        form = s["form"] or "System"
        if form != current_form:
            if phase_steps:
                # Summarise the previous phase
                first_caption = phase_steps[0]["caption"]
                if len(phase_steps) == 1:
                    process_phases.append(f"{first_caption} (`{current_form}`)")
                else:
                    last_caption = phase_steps[-1]["caption"]
                    process_phases.append(f"{first_caption} through {last_caption} (`{current_form}`)")
            current_form = form
            phase_steps = [s]
        else:
            phase_steps.append(s)
    # Flush the last phase
    if phase_steps and current_form:
        first_caption = phase_steps[0]["caption"]
        if len(phase_steps) == 1:
            process_phases.append(f"{first_caption} (`{current_form}`)")
        else:
            last_caption = phase_steps[-1]["caption"]
            process_phases.append(f"{first_caption} through {last_caption} (`{current_form}`)")

    # Cap at 7 phases for SIPOC best practice
    if len(process_phases) > 7:
        process_phases = process_phases[:6] + [f"...and {len(process_phases) - 6} additional phase(s)"]

    # ── Outputs: inferred from the final steps and overall process ──
    outputs = []
    outputs.append(f"Completed **{title}** record in Microsoft Dynamics 365")
    # Check for common terminal action types
    terminal_actions = {"Post": "Posted transaction", "Save": "Saved record",
                        "Validate": "Validated record", "Submit": "Submitted record"}
    for s in reversed(steps):
        action = s["action_type"]
        if action in terminal_actions:
            outputs.append(f"{terminal_actions[action]} via `{s['caption']}`")
            break
    outputs.append("Audit trail / transaction log entry")
    outputs.append("Triggered downstream workflows, approvals, or notifications (if configured)")

    # ── Customers: internal/external recipients of the outputs ──
    customers = []
    customers.append(f"{department} team members (primary users)")
    customers.append("Process Owner / Manager (oversight and approval)")
    customers.append("Internal Audit / Compliance (transaction records)")
    customers.append("Downstream process consumers (e.g. Finance, Procurement, Operations)")

    return {
        "suppliers": suppliers,
        "inputs":    inputs,
        "process":   process_phases,
        "outputs":   outputs,
        "customers": customers,
    }


# ─────────────────────────────────────────────────────────
#  L4 PROCESS DESCRIPTION GENERATOR
# ─────────────────────────────────────────────────────────

# antigravity review: generates a contextual L4 process description based on
# the Dynamics 365 documentation hierarchy and the specific process recorded
def generate_l4_description(title: str, department: str, step_count: int) -> list:
    """
    Returns a list of markdown lines describing what an L4 process document is,
    contextualised to the specific process being documented.
    """
    lines = []
    lines.append(f"This is a **Level 4 (L4) Detailed Work Instruction** for the **{title}** process.")
    lines.append("")
    lines.append("In the process documentation hierarchy, an L4 document is the most granular level of documentation:")
    lines.append("")
    lines.append("| Level | Type | Description |")
    lines.append("|---|---|---|")
    lines.append("| L1 | Process Landscape | Enterprise-wide map of all business processes |")
    lines.append("| L2 | Process Map | End-to-end flow with swimlanes and decision points |")
    lines.append("| L3 | Standard Operating Procedure | Step-level instructions for process execution |")
    lines.append("| **L4** | **Detailed Work Instruction** | **Click-by-click system instructions (this document)** |")
    lines.append("")
    lines.append(f"This L4 document captures **{step_count} recorded steps** from the Microsoft Dynamics 365 Task Recorder, ")
    lines.append(f"providing **{department}** users with exact screen-by-screen, field-by-field instructions ")
    lines.append("to execute this process consistently and accurately.")
    lines.append("")
    lines.append("> **Dynamics 365 Context:** This document was generated from a Task Recorder (.axtr) export. ")
    lines.append("> Task Recorder is a built-in D365 tool that captures user interactions for training, ")
    lines.append("> business process modelling (BPM), and Regression Suite Automation Tool (RSAT) testing.")
    return lines


# ─────────────────────────────────────────────────────────
#  MARKDOWN DOCUMENT BUILDER
# ─────────────────────────────────────────────────────────

def build_markdown_document(
    parsed_data: dict,
    title: str,
    author: str,
    department: str,
    process_level: str = "L4",
    include_screenshots: bool = False
) -> str:
    """
    Builds a complete Level 3 or Level 4 Markdown training document
    from the parsed AXTR data.
    """
    # antigravity review: replaced deprecated datetime.utcnow() with
    # timezone-aware datetime.now(timezone.utc) (deprecated since Python 3.12)
    today       = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    steps       = parsed_data.get("steps", [])
    description = parsed_data.get("description", "No description available.")
    version     = parsed_data.get("version", "1.0")
    level_label = "Level 4 — Detailed Step-by-Step Procedure" if process_level == "L4" \
                  else "Level 3 — Standard Operating Procedure"

    md = []

    # ══ DOCUMENT HEADER ════════════════════════════════
    md.append(f"# {title}")
    md.append("")
    md.append(f"| Field | Details |")
    md.append(f"|---|---|")
    md.append(f"| **Document Type** | {level_label} |")
    md.append(f"| **Author** | {author} |")
    md.append(f"| **Department** | {department} |")
    md.append(f"| **Version** | {version} |")
    md.append(f"| **Date** | {today} |")
    md.append(f"| **System** | Microsoft Dynamics 365 |")
    md.append(f"| **Source** | Task Recorder (AXTR) |")
    md.append("")
    md.append("---")
    md.append("")

    # ══ 1. PURPOSE ═════════════════════════════════════
    md.append("## 1. Purpose")
    md.append("")
    md.append(f"> {description}")
    md.append("")
    md.append(f"This document provides a {level_label} for **{title}** in Microsoft Dynamics 365.")
    md.append("")

    # ══ 2. L4 PROCESS DESCRIPTION ══════════════════════
    # antigravity review: new section — provides context on what an L4 document
    # is within the process documentation hierarchy, with D365-specific detail
    if process_level == "L4":
        md.append("## 2. L4 Process Description")
        md.append("")
        l4_desc_lines = generate_l4_description(title, department, len(steps))
        md.extend(l4_desc_lines)
        md.append("")

    # ══ 3. SIPOC ANALYSIS ══════════════════════════════
    # antigravity review: new section — auto-generates a SIPOC diagram from
    # the AXTR recording data to give process context at a glance
    md.append(f"## {3 if process_level == 'L4' else 2}. SIPOC Analysis")
    md.append("")
    md.append("> **SIPOC** (Suppliers, Inputs, Process, Outputs, Customers) provides a high-level ")
    md.append("> view of the process and its ecosystem, identifying what feeds into the process, ")
    md.append("> what the process produces, and who benefits from its outputs.")
    md.append("")

    sipoc = generate_sipoc(steps, title, department)

    # Suppliers
    md.append(f"### {3 if process_level == 'L4' else 2}.1 Suppliers")
    md.append("")
    md.append("*The people, systems, or organisations that provide the resources required for this process.*")
    md.append("")
    for item in sipoc["suppliers"]:
        md.append(f"- {item}")
    md.append("")

    # Inputs
    md.append(f"### {3 if process_level == 'L4' else 2}.2 Inputs")
    md.append("")
    md.append("*The data, materials, or resources provided by the suppliers to make the process function.*")
    md.append("")
    for item in sipoc["inputs"]:
        md.append(f"- {item}")
    md.append("")

    # Process
    md.append(f"### {3 if process_level == 'L4' else 2}.3 Process (High-Level)")
    md.append("")
    md.append("*A high-level, chronological summary of the major phases that transform inputs into outputs.*")
    md.append("")
    for i, phase in enumerate(sipoc["process"], 1):
        md.append(f"{i}. {phase}")
    md.append("")

    # Outputs
    md.append(f"### {3 if process_level == 'L4' else 2}.4 Outputs")
    md.append("")
    md.append("*The final products, services, or information delivered by the process.*")
    md.append("")
    for item in sipoc["outputs"]:
        md.append(f"- {item}")
    md.append("")

    # Customers
    md.append(f"### {3 if process_level == 'L4' else 2}.5 Customers")
    md.append("")
    md.append("*The internal or external recipients who use or benefit from the outputs.*")
    md.append("")
    for item in sipoc["customers"]:
        md.append(f"- {item}")
    md.append("")

    # ── Section number offset for remaining sections ──
    # antigravity review: L4 docs have 2 extra sections (L4 Description + SIPOC)
    # so subsequent numbering starts at 4; L3 has 1 extra (SIPOC) starting at 3
    n = 4 if process_level == "L4" else 3

    # ══ SCOPE ══════════════════════════════════════════
    md.append(f"## {n}. Scope")
    md.append("")
    md.append(f"This procedure applies to all **{department}** users responsible for performing the **{title}** process in Microsoft Dynamics 365.")
    md.append("")

    # ══ PREREQUISITES ══════════════════════════════════
    md.append(f"## {n + 1}. Prerequisites")
    md.append("")
    md.append("Before starting this process, ensure the following are in place:")
    md.append("")

    # antigravity review: dynamically lists unique screens/forms used in the
    # recording to generate context-aware prerequisites (capped at 6)
    forms_used = list(dict.fromkeys([s["form"] for s in steps if s["form"]]))
    if forms_used:
        md.append("**Required System Access:**")
        md.append("")
        for form in forms_used[:6]:
            md.append(f"- Access to the `{form}` screen / module")
    else:
        md.append("- Valid Microsoft Dynamics 365 user account with appropriate permissions")
        md.append("- Required master data has been set up in the system")
        md.append("- Relevant reference documents or approval workflows are in place")
    md.append("")

    # ══ ROLES & RESPONSIBILITIES ═══════════════════════
    md.append(f"## {n + 2}. Roles & Responsibilities")
    md.append("")
    md.append("| Role | Responsibility |")
    md.append("|---|---|")
    md.append(f"| {department} User | Execute the steps documented in this procedure |")
    md.append("| System Administrator | Maintain correct access, roles, and system configuration |")
    md.append("| Process Owner | Review, approve, and maintain this document |")
    md.append("")

    # ══ STEP-BY-STEP PROCEDURE ═════════════════════════
    md.append(f"## {n + 3}. Step-by-Step Procedure")
    md.append("")

    if not steps:
        md.append("> ⚠️ **No steps were extracted from the AXTR file.** Please verify the file is a valid Task Recorder export.")
    else:
        for step in steps:
            # Step heading
            md.append(f"### Step {step['index']}: {step['caption']}")
            md.append("")

            # Instruction / comment
            if step["comment"]:
                md.append(f"**Instruction:** {step['comment']}")
                md.append("")

            # Step details table
            details_rows = []
            if step["action_type"]:
                details_rows.append(("Action", f"`{step['action_type']}`"))
            if step["form"]:
                details_rows.append(("Screen / Form", f"`{step['form']}`"))
            if step["control"]:
                details_rows.append(("Field / Control", f"`{step['control']}`"))
            if step["value"]:
                details_rows.append(("Value / Input", f"`{step['value']}`"))
            if step["step_type"]:
                details_rows.append(("Step Type", f"`{step['step_type']}`"))

            if details_rows:
                md.append("| Detail | Value |")
                md.append("|---|---|")
                for label, val in details_rows:
                    md.append(f"| **{label}** | {val} |")
                md.append("")

            # antigravity review: L4 documents include per-step expected results;
            # L3 documents omit this for brevity
            if process_level == "L4":
                md.append(f"**Expected Result:** The system responds to the `{step['action_type']}` action on `{step['caption']}`.")
                md.append("")

            # antigravity review: screenshot embedding uses data: URIs which can
            # produce very large files — consider --screenshots-dir for extraction
            if include_screenshots and step["screenshot"]:
                md.append(f"**Screenshot:**")
                md.append("")
                md.append(f"![Step {step['index']} — {step['caption']}](data:image/png;base64,{step['screenshot']})")
                md.append("")

            md.append("---")
            md.append("")

    # ══ EXPECTED OUTCOMES ══════════════════════════════
    md.append(f"## {n + 4}. Expected Outcomes")
    md.append("")
    md.append(f"Upon successful completion of all **{len(steps)} steps**, the following outcomes are expected:")
    md.append("")
    md.append(f"- The **{title}** process has been fully executed in Microsoft Dynamics 365")
    md.append("- All required fields have been populated and validated")
    md.append("- No system error messages are displayed")
    md.append("- The record has been saved and is visible in the relevant list or view")
    md.append("- Any downstream workflows, approvals, or notifications have been triggered")
    md.append("")

    # ══ TROUBLESHOOTING ════════════════════════════════
    md.append(f"## {n + 5}. Troubleshooting")
    md.append("")
    md.append("| Issue | Possible Cause | Resolution |")
    md.append("|---|---|---|")
    md.append("| Access denied / permission error | Insufficient security role | Contact your system administrator to review role assignments |")
    md.append("| Required field is missing or hidden | Personalisation or field-level security | Check field visibility settings or contact your admin |")
    md.append("| Validation error on save | Missing mandatory data | Review all highlighted fields and complete required entries |")
    md.append("| Record not saving | Workflow or approval blocking | Check active workflows and approval chains |")
    md.append("| Screen or menu not visible | Module not enabled or wrong company | Verify the correct legal entity and module is selected |")
    md.append("")

    # ══ RELATED DOCUMENTS ══════════════════════════════
    md.append(f"## {n + 6}. Related Documents")
    md.append("")
    md.append("| Document | Description |")
    md.append("|---|---|")
    md.append(f"| {title} — Level 3 Process Map | High-level swimlane diagram for this process |")
    md.append("| Dynamics 365 User Access Guide | Role and permission setup reference |")
    md.append("| System Configuration Guide | Dynamics 365 environment setup |")
    md.append("| Training Needs Assessment | List of all processes requiring documentation |")
    md.append("")

    # ══ REVISION HISTORY ═══════════════════════════════
    md.append(f"## {n + 7}. Revision History")
    md.append("")
    md.append("| Version | Date | Author | Description of Change |")
    md.append("|---|---|---|---|")
    md.append(f"| {version} | {today} | {author} | Initial document — auto-generated from AXTR recording |")
    md.append("")

    # ══ FOOTER ═════════════════════════════════════════
    md.append("---")
    md.append("")
    md.append(f"*This document was automatically generated by the **AXTR to Markdown Copilot Studio Skill** on {today}.*  ")
    md.append(f"*Source system: Microsoft Dynamics 365 Task Recorder | Document level: {process_level}*")

    return "\n".join(md)


# ─────────────────────────────────────────────────────────
#  FILE SAVER
# ─────────────────────────────────────────────────────────

def save_markdown_file(content: str, output_path: str) -> bool:
    """
    Saves the Markdown content to the specified file path.
    Creates parent directories if they do not exist.
    Returns True on success, False on failure.
    """
    try:
        output_dir = os.path.dirname(output_path)
        # antigravity review: creates intermediate directories so users don't
        # need to manually create output folders before running the script
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    except Exception as e:
        print_error(f"Failed to save file: {e}")
        return False
