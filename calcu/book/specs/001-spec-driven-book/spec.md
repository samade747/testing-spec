# Spec: Spec-Driven AI Book + Embedded RAG Chatbot

## ID
001

## Title
Spec-Driven AI Book (Docusaurus) with Embedded RAG Chatbot (FastAPI + Qdrant + OpenAI/ChatKit)

## Overview
Build a Docusaurus-based technical book that teaches Spec-Driven AI development using Spec-Kit Plus and Claude Code (optional). The book will be deployed to GitHub Pages. An embedded Retrieval-Augmented Generation (RAG) chatbot will answer questions about the book content. The chatbot must support two modes:
- **Global retrieval**: search across the entire indexed book in Qdrant.
- **Selection-only (strict)**: when the user highlights text and asks a question, the answer MUST be derived **only** from the selected text; if it's not present, the assistant must reply exactly:  
  `I don't know from the provided text.`

## Goals
- Provide a tutorial-first, reproducible book with runnable examples and code.
- Demonstrate an end-to-end RAG pipeline: markdown → chunk → embeddings → Qdrant → FastAPI query → Chat UI.
- Deliver code, docs, CI/CD, and tests so reviewers can reproduce and deploy the project.

## Audience
Developers and technical authors learning spec-driven development and RAG engineering.

## Scope (what we will deliver)
- Docusaurus book under `book/` with at least:
  - `intro.md`, 6 core chapters, and a `rag-chatbot/` section.
- FastAPI backend under `backend/`:
  - `POST /ingest` (optional trigger)
  - `POST /query` { question, selectionText?, top_k? }
- Ingest script `backend/ingest.py` that:
  - Reads `book/docs/*.md`, splits into chunks, computes embeddings, upserts into Qdrant Cloud.
- React chat widget `book/src/components/ChatWidget.jsx` and `SelectedTextHelper.jsx`.
- GitHub Actions workflow to build + deploy Docusaurus to GitHub Pages.
- `.env.example`, Dockerfile, README_DEPLOY.md, basic tests.
- Checklist and specification artifacts.

## Functional requirements (priority order)
1. Book builds locally and deploys to GitHub Pages.
2. `POST /query` accepts `{ question, selectionText? }` and returns `{ answer, contexts[] }`.
3. If `selectionText` exists:
   - Backend uses it **as the only context** (strict mode) unless a fallback policy is explicitly enabled.
   - If answer not present in selection, return exactly: `I don't know from the provided text.`
4. Ingest script supports batching and configurable chunk size/overlap.
5. Chat UI can:
   - Capture highlighted text on page (`window.getSelection()`).
   - Send `selectionText` with the question.
   - Display the answer and the retrieved context summary.
6. Qdrant collection named `calcu_book` with payloads `{ source, chunk_index, text }`.
7. Use OpenAI embeddings (or Anthropic/Claude embeddings if chosen) and a suitable chat model available on account.

## Non-functional requirements
- Secrets must not be committed. Use `.env` and GitHub Secrets.
- Ingestion performance: reasonable for a small book (indexing completes in < 5 minutes).
- Query latency: under ~3s for typical requests on free-tier hosting.
- Code must be readable, commented, and include small tests for core flows.

## Acceptance criteria (explicit)
- `book` builds (`cd book && npm ci && npm run build`) and preview runs (`npm start`).
- The ingest script runs and uploads points into Qdrant Cloud.
- `POST /query` returns sensible answers for book queries.
- Selection-only mode returns direct answers from the selection; if not present, returns exact refusal string.
- GitHub Actions successfully deploys `book/` to GitHub Pages.
- README_DEPLOY.md contains complete deploy instructions.

## Edge cases & decisions
- Short selections (< ~15 words): recommended behavior — treat selection as strict context; if too short to answer, return refusal; optionally show a UX hint recommending selecting a larger passage.
- Large selections: limit selection size (e.g., 8k tokens) before truncation; document size limits in the book.
- Model fallback: if ChatKit/selected model not available, use an alternate model defined in `.env`.

## Deliverables
- `specs/001-spec-driven-book/spec.md` (this file)
- `plan.md`, `tasks.md`, `checklist.md`
- `book/` (Docusaurus site)
- `backend/` (FastAPI, ingest)
- `README_DEPLOY.md`, `.env.example`, Dockerfile
- Basic tests & CI

## Out-of-scope
- Production-grade scaling optimizations
- SSO / authentication for chat widget
- Multi-language support (English only)

## Notes & references
- Use Qdrant Cloud free tier for vector store.
- Use OpenAI ChatKit or Chat completions for inference; provide Claude variant as an optional adapter.

---
