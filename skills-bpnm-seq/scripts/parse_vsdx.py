# =============================================================================
# parse_vsdx.py — Visio (.vsdx) BPMN parser → JSON Intermediate Representation
# Version: 1.0.0
# Date: 2026-09-09
# Original Author: Bala Madhusoodhanan (initial VSDX parsing concept)
# Enhanced By: Antigravity AI (Peer Coding)
# Changelog:
#   1.0.0 (2026-09-09) - Antigravity enhancement. Refined shape extraction,
#                        added swimlane spatial detection, connector XML
#                        inspection, and JSON IR output format.
#   0.1.0 (2026-09-09) - Initial concept by Bala Madhusoodhanan.
# =============================================================================

import argparse
import sys
import os

# Assuming scripts are run from the directory they reside in or using python -m
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import ensure_dependencies, classify_bpmn_shape, save_json_ir, sanitize_label

# Ensure vsdx is installed
ensure_dependencies('vsdx')
from vsdx import VisioFile

def parse_vsdx(input_path: str, output_path: str):
    try:
        with VisioFile(input_path) as vis:
            ir_data = {
                "metadata": {
                    "source_file": input_path,
                    "source_type": "vsdx",
                    "title": os.path.basename(input_path),
                    "pages": len(vis.pages)
                },
                "processes": []
            }
            
            for i, page in enumerate(vis.pages):
                process = {
                    "name": page.name,
                    "page": i + 1,
                    "participants": [],
                    "nodes": [],
                    "edges": []
                }
                
                shapes_by_id = {}
                lanes = []
                connectors = []
                
                for shape in page.child_shapes:
                    shape_id = str(shape.ID)
                    shapes_by_id[shape_id] = shape
                    
                    master_name = shape.master_shape.name if shape.master_shape else ""
                    if not master_name and shape.master_page:
                         master_name = shape.master_page.name
                         
                    shape_type = classify_bpmn_shape(master_name)
                    
                    if shape_type in ['pool', 'lane']:
                        lanes.append({
                            'id': shape_id,
                            'name': sanitize_label(shape.text),
                            'bbox': (shape.x, shape.y, shape.width, shape.height)
                        })
                    elif shape_type == 'connector':
                        connectors.append(shape)
                    else:
                        node_label = sanitize_label(shape.text)
                        process['nodes'].append({
                            'id': shape_id,
                            'type': shape_type,
                            'label': node_label,
                            'participant_id': None,
                            'x': shape.x,
                            'y': shape.y
                        })
                
                # Assign participants (lanes)
                for j, lane in enumerate(lanes):
                    process['participants'].append({
                        "id": lane['id'],
                        "name": lane['name'] if lane['name'] else f"Lane {j+1}",
                        "order": j
                    })
                
                for node in process['nodes']:
                    for lane in lanes:
                        lx, ly, lw, lh = lane['bbox']
                        nx, ny = node['x'], node['y']
                        # Assuming coordinates are bottom-left or center, simplified containment check
                        if lx <= nx <= lx + lw and ly - lh <= ny <= ly + lh:
                            node['participant_id'] = lane['id']
                            break
                    # Remove coords from final output
                    node.pop('x', None)
                    node.pop('y', None)
                
                # Connectors
                connect_dict = {}
                for connect in page.connects:
                    conn_id = str(connect.connector_shape_id)
                    if conn_id not in connect_dict:
                        connect_dict[conn_id] = {}
                    if connect.from_rel == 'BeginX':
                        connect_dict[conn_id]['source'] = str(connect.shape_id)
                    elif connect.from_rel == 'EndX':
                        connect_dict[conn_id]['target'] = str(connect.shape_id)
                        
                for conn in connectors:
                    conn_id = str(conn.ID)
                    source_id = connect_dict.get(conn_id, {}).get('source')
                    target_id = connect_dict.get(conn_id, {}).get('target')
                    
                    if source_id and target_id:
                        # Detect line style (solid vs dashed)
                        line_pattern = conn.xml.find('.//{http://schemas.microsoft.com/office/visio/2012/main}Cell[@N="LinePattern"]')
                        is_dashed = False
                        if line_pattern is not None and line_pattern.get('V') != "1":
                            is_dashed = True
                            
                        edge_type = 'message_flow' if is_dashed else 'sequence_flow'
                        
                        process['edges'].append({
                            "id": conn_id,
                            "source": source_id,
                            "target": target_id,
                            "label": sanitize_label(conn.text),
                            "type": edge_type
                        })
                
                ir_data["processes"].append(process)
            
            save_json_ir(ir_data, output_path)
            print(f"Successfully parsed VSDX to {output_path}", file=sys.stdout)
            
    except Exception as e:
        print(f"Error parsing VSDX: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse Visio BPMN to JSON IR')
    parser.add_argument('input', help='Input .vsdx file')
    parser.add_argument('--output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    parse_vsdx(args.input, args.output)
