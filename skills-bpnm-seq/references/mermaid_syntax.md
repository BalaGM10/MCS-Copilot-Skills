<!-- ==========================================================================
  mermaid_syntax.md — Mermaid Sequence Diagram Syntax Reference
  Version: 1.0.0 | Date: 2026-09-09
  Original Author: Bala Madhusoodhanan | Enhanced By: Antigravity AI (Peer Coding)
  Changelog:
    1.0.0 (2026-09-09) - Created by Antigravity during peer coding enhancement.
========================================================================== -->

# Mermaid Sequence Diagram Syntax

## Overview
This document covers the syntax for Mermaid sequence diagrams, specifically tailored for translating BPMN processes.

## Diagram Declaration
Every sequence diagram begins with the `sequenceDiagram` declaration. 
Optionally, use `autonumber` to automatically number the message flows.

```mermaid
sequenceDiagram
    autonumber
    Alice->>Bob: Hello
```

## Participants & Actors
Participants define the distinct entities (swimlanes/systems). They are displayed left-to-right in the order they are declared.

- **Standard Participant**: `participant <id> [as <alias>]`
- **Actor (stick figure)**: `actor <id> [as <alias>]`
- **Grouping (Pools)**: `box [color] [Title] ... end`

### Dynamic Lifelines
You can dynamically create and destroy participants mid-flow:
- `create participant <id>`
- `destroy <id>`

### Example
```mermaid
sequenceDiagram
    box rgb(240, 240, 240) Customer Pool
        actor C as Customer
    end
    box rgb(200, 220, 240) System Pool
        participant UI as Frontend
        participant DB as Database
    end
    
    C->>UI: Request Data
    create participant Temp as CacheWorker
    UI->>Temp: Init worker
    destroy Temp
    Temp-->>UI: Done
```

## Message Arrow Types

| Syntax | Description | BPMN Use |
|--------|-------------|----------|
| `A->>B: msg` | Solid line, solid arrowhead | Synchronous call / sequence flow crossing lanes |
| `A-->>B: msg` | Dashed line, open arrowhead | Response / reply |
| `A-)B: msg` | Solid line, open half-arrow | Async message flow (cross-pool) |
| `A--)B: msg` | Dashed line, open half-arrow | Async notification |
| `A-xB: msg` | Solid with cross | Lost message / error |
| `A--xB: msg` | Dashed with cross | Failed return |

## Activations
Show when a participant is actively processing a task.
- Explicit: `activate <participant>` / `deactivate <participant>`
- Shorthand: Append `+` to the arrow to activate, and `-` to deactivate.

```mermaid
sequenceDiagram
    Alice->>+Bob: Do work
    Bob-->>-Alice: Done
```

## Control Flow Blocks
Used to represent BPMN Gateways and Loops.

### XOR Gateway (Exclusive)
```mermaid
sequenceDiagram
    alt is valid
        A->>B: Process
    else is invalid
        A->>C: Reject
    end
```

### AND Gateway (Parallel)
```mermaid
sequenceDiagram
    par Fetch Data
        A->>DB: Query 1
    and Fetch Auth
        A->>Auth: Query 2
    end
```

### Loop & Optional
```mermaid
sequenceDiagram
    loop Every 5 mins
        A->>B: Ping
    end
    
    opt If detailed
        A->>B: Send extra data
    end
```

### Error / Break
```mermaid
sequenceDiagram
    critical Save Data
        A->>DB: Write
    option DB Down
        A->>Cache: Save fallback
    end
    
    break On timeout
        A->>A: Abort
    end
```

## Notes
Add context to the diagram.
- `Note left of <participant>: text`
- `Note right of <participant>: text`
- `Note over <participant>: text`
- `Note over <p1>,<p2>: text`

## Styling
Highlight areas with background colors.
- `rect rgb(r,g,b)` ... `end`
- `rect rgba(r,g,b,a)` ... `end`

```mermaid
sequenceDiagram
    rect rgb(200, 255, 200)
        A->>B: Safe operation
    end
```
