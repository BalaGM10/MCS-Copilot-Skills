<!-- ==========================================================================
  vsdx_format.md — VSDX File Format Reference
  Version: 1.0.0 | Date: 2026-09-09
  Original Author: Bala Madhusoodhanan | Enhanced By: Antigravity AI (Peer Coding)
  Changelog:
    1.0.0 (2026-09-09) - Created by Antigravity during peer coding enhancement.
========================================================================== -->

# VSDX Format Reference

## Overview
A `.vsdx` file (Visio Drawing) is an Office Open XML (OPC) package. It is essentially a ZIP archive containing various XML files and media assets. You can rename a `.vsdx` file to `.zip` and extract it to view the internal structure.

## Directory Structure
When extracted, the contents generally follow this structure:

```
[Content_Types].xml       # Defines MIME types for file extensions and parts
_rels/                    # Package-level relationships
visio/                    # Main folder for Visio content
├── document.xml          # Root document file
├── pages/                # Contains individual page XML files
│   ├── page1.xml         # XML definition of Page 1
│   ├── page2.xml         # XML definition of Page 2
│   └── _rels/            # Relationships for pages (e.g., masters used)
├── masters/              # Contains master shapes (stencils)
│   ├── master1.xml
│   └── _rels/
└── _rels/                # Document-level relationships
```

## Key XML Elements
Within `visio/pages/pageN.xml`, the document uses a structured XML schema:

- `<Page>`: Root element representing the drawing canvas.
- `<Shape>`: Represents an individual element on the canvas (e.g., Task, Gateway, Connector).
- `<Shapes>`: A collection of child shapes, either on the page or nested within another shape (like a Pool containing Lanes).
- `<Connect>`: Maps connections between 1D (connectors) and 2D (nodes) shapes.
- `<Connects>`: A collection of `<Connect>` elements at the page level.
- `<Cell>`: Defines properties (like geometry, color, text) for a shape.
- `<Section>`: Groups similar cells, e.g., the `Character` section for text formatting or `LineFormat` for stroke details.

## Shape Properties
Common attributes for `<Shape>` elements:
- `ID`: Unique integer identifier for the shape on the page.
- `NameU`: Universal (non-localized) name of the shape, e.g., `Task.12`.
- `Name`: Localized name of the shape.
- `Text`: Represents the inner text content of the shape, though actual text is often stored in child `<Text>` elements or mapped from data.
- `PinX`, `PinY`: The X and Y coordinates of the shape's center (pin) on the page.
- `Width`, `Height`: Dimensions of the shape bounding box.
- `Master`: References the ID of a Master shape in the `masters/` directory, linking it to its stencil definition.

## Connectors and Connectivity
Connections are stored in the `<Connects>` element on the page.
A `<Connect>` element typically looks like this:
```xml
<Connect FromSheet="3" FromCell="BeginX" ToSheet="1" ToPart="3"/>
<Connect FromSheet="3" FromCell="EndX" ToSheet="2" ToPart="1"/>
```
- `FromSheet`: The ID of the 1D connector shape.
- `ToSheet`: The ID of the 2D target node shape.
- `FromCell`: Indicates if it's the start (`BeginX`) or end (`EndX`) of the connector.

## Swimlanes and Pools
In Visio, Swimlanes and Pools are represented as container shapes.
- They act as structural groups. If a shape is inside a swimlane, it might be nested within a `<Shapes>` child of the lane shape, or logically linked.
- The `Master` name is often `FunctionBand` or `Swimlane`.
- Visio Cross-Functional Flowchart shapes manage spatial grouping tightly.

## Line Styles (Cell Values)
Line formatting is defined in `<Cell N="LinePattern">`, `<Cell N="LineColor">`, etc.
- `LinePattern`: 
  - `0` = None
  - `1` = Solid (Standard sequence flow)
  - `2-23` = Various dashed/dotted patterns (Commonly used for Message flows, e.g., dashed = pattern `2` or `3`).
- `LineWeight`: Thickness of the line.

## Common BPMN Visio Stencil Masters
The mapping of standard Visio BPMN master names to their logical elements:

- **Events:** `Start Event`, `End Event`, `Intermediate Event`
- **Activities:** `Task`, `Service Task`, `User Task`, `Script Task`, `Manual Task`
- **Gateways:** `Exclusive Gateway`, `Parallel Gateway`, `Inclusive Gateway`
- **Structural:** `Pool`, `Lane`, `Swimlane`, `FunctionBand`
- **Data/Artifacts:** `Data Object`, `Data Store`, `Message`
- **Connectors:** `Dynamic connector`, `Association`, `Sequence Flow`, `Message Flow`
