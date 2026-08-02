# Level 4 Process Documentation Guide

> **Location:** `references/level4-process-guide.md`
> This reference explains what a Level 4 process document is and how it fits into the process documentation hierarchy.

---

## Process Documentation Levels

Process documentation is typically organised into a hierarchy of increasing detail. The most common framework uses four levels:

| Level | Name | Purpose | Audience |
|---|---|---|---|
| **L1** | Process Landscape | High-level map of all enterprise processes | Executive / Strategic |
| **L2** | Process Map | End-to-end flow of a business process | Process Owners / Managers |
| **L3** | Standard Operating Procedure (SOP) | Step-level instructions for a process | Team Leads / Supervisors |
| **L4** | Detailed Work Instruction | Click-by-click system instructions | End Users / Operators |

---

## What is a Level 4 Document?

A **Level 4 (L4)** document — also called a **Detailed Work Instruction** or **Step-by-Step Procedure** — is the most granular form of process documentation. It tells the user:

- **Exactly** which screen to navigate to
- **Exactly** which button, field, or control to interact with
- **Exactly** what value to enter or select
- **Exactly** what the system should do in response

### Key Characteristics

| Characteristic | Description |
|---|---|
| **Granularity** | Individual clicks, keystrokes, and field entries |
| **System-specific** | Tied to a particular application (e.g., Dynamics 365) |
| **Screenshots** | Often includes annotated screenshots for each step |
| **Expected results** | Documents what the user should see after each action |
| **Audience** | End users performing the task day-to-day |

---

## L4 vs L3 — Key Differences

| Aspect | Level 3 (SOP) | Level 4 (Work Instruction) |
|---|---|---|
| **Focus** | *What* to do | *How* to do it in the system |
| **Detail** | Process steps and decisions | Screen-by-screen, field-by-field |
| **Screenshots** | Optional / overview only | Recommended for every step |
| **Expected results** | Per-process | Per-step |
| **Length** | 1–3 pages | 5–20+ pages |
| **Maintenance** | Updated on process change | Updated on system change |

---

## Standard L4 Document Structure

The AXTR to Markdown skill generates documents following this structure:

```
1. Purpose             — Why this process exists
2. Scope               — Who this document applies to
3. Prerequisites       — What must be in place before starting
4. Roles & Responsibilities — Who does what
5. Step-by-Step Procedure   — The detailed instructions (core of L4)
6. Expected Outcomes   — What success looks like
7. Troubleshooting     — Common issues and resolutions
8. Related Documents   — Links to L3 SOPs, system guides, etc.
9. Revision History    — Change log
```

---

## When to Create an L4 Document

Create an L4 document when:

- A process involves **complex system interactions** that new users cannot intuit
- The organisation is **onboarding new staff** to a system or process
- A process is being **standardised** across multiple teams or locations
- **Audit or compliance** requirements mandate detailed procedural documentation
- A **Dynamics 365 Task Recording** (AXTR) is available as a source

---

## Best Practices

1. **One L4 per process variant** — Don't combine multiple process paths into one document
2. **Keep screenshots current** — Re-record and regenerate when the system UI changes
3. **Use consistent terminology** — Match field labels and menu names exactly as they appear in the system
4. **Review regularly** — L4 documents go stale quickly; schedule quarterly reviews
5. **Link to L3** — Always reference the parent L3 SOP so users understand the broader context
6. **Version control** — Track changes in the Revision History table

---

## Further Reading

- [Microsoft Docs — Task Recorder](https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/user-interface/task-recorder)
- [APQC Process Classification Framework](https://www.apqc.org/process-frameworks)
- [ISO 9001 — Documented Information Requirements](https://www.iso.org/standard/62085.html)
