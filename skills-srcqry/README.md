# 📦 query-enhancer — Skill Package

> A RAG preprocessing skill that transforms raw user queries into optimised search inputs,
> improving retrieval accuracy from vector and keyword knowledge sources.
>
> **This is a markdown-only skill** — no Python scripts or external dependencies required.
> It provides prompt templates, examples, and reference docs for use with any LLM integration.

---

## 📁 Package Contents

```text
query-enhancer/
├── SKILL.md                         ← Main skill: prompts, examples, pipeline, config
├── README.md                        ← You are here
├── references/
│   ├── prompt_template.md           ← Standalone LLM prompt templates
│   └── intent_categories.md         ← Intent classification taxonomy & routing
└── examples/
    └── sample_queries.json          ← Example input/output pairs for testing
```

---

## ⚡ How to Use

### 1. Read the Skill

Open [SKILL.md](SKILL.md) — it contains everything you need:
- The **LLM prompt templates** (base + with intent classification)
- **Pipeline architecture** diagram
- **5 worked examples** across all intent categories
- **Configuration recommendations** (model, temperature, caching)
- **Customisation guide** (adding intents, domain terminology)

### 2. Copy the Prompt

Copy the prompt template from SKILL.md into your LLM integration — whether that's:
- A direct API call (OpenAI, Gemini, Anthropic, etc.)
- A LangChain / LlamaIndex chain
- A custom RAG pipeline
- An agent skill configuration

### 3. Replace the Placeholder

Replace `{{USER_QUERY}}` with the actual user input and send to your LLM.

### 4. Parse the JSON Output

The LLM returns structured JSON:

```json
{
  "optimised_query": "rewritten search-ready query",
  "keywords": ["keyword1", "keyword2", "..."],
  "intent": "troubleshooting"
}
```

Feed `optimised_query` to your vector search and `keywords` to your metadata/BM25 filter.

---

## 📤 Quick Example

**User says:**
```
how do i fix the thing when my account gets locked out
```

**Skill produces:**
```json
{
  "optimised_query": "account lockout resolution steps user authentication failure",
  "keywords": [
    "account lockout", "locked out", "authentication failure",
    "password reset", "access denied", "user account",
    "login error", "unlock account"
  ],
  "intent": "troubleshooting"
}
```

---

## 📚 Reference Files

| File | Purpose |
|------|---------|
| [prompt_template.md](references/prompt_template.md) | Standalone prompt templates with customisation guide |
| [intent_categories.md](references/intent_categories.md) | Intent taxonomy, detection signals, and routing logic |
| [sample_queries.json](examples/sample_queries.json) | 6 example input/output pairs across all 5 intents |

---

## 📝 Version

| Version | Date       | Notes           |
|---------|------------|-----------------|
| 1.0.0   | 2026-07-10 | Initial release (markdown-only) |
