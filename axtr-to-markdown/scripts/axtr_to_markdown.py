#!/usr/bin/env python3
"""
=============================================================
 AXTR to Markdown Converter
 Copilot Studio Skill — scripts/axtr_to_markdown.py
 Version : 1.0.0
 Date    : 2026-07-10
=============================================================
 Converts Microsoft Dynamics 365 Task Recorder (.axtr) files
 into structured Level 4 Process Training Documents in Markdown.

 Usage:
   python axtr_to_markdown.py --file recording.axtr
   python axtr_to_markdown.py --file recording.axtr --title "My Process" --author "Jane" --department "Finance" --level L4 --output out.md
=============================================================
"""

import argparse
import sys
import os

# antigravity review: reconfigure stdout/stderr to UTF-8 so generated markdown
# containing em-dashes and other Unicode prints correctly on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# antigravity review: imports from sibling module — works for CLI invocation
# but would fail if imported as a package without __init__.py
from helpers import (
    load_axtr_file,
    parse_axtr_xml,
    build_markdown_document,
    save_markdown_file,
    print_banner,
    print_success,
    print_error,
    print_info
)


# ─────────────────────────────────────────────────────────
#  ARGUMENT PARSER
# ─────────────────────────────────────────────────────────
def parse_args():
    """
    Parses CLI arguments for the AXTR to Markdown converter.
    Supports mutually exclusive --file / --content source inputs.
    """
    parser = argparse.ArgumentParser(
        prog="axtr_to_markdown",
        description="Convert a Dynamics 365 AXTR file into a Level 4 Markdown training document."
    )

    # antigravity review: mutually exclusive group ensures exactly one input source
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--file", "-f",
        type=str,
        help="Path to the .axtr file (local or network path)"
    )
    source.add_argument(
        "--content", "-c",
        type=str,
        help="Raw AXTR XML content as a string (alternative to --file)"
    )

    parser.add_argument(
        "--title", "-t",
        type=str,
        default=None,
        help="Custom process title (default: extracted from AXTR)"
    )
    parser.add_argument(
        "--author", "-a",
        type=str,
        default="Unknown",
        help="Author name for document header (default: Unknown)"
    )
    parser.add_argument(
        "--department", "-d",
        type=str,
        default="Not Specified",
        help="Department / process owner (default: Not Specified)"
    )
    parser.add_argument(
        "--level", "-l",
        type=str,
        choices=["L3", "L4"],
        default="L4",
        help="Process documentation level: L3 or L4 (default: L4)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output.md",
        help="Output Markdown file path (default: output.md)"
    )
    parser.add_argument(
        "--screenshots", "-s",
        action="store_true",
        default=False,
        help="Embed base64 screenshots from AXTR into the Markdown (default: False)"
    )
    parser.add_argument(
        "--print", "-p",
        action="store_true",
        default=False,
        help="Print the Markdown content to the console (default: False)"
    )

    return parser.parse_args()


# ─────────────────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────
def main():
    """
    Main pipeline: load → parse → build markdown → save.
    """
    print_banner()
    args = parse_args()

    # ── Step 1: Load AXTR Content ──────────────────────
    print_info("Loading AXTR file...")

    if args.file:
        xml_content = load_axtr_file(args.file)
        if xml_content is None:
            print_error(f"Could not load file: {args.file}")
            sys.exit(1)
        print_info(f"File loaded: {args.file}")
    else:
        # antigravity review: --content path — no validation on empty string,
        # but parse_axtr_xml will catch invalid XML gracefully
        xml_content = args.content
        print_info("Using inline XML content.")

    # ── Step 2: Parse AXTR XML ─────────────────────────
    print_info("Parsing AXTR XML structure...")

    parsed = parse_axtr_xml(xml_content)
    if parsed is None:
        print_error("Failed to parse AXTR XML. Please verify the file is a valid AXTR recording.")
        sys.exit(1)

    step_count = len(parsed.get("steps", []))
    resolved_title = args.title or parsed.get("task_name", "Unnamed Process")

    print_info(f"Process title : {resolved_title}")
    print_info(f"Steps found   : {step_count}")
    # antigravity review: truncate long descriptions to keep console output tidy
    print_info(f"Description   : {parsed.get('description', 'N/A')[:80]}...")

    if step_count == 0:
        print_error("No steps were found in the AXTR file. The recording may be empty.")
        sys.exit(1)

    # ── Step 3: Build Markdown Document ───────────────
    print_info(f"Building Level {args.level} Markdown document...")

    markdown_content = build_markdown_document(
        parsed_data=parsed,
        title=resolved_title,
        author=args.author,
        department=args.department,
        process_level=args.level,
        include_screenshots=args.screenshots
    )

    # ── Step 4: Print to Console (if requested) ────────
    if getattr(args, 'print'):
        # antigravity review: use ASCII separator for Windows cp1252 compatibility
        print("\n" + "=" * 60)
        print(markdown_content)
        print("=" * 60 + "\n")

    # ── Step 5: Save Markdown File ─────────────────────
    print_info(f"Saving output to: {args.output}")

    saved = save_markdown_file(markdown_content, args.output)
    if not saved:
        print_error(f"Failed to save file to: {args.output}")
        sys.exit(1)

    # ── Done ───────────────────────────────────────────
    print_success("Conversion complete!")
    print_success(f"Title    : {resolved_title}")
    print_success(f"Steps    : {step_count}")
    print_success(f"Level    : {args.level}")
    print_success(f"Output   : {os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
