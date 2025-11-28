# Deployment Instructions

This document outlines the steps to deploy the Spec-Driven AI Book (Docusaurus frontend) and the RAG Chatbot (FastAPI backend).

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
- GitHub Secrets used for CI: `OPENAI_API_KEY`, `QDRANT_API_KEY`, `QDRANT_URL`
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
- Manual test for selection-only mode: pass exact sentence as `selectionText` and verify direct answer and negative case

## Deliverables per milestone
- M1: constitution.md (done), basic README
- M2: Docusaurus skeleton & docs pages
- M3: backend skeleton + ingest
- M4: Qdrant upsert + retrieval code
- M5: ChatWidget + selection flow wiring
- M6: CI + deploy config
- M7: Tests, checklist, PR ready

---

## Frontend Deployment (Docusaurus to GitHub Pages)

The Docusaurus site is deployed to GitHub Pages using GitHub Actions.

1.  **Prerequisites**:
    *   Ensure all Node.js dependencies are installed (`cd book && npm install`). **(Currently blocked due to network issues)**
    *   Ensure the Docusaurus site builds successfully locally (`cd book && npm run build`). **(Currently blocked due to missing dependencies)**
    *   Your GitHub repository must have GitHub Pages enabled.

2.  **Workflow**:
    *   The deployment is automated via the GitHub Actions workflow located at `.github/workflows/deploy.yml`.
    *   This workflow is triggered on `push` to the `main` branch.
    *   It checks out the code, installs Node.js dependencies in the `book/` directory, builds the Docusaurus site, and then uses `peaceiris/actions-gh-pages` to deploy the `book/build` directory to the `gh-pages` branch.

3.  **Configuration**:
    *   No specific secrets are needed for Docusaurus deployment itself beyond the default `GITHUB_TOKEN`.
    *   Ensure `baseUrl` in `book/docusaurus.config.js` is correctly configured for your GitHub Pages URL (e.g., if deploying to `https://<USERNAME>.github.io/<REPO_NAME>/`, set `baseUrl: '/<REPO_NAME>/'`).

---

## Backend Deployment (FastAPI)

The FastAPI backend can be deployed to various cloud providers. This section provides general guidelines.

1.  **Prerequisites**:
    *   Ensure all Python dependencies are installed (`cd backend && pip install -r requirements.txt`). **(Currently blocked due to Rust/Cargo dependency)**
    *   Ensure Docker is installed and running if deploying via Docker. **(Currently blocked as Docker is not found)**
    *   Environment variables (`OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`) must be configured in your deployment environment. Refer to `backend/.env.example`.

2.  **Deployment Options**:

    *   **Docker (Recommended for portability)**:
        *   Build the Docker image: `docker build -t calcu-backend backend/` **(Currently blocked as Docker is not found)**
        *   Run the container: `docker run -p 8000:8000 --env-file backend/.env calcu-backend` (replace `.env` with actual secret management for production)
        *   Deploy the built image to a container-hosting service (e.g., Google Cloud Run, AWS ECS, Azure Container Instances, Render).

    *   **Direct Python Execution (e.g., on a VM or PaaS)**:
        *   Set up a Python environment (e.g., `venv`).
        *   Install dependencies: `pip install -r backend/requirements.txt`.
        *   Run the Uvicorn server: `uvicorn app:app --host 0.0.0.0 --port 8000`.
        *   Ensure a process manager (e.g., Gunicorn, systemd) is used for production.

3.  **Environment Variables**:
    *   For production, **do not commit sensitive information like API keys**.
    *   Instead, configure these as environment variables directly in your deployment platform's settings.
    *   Refer to `backend/.env.example` for a list of required variables.

---