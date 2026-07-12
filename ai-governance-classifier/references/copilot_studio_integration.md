# Integration Guide — Copilot Studio

This document describes how to integrate the **AI Governance Intent Classifier** skill into a Microsoft Copilot Studio agent.

---

## Architecture Overview

```
User Query
    │
    ▼
┌──────────────────────────┐
│  Copilot Studio Agent    │
│                          │
│  ┌────────────────────┐  │
│  │ Governance Skill   │  │  ◄── Runs FIRST on every query
│  │ (This Classifier)  │  │
│  └────────┬───────────┘  │
│           │              │
│    Classification JSON   │
│    {Personal, Bias,      │
│     lang, translation}   │
│           │              │
│  ┌────────▼───────────┐  │
│  │ Policy Enforcer    │  │  ◄── Decides: block / warn / allow
│  └────────┬───────────┘  │
│           │              │
│  ┌────────▼───────────┐  │
│  │ Agent Core Logic   │  │  ◄── Primary topic / plugin handling
│  └────────────────────┘  │
└──────────────────────────┘
```

---

## Integration Steps

### 1. Create a Before-Topic Trigger

In Copilot Studio, create a **"Before Conversation Start"** or **"On Every Turn"** trigger topic that invokes this classification skill before any other topic routing.

### 2. Call the Classifier

Pass the user's raw message (`Activity.Text`) as the `ConversationQuery QueryText` input to the skill's prompt.

### 3. Parse the Response

The classifier returns a JSON object:

```json
{
  "ClassifyPersonal": "Yes" or "No",
  "ClassifyBias": "Yes" or "No",
  "languageCode": "en",
  "translatedQuestion": "..."
}
```

Parse this into Copilot Studio variables for downstream use.

### 4. Apply Policy Rules

Use **Condition** nodes to branch based on the classification:

| Condition | Recommended Action |
|---|---|
| `ClassifyPersonal == "Yes"` AND `ClassifyBias == "Yes"` | Redirect to a sensitive-content topic. Add a privacy + bias disclaimer. Log the event for compliance review. |
| `ClassifyPersonal == "Yes"` | Remind the user of data privacy policies. Optionally redact PII before processing. |
| `ClassifyBias == "Yes"` | Add an inclusivity disclaimer. Flag for human review if severity is high. |
| Both `"No"` | Proceed normally to the agent's core logic. |

### 5. Use the Translation

If `languageCode` is not `"en"`, use `translatedQuestion` for downstream English-only processing while preserving the original language for the user-facing response.

---

## Logging & Audit

For compliance, log every classification result alongside:

- Timestamp
- Session / Conversation ID
- Original query (hashed or anonymized if PII is detected)
- Classification result
- Action taken

This creates an audit trail for governance reviews.

---

## Testing

Use the examples in [classification_examples.md](file:///c:/Users/bmadhuso/Documents/Bala/Anti%20Gravity/Skills/skills-intend-classify/.agents/skills/ai-governance-classifier/examples/classification_examples.md) to validate the classifier's behavior in your Copilot Studio environment.
