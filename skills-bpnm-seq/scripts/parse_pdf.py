# =============================================================================
# parse_pdf.py — PDF visual renderer for LLM Vision BPMN extraction
# Version: 1.0.0
# Date: 2026-09-09
# Original Author: Bala Madhusoodhanan (initial skill concept)
# Enhanced By: Antigravity AI (Peer Coding)
# Changelog:
#   1.0.0 (2026-09-09) - New component added by Antigravity. Renders PDF pages
#                        to 300 DPI PNG, extracts text overlay, outputs
#                        structured vision prompt template for LLM analysis.
# =============================================================================

import argparse
import sys
import os
import json

# Assuming scripts are run from the directory they reside in or using python -m
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import ensure_dependencies

# Ensure pymupdf is installed
ensure_dependencies('pymupdf')
import fitz

def parse_pdf(input_path: str, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        doc = fitz.open(input_path)
        text_overlay = {"pages": []}
        rendered_images = []
        
        for i in range(len(doc)):
            page = doc[i]
            
            # Render to 300 DPI PNG
            pix = page.get_pixmap(dpi=300)
            img_filename = f"page_{i+1}.png"
            img_path = os.path.join(output_dir, img_filename)
            pix.save(img_path)
            rendered_images.append(img_path)
            
            # Extract text
            words_data = []
            words = page.get_text('words')
            for w in words:
                x0, y0, x1, y1, word, block_no, line_no, word_no = w
                words_data.append({
                    "text": word,
                    "bbox": [x0, y0, x1, y1]
                })
                
            text_overlay["pages"].append({
                "page": i+1,
                "image_path": img_filename,
                "words": words_data
            })
            
        json_path = os.path.join(output_dir, "text_overlay.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(text_overlay, f, indent=2)
            
        print(f"Successfully rendered {len(doc)} pages to {output_dir}")
        print("Output paths:")
        for img in rendered_images:
            print(f"- {img}")
        print(f"- {json_path}")
        
        print("\n=== PROMPT TEMPLATE FOR AGENT ===")
        print("Please review the provided BPMN diagram images.")
        print("Extract the process information into the standard JSON IR schema.")
        print("Identify all participants (pools/lanes), activities (tasks/sub-processes), gateways (exclusive/parallel/inclusive), events (start/intermediate/end), and data objects.")
        print("Reconstruct the sequence flows and message flows between these nodes.")
        print("Ensure accurate grouping of nodes within their respective participant lanes.")
        print("=================================")
            
    except Exception as e:
        print(f"Error parsing PDF: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse PDF to Images and Text Overlay for LLM Vision analysis')
    parser.add_argument('input', help='Input .pdf file')
    parser.add_argument('--output-dir', required=True, help='Output directory for images and JSON')
    
    args = parser.parse_args()
    parse_pdf(args.input, args.output_dir)
