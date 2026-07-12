# AI Governance Policy Reference

This document outlines the governance principles that underpin the AI Governance Intent Classifier skill.

---

## Core Principles

### 1. Privacy & Confidentiality

All user interactions with AI agents must protect personally identifiable information (PII). The classifier flags queries that reference, request, or reveal:

- **Direct identifiers**: Full names, employee IDs, email addresses, phone numbers, physical addresses
- **Indirect identifiers**: Job titles tied to a single person, team references that narrow to an individual, approver/reviewer chains
- **Contextual identifiers**: "My colleague", "my manager" when the organizational context makes the person identifiable

**Policy action**: When personal information is detected, the agent must not store, repeat, or surface PII in its response unless the user has explicit authorization. Responses should be generalized.

---

### 2. Bias-Free Communication

AI agents must not reinforce, perpetuate, or amplify bias related to protected characteristics. The classifier flags queries that involve:

| Protected Category | Examples |
|---|---|
| Ethnicity / Race / Nationality | British, Asian, African-American |
| Gender / Gender Identity | Female, non-binary, transgender |
| Religion / Belief | Muslim, Christian, atheist |
| Age | Older, millennial, Gen Z |
| Disability | Asperger's, ADHD, wheelchair user |
| Sexual Orientation | Lesbian, gay, bisexual |
| Physical Appearance | Posh, overweight, tall |
| Socio-Economic Status | Working class, privileged |
| Political Views | Conservative, liberal |

**Policy action**: When bias-sensitive content is detected, the agent must:
1. Respond neutrally without reinforcing stereotypes
2. Avoid making assumptions based on protected characteristics
3. Offer inclusive, evidence-based guidance

---

### 3. Transparency & Accountability

- Every classification decision must be explainable
- Classification results should be logged for audit purposes
- False positives are preferred over false negatives (err on the side of caution)

---

## Classification Decision Matrix

| Personal? | Bias? | Risk Level | Recommended Action |
|---|---|---|---|
| No | No | Low | Process normally |
| Yes | No | Medium | Apply PII safeguards; generalize response |
| No | Yes | Medium | Apply inclusivity guardrails; flag for review |
| Yes | Yes | High | Apply both safeguards; escalate to human review if needed |

---

## Regulatory Alignment

This classifier supports compliance with:

- **GDPR** (EU) — Data minimization, purpose limitation
- **UK Data Protection Act 2018** — PII handling
- **EU AI Act** — High-risk AI system transparency requirements
- **Corporate AI Ethics Policies** — Internal standards for responsible AI use
