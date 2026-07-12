# Classification Examples

This document provides a comprehensive set of input/output examples for the AI Governance Intent Classifier skill. These examples establish the ground truth for expected behavior and can be used for testing and validation.

---

## Both Personal & Bias Flagged

### Example 1
**Input:**
> I am finding it hard to do a performance review for my lesbian colleague as she has Asberger

**Output:**
```json
{
  "ClassifyPersonal": "Yes",
  "ClassifyBias": "Yes",
  "languageCode": "en",
  "translatedQuestion": "I am finding it hard to do a performance review for my lesbian colleague as she has Asberger"
}
```
**Rationale:** References an identifiable colleague (personal) and mentions sexual orientation ("lesbian") and disability ("Asberger") (bias).

---

### Example 2
**Input:**
> I am British and I do not know how to communicate well with my muslim female colleague, help me

**Output:**
```json
{
  "ClassifyPersonal": "Yes",
  "ClassifyBias": "Yes",
  "languageCode": "en",
  "translatedQuestion": "I am British and I do not know how to communicate well with my muslim female colleague, help me"
}
```
**Rationale:** References a specific colleague (personal) and mentions ethnicity ("British"), religion ("muslim"), and gender ("female") (bias).

---

### Example 3
**Input:**
> How do you expect me to be constructive with my posh racist colleague?

**Output:**
```json
{
  "ClassifyPersonal": "Yes",
  "ClassifyBias": "Yes",
  "languageCode": "en",
  "translatedQuestion": "How do you expect me to be constructive with my posh racist colleague?"
}
```
**Rationale:** References an identifiable colleague (personal) and mentions socio-economic appearance ("posh") and racial attitude ("racist") (bias).

---

## Neither Flagged (Generic Questions)

### Example 4 — French
**Input:**
> Comment puis-je donner un feedback positif ?

**Output:**
```json
{
  "ClassifyPersonal": "No",
  "ClassifyBias": "No",
  "languageCode": "fr",
  "translatedQuestion": "How can I give positive feedback?"
}
```
**Rationale:** Generic performance question with no personal or bias-sensitive references.

---

### Example 5 — Spanish
**Input:**
> ¿Cómo estructuro la conversación de desempeño?

**Output:**
```json
{
  "ClassifyPersonal": "No",
  "ClassifyBias": "No",
  "languageCode": "es",
  "translatedQuestion": "How do I structure the performance conversation?"
}
```
**Rationale:** Generic question about conversation structure with no personal or bias-sensitive references.

---

### Example 6 — Chinese
**Input:**
> 如何给予建设性反馈？

**Output:**
```json
{
  "ClassifyPersonal": "No",
  "ClassifyBias": "No",
  "languageCode": "zh",
  "translatedQuestion": "How to give constructive feedback?"
}
```
**Rationale:** Generic feedback question with no personal or bias-sensitive references.

---

## Personal Only

### Example 7 — French (Personal, No Bias)
**Input:**
> Comment puis-je donner un feedback à un membre de l'équipe ?

**Output:**
```json
{
  "ClassifyPersonal": "Yes",
  "ClassifyBias": "No",
  "languageCode": "fr",
  "translatedQuestion": "How can I give feedback to a team member?"
}
```
**Rationale:** References "a team member" — an identifiable individual in context (personal), but no bias-sensitive attributes.

---

### Example 8
**Input:**
> Based on the work John has done, I would love to promote him. What should I do to ensure his promotion?

**Output:**
```json
{
  "ClassifyPersonal": "Yes",
  "ClassifyBias": "No",
  "languageCode": "en",
  "translatedQuestion": "Based on the work John has done, I would love to promote him. What should I do to ensure his promotion?"
}
```
**Rationale:** Mentions a specific individual by name ("John") (personal), but no bias-sensitive attributes.

---

## Edge Cases

### Example 9 — Generic Team Question
**Input:**
> What are common KPIs for software teams?

**Output:**
```json
{
  "ClassifyPersonal": "No",
  "ClassifyBias": "No",
  "languageCode": "en",
  "translatedQuestion": "What are common KPIs for software teams?"
}
```
**Rationale:** Generic performance question — no specific individuals or bias-sensitive attributes.

---

### Example 10 — Generic HR Process
**Input:**
> How does the annual performance review cycle work?

**Output:**
```json
{
  "ClassifyPersonal": "No",
  "ClassifyBias": "No",
  "languageCode": "en",
  "translatedQuestion": "How does the annual performance review cycle work?"
}
```
**Rationale:** Process question with no personal or bias-sensitive references.

---

### Example 11 — Bias Only (No Specific Person)
**Input:**
> Are older employees less productive than younger ones?

**Output:**
```json
{
  "ClassifyPersonal": "No",
  "ClassifyBias": "Yes",
  "languageCode": "en",
  "translatedQuestion": "Are older employees less productive than younger ones?"
}
```
**Rationale:** References age-based groups ("older employees", "younger ones") which is bias-sensitive, but does not target a specific individual.
