# Implementation Plan
Project: Spec-Driven AI Book + RAG Chatbot  
Spec ID: 001

## Summary
This plan breaks work into milestones with clear deliverables, artifacts, and owners. Timeline estimates assume a single developer working full-time; adjust as needed.

## Milestones & timeline (recommended)
- **M1: Project init & constitution** (0.5 day)
  - Create repo structure, add constitution.md, initial spec
- **M2: Docusaurus skeleton & core docs** (1–2 days)
  - Initialize Docusaurus, add base pages and sidebar
- **M3: Backend skeleton & ingest** (2–4 days)
  - FastAPI skeleton, ingest.py, requirements
- **M4: Embeddings & Qdrant integration** (1–2 days)
  - Implement embedding calls, upsert to Qdrant, test vector retrieval
- **M5: Chat UI & selection flow** (1–2 days)
  - ChatWidget component, selection helper, wiring to backend
- **M6: CI & deploy** (1 day)
  - GitHub Actions for Docusaurus, README deploy steps
- **M7: Tests, polish & docs** (1–2 days)
  - Add smoke tests, checklist, finalize docs

Estimated total: 7–12 working days (MVP in ~1 week, full deliverable in ~2 weeks).

## Architecture (textual)
- **Frontend (book/)**: Docusaurus + React components.
  - MDX docs + inline ChatWidget.
- **Backend (backend/)**: FastAPI app
  - Endpoints: `POST /ingest`, `POST /query`
  - Uses OpenAI for embeddings & chat (or Anthropic for Claude variant)
  - Uses Qdrant Cloud for vector storage
- **Data flow**
  1. `book/docs/*.md` → `ingest.py` → text chunks → embeddings → Qdrant `calcu_book`
  2. Client (ChatWidget) → `/query` { question, selectionText? }
  3. Backend:
     - If selectionText: use selection as context (strict) → call model
     - Else: embed question → query Qdrant → assemble contexts → call model
  4. Model returns answer → backend returns `{ answer, contexts }` → UI displays answer

## Folder layout (recommended)
