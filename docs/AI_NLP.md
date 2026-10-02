# AI and NLP

Resume text is extracted with PyMuPDF and python-docx, normalized, and matched against a controlled taxonomy with aliases. Canonical skills are deduplicated and confidence is higher when the canonical phrase appears directly.

Matching is explainable: required skills are compared case-insensitively, weighted scoring uses job importance, and gap priority is derived from configured importance (`High` >= 8, `Medium` >= 5, otherwise `Low`). Semantic matching is modular and constrained to known skills. Install `sentence-transformers` and configure a model in deployment to enable embeddings; the deterministic fallback keeps local development reliable.
