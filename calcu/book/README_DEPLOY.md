
## Tech stack & versions
- Node.js LTS (18/20)
- Docusaurus v3
- React 18
- Python 3.11+
- FastAPI, uvicorn
- Qdrant Cloud (free tier)
- OpenAI SDK (or Anthropic SDK for Claude)
- GitHub Actions for CI

## Security & secrets
- `.env` used locally (ignored by `.gitignore`)
- GitHub Secrets used for CI: OPENAI_API_KEY, QDRANT_API_KEY, QDRANT_URL
- Document secrets usage in README_DEPLOY.md

## Risk assessment & mitigations
- **Rate limits / cost**: batch embeddings, use smaller embedding model for dev.
- **Model availability**: support a model alias in `.env` to switch providers.
- **Short selection UX**: warn user; return refusal if insufficient context.
- **Qdrant connectivity**: test ingestion with small dataset first.

## Testing strategy
- Unit tests for ingest chunker
- Smoke test for `/query` (curl)
- Integration test: ingest → query → verify answer contains expected substring
- Manual test for selection-only mode: pass exact sentence as selectionText and verify direct answer and negative case

## Deliverables per milestone
- M1: constitution.md (done), basic README
- M2: Docusaurus skeleton & docs pages
- M3: backend skeleton + ingest
- M4: Qdrant upsert + retrieval code
- M5: ChatWidget + selection flow wiring
- M6: CI + deploy config
- M7: Tests, checklist, PR ready

---
