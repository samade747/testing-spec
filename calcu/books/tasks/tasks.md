# Tasks (dependency-ordered)
Project: Spec-Driven AI Book + RAG Chatbot  
Spec: 001

> Format: Task # — Title (Estimate) — Owner — Prereqs — Success criteria — Commands/snippets

---

1. **Initialize repository & constitution** — owner: dev  
   - Prereqs: none  
   - Success: `.specify/memory/constitution.md` exists; repo has `book/`, `backend/`, `specs/`, `plans/`, `tasks/`, `checklist/` folders.  
   - Commands:
     ```bash
     git init
     mkdir book backend specs plans tasks checklist
     # add constitution file (from spec)
     git add . && git commit -m "chore: init repo and add constitution"
     ```

2. **Scaffold Docusaurus site**  — owner: dev  
   - Prereqs: Task 1  
   - Success: `book/package.json`, `docusaurus.config.js`, `sidebars.js` present; `npm ci` succeeds.  
   - Commands:
     ```bash
     cd book
     npm init -y
     npm install @docusaurus/core @docusaurus/preset-classic react react-dom
     ```

3. **Create book docs (intro + 6 chapters + rag-chatbot pages)**  — owner: content/dev  
   - Prereqs: Task 2  
   - Success: `book/docs/intro.md`, `chapter-1-getting-started.md`, ..., `rag-chatbot/index.md` present.  
   - Notes: Each doc should include examples and code snippets.

4. **Add ChatWidget and SelectedTextHelper components**  — owner: frontend dev  
   - Prereqs: Task 2, Task 3  
   - Success: `book/src/components/ChatWidget.jsx` and `SelectedTextHelper.jsx` exist and compile in local preview.  
   - Commands: import and test on an MDX page.

5. **Scaffold backend skeleton**  — owner: backend dev  
   - Prereqs: Task 1  
   - Success: `backend/app.py`, `backend/requirements.txt`, `.env.example`, `Dockerfile` exist and `pip install -r requirements.txt` works.  
   - Commands:
     ```bash
     python -m venv .venv
     .venv/bin/pip install -r backend/requirements.txt
     ```

6. **Implement ingest.py (chunk + embed + upsert)**  — owner: backend dev  
   - Prereqs: Task 3, Task 5  
   - Success: Running `python backend/ingest.py` upserts records to Qdrant (verify collection `calcu_book`).  
   - Commands:
     ```bash
     python backend/ingest.py
     ```

7. **Test ingest pipeline locally**  — owner: backend dev  
   - Prereqs: Task 6, Qdrant cluster & OPENAI_API_KEY set  
   - Success: Qdrant contains points; sample retrieval returns relevant chunks.  
   - Commands: use `qdrant-client` to list collections or call a quick search.

8. **Implement POST /query with selection-only strict mode** (2h) — owner: backend dev  
   - Prereqs: Task 5, Task 6  
   - Success: `POST /query` returns `{ answer, contexts }`. If selectionText provided and not present → return exact refusal string.  
   - Test:
     ```bash
     curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question":"...","selectionText":"..."}'
     ```

9. **Wire ChatWidget to backend**  — owner: frontend dev  
   - Prereqs: Task 4, Task 8  
   - Success: Chat widget posts to backend and displays answers; selection capture works.  
   - Test in browser: highlight text → Ask selected text → verify response.

10. **Add unit / smoke tests for backend**  — owner: dev/tester  
    - Prereqs: Task 8, Task 7  
    - Success: Tests for `ingest` chunker, `POST /query` positive + negative run with pytest or simple scripts.

11. **Add Dockerfile and test Docker build** — owner: devops  
    - Prereqs: Task 5  
    - Success: `docker build -t calcu-backend .` succeeds and container runs.

12. **Create GitHub Actions to build & deploy Docusaurus to GitHub Pages** (1.5h) — owner: devops  
    - Prereqs: Task 2, Task 3  
    - Success: On push to `main`, action builds `book` and deploys to GitHub Pages.

13. **Create deployment plan & host backend**  — owner: devops  
    - Prereqs: Task 11, Task 12  
    - Success: Backend deployed to Render/Cloud Run with env vars set; returns OK on health check.

14. **Run full acceptance checklist & fix issues**  — owner: all  
    - Prereqs: Tasks 1–13  
    - Success: All checklist items pass.

15. **Create PR & code review**  — owner: dev  
    - Prereqs: Task 14  
    - Success: PR created with tasks linked; reviewers assigned; checks passing.

---

## Task metadata
- Default owner: `dev` (replace with actual names)
- Time estimates are approximate; adjust for team size.
- Use `/sp.clarify` to refine any task or duration.
