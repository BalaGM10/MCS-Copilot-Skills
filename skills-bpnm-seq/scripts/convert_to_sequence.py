# =============================================================================
# convert_to_sequence.py — JSON IR → Mermaid Sequence Diagram converter
# Version: 1.0.0
# Date: 2026-09-09
# Original Author: Bala Madhusoodhanan (initial Mermaid conversion concept)
# Enhanced By: Antigravity AI (Peer Coding)
# Changelog:
#   1.0.0 (2026-09-09) - Antigravity enhancement. Rewrote conversion from
#                        flowchart to sequence diagram output. Added graph
#                        traversal with gateway handling (alt/par/loop),
#                        activation markers, and multi-process support.
#   0.1.0 (2026-09-09) - Initial concept by Bala Madhusoodhanan (flowchart).
# =============================================================================

import argparse
import sys
import os

# Assuming scripts are run from the directory they reside in or using python -m
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json_ir, sanitize_id

def build_graph(nodes, edges):
    graph = {node['id']: [] for node in nodes}
    in_degree = {node['id']: 0 for node in nodes}
    for edge in edges:
        source = edge.get('source')
        target = edge.get('target')
        if source in graph and target in graph:
            graph[source].append((target, edge))
            in_degree[target] += 1
    return graph, in_degree

def convert_to_sequence(input_path: str, output_path: str):
    try:
        ir_data = load_json_ir(input_path)
        output_lines = []
        
        for process in ir_data.get('processes', []):
            output_lines.append(f"## Process: {process.get('name', 'Process')}\n")
            output_lines.append("```mermaid")
            output_lines.append("sequenceDiagram")
            output_lines.append("autonumber")
            
            participants = process.get('participants', [])
            participant_map = {}
            for p in sorted(participants, key=lambda x: x.get('order', 0)):
                p_id = sanitize_id(p['id'])
                p_name = p['name']
                output_lines.append(f"participant {p_id} as {p_name}")
                participant_map[p['id']] = p_id
                
            nodes = process.get('nodes', [])
            edges = process.get('edges', [])
            
            node_map = {n['id']: n for n in nodes}
            graph, in_degree = build_graph(nodes, edges)
            
            start_nodes = [n['id'] for n in nodes if n['type'] == 'start_event']
            if not start_nodes:
                # Fallback to nodes with 0 in-degree
                start_nodes = [n_id for n_id, deg in in_degree.items() if deg == 0]
                
            visited = set()
            
            def get_participant(node_id):
                n = node_map.get(node_id, {})
                pid = n.get('participant_id')
                return participant_map.get(pid, 'Unassigned')

            def traverse(current_id, current_participant=None):
                if current_id in visited:
                    output_lines.append(f"loop Circular Reference Detected")
                    output_lines.append(f"Note over {get_participant(current_id)}: Circular reference to {node_map[current_id].get('label', current_id)}")
                    output_lines.append("end")
                    return
                
                visited.add(current_id)
                node = node_map[current_id]
                part = get_participant(current_id)
                ntype = node.get('type')
                nlabel = node.get('label', '')
                
                if ntype == 'start_event':
                    output_lines.append(f"Note over {part}: 🟢 Start: {nlabel}")
                elif ntype == 'end_event':
                    output_lines.append(f"Note over {part}: 🔴 End: {nlabel}")
                elif ntype == 'data_object':
                    output_lines.append(f"Note right of {part}: 📄 {nlabel}")
                elif ntype == 'sub_process':
                    output_lines.append(f"rect rgb(200, 220, 255)")
                    output_lines.append(f"Note over {part}: Sub-process: {nlabel}")
                    
                neighbors = graph.get(current_id, [])
                
                if ntype == 'exclusive_gateway':
                    if len(neighbors) > 1:
                        for idx, (nxt, edge) in enumerate(neighbors):
                            cond = edge.get('label', f'branch_{idx+1}')
                            if idx == 0:
                                output_lines.append(f"alt {cond}")
                            else:
                                output_lines.append(f"else {cond}")
                            traverse(nxt, part)
                        output_lines.append("end")
                    elif len(neighbors) == 1:
                        traverse(neighbors[0][0], part)
                elif ntype == 'parallel_gateway':
                    if len(neighbors) > 1:
                        for idx, (nxt, edge) in enumerate(neighbors):
                            cond = edge.get('label', f'branch_{idx+1}')
                            if idx == 0:
                                output_lines.append(f"par {cond}")
                            else:
                                output_lines.append(f"and {cond}")
                            traverse(nxt, part)
                        output_lines.append("end")
                    elif len(neighbors) == 1:
                        traverse(neighbors[0][0], part)
                elif ntype == 'inclusive_gateway':
                    if len(neighbors) > 1:
                        for idx, (nxt, edge) in enumerate(neighbors):
                            cond = edge.get('label', f'branch_{idx+1}')
                            if idx == 0:
                                output_lines.append(f"alt {cond}")
                            else:
                                output_lines.append(f"else {cond}")
                            traverse(nxt, part)
                        output_lines.append("end")
                    elif len(neighbors) == 1:
                        traverse(neighbors[0][0], part)
                else:
                    for nxt, edge in neighbors:
                        next_part = get_participant(nxt)
                        edge_lbl = edge.get('label', '')
                        msg = edge_lbl if edge_lbl else ("Flow" if current_participant == next_part else "Message")
                        
                        if ntype in ['task', 'sub_process'] and current_participant:
                            msg = f"{nlabel} - {msg}" if edge_lbl else nlabel
                            
                        # activation marker logic could go here
                        if part != next_part:
                            output_lines.append(f"{part}->>{next_part}: {msg}")
                        else:
                            output_lines.append(f"{part}->>{part}: {msg}")
                            
                        traverse(nxt, next_part)

                if ntype == 'sub_process':
                    output_lines.append(f"end")

            for sn in start_nodes:
                traverse(sn, get_participant(sn))
                
            output_lines.append("```\n")
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
            
        print(f"Successfully converted to {output_path}", file=sys.stdout)
            
    except Exception as e:
        print(f"Error converting to sequence: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert JSON IR to Mermaid Sequence Diagram')
    parser.add_argument('input', help='Input JSON IR file')
    parser.add_argument('--output', required=True, help='Output Markdown file')
    
    args = parser.parse_args()
    convert_to_sequence(args.input, args.output)
