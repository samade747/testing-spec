# QA & Acceptance Checklist

Project: Spec-Driven AI Book + RAG Chatbot  
Use this checklist to verify the deliverable before merging.

---

## Local build (Frontend)
- [ ] **Install deps**
  - Command:
    ```
    cd book
    npm ci
    ```
  - Expected: `node_modules` installed successfully.

- [ ] **Run dev preview**
  - Command:
    ```
    npm start
    ```
  - Expected: Site served at `http://localhost:3000` with no critical errors.

- [ ] **Production build**
  - Command:
    ```
    npm run build
    ```
  - Expected: Build completes, `build/` folder created.

---

## Backend & ingestion
- [ ] **Install Python deps**
  - Command:
    ```
    cd backend
    python -m venv .venv
    .venv/bin/pip install -r requirements.txt
    ```
  - Expected: All packages installed.

- [ ] **Prepare .env**
  - Action: Copy `.env.example` → `.env`, populate:
    ```
    OPENAI_API_KEY=...
    QDRANT_URL=https://<cluster>.qdrant.cloud
    QDRANT_API_KEY=...
    BACKEND_PORT=8000
    ```
  - Expected: No credentials in git.

- [ ] **Run ingestion**
  - Command:
    ```
    python ingest.py
    ```
  - Expected: Console shows "Ingest complete", Qdrant collection `calcu_book` created and contains points.

- [ ] **Check Qdrant content**
  - Action: Use `qdrant-client` or Qdrant Cloud UI to confirm collection and sample payloads include `source`, `chunk_index`, `text`.

- [ ] **Start backend**
  - Command:
    ```
    uvicorn app:app --reload --port 8000
    ```
  - Expected: Server running and `/query` reachable.

---

## API smoke tests
- [ ] **Query the book (global)**
  - Command:
    ```bash
    curl -X POST http://localhost:8000/query -H "Content-Type: application/json" \
      -d '{"question":"What is this book about?","selectionText":""}'
    ```
  - Expected: JSON response with `answer` and `contexts[]`.

- [ ] **Selection-only positive test**
  - Action: Copy an exact sentence from a doc page into `selectionText`.
  - Command:
    ```bash
    curl -X POST http://localhost:8000/query -H "Content-Type: application/json" \
      -d '{"question":"Summarize this sentence","selectionText":"<exact sentence>"}'
    ```
  - Expected: `answer` derived from selection.

- [ ] **Selection-only negative test (strict)**
  - Action: Provide selectionText that does NOT contain the answer.
  - Command:
    ```bash
    curl -X POST http://localhost:8000/query -H "Content-Type: application/json" \
      -d '{"question":"What year did X happen?","selectionText":"A short unrelated sentence."}'
    ```
  - Expected: The assistant returns **exactly**:  
    `I don't know from the provided text.`

---

## Frontend integration tests
- [ ] **Chat widget posts to backend**
  - Action: On a book page with `<ChatWidget />`, type a question and press "Ask book".  
  - Expected: Widget displays an answer.

- [ ] **Ask selected text in UI**
  - Action: Highlight text in a page, click "Ask selected text".
  - Expected: Answer matches selected content or returns refusal string.

---

## CI / Deployment
- [ ] **GitHub Actions (book)**
  - Action: Push to main branch (or create test push)
  - Expected: Action builds `book/` and deploys to GitHub Pages successfully.

- [ ] **Backend deployment (staging/prod)**
  - Action: Deploy Docker image or run on Render/Cloud Run.
  - Expected: Health endpoint returns 200; env secrets configured.

---

## Security checks
- [ ] `.env` or keys not committed
  - Command:
    ```
    git ls-files | grep .env || true
    ```
  - Expected: No `.env` in tracked files.

- [ ] Secrets not in logs or config files
  - Action: Scan repo for API keys (simple grep)
  - Command:
    ```
    git grep -n "OPENAI_API_KEY\|QDRANT_API_KEY" || true
    ```
  - Expected: No keys found.

---

## Accessibility & usability (basic)
- [ ] Buttons have accessible text (no icon-only controls without `aria-label`).
- [ ] Chat widget visible on mobile/responsive.

---

## Final acceptance
- [ ] All above items passed
- [ ] Create PR, include link to deployed GitHub Pages site, backend health URL, and sample test queries.
- [ ] Reviewer sign-off recorded in PR description.

---
