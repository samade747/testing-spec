# Tasks: Spec-Driven AI Book + Embedded RAG Chatbot

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure


## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create repository structure as defined in plan.md (`book/`, `backend/`, `specs/`, `plans/`, `tasks/`, `checklist/`)
- [ ] T002 Initialize Docusaurus site in `book/` (including `book/package.json`, `docusaurus.config.js`, `sidebars.js`)
- [ ] T003 [P] Configure initial `.gitignore`, `.dockerignore` for `book/` and `backend/` in `D:/github/testing-spec/calcu/book/`
- [ ] T004 Scaffold backend skeleton in `backend/` (including `backend/app.py`, `backend/requirements.txt`, `.env.example`, `Dockerfile`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Install Docusaurus dependencies in `book/` (`cd book && npm ci`)
- [ ] T006 Install backend dependencies in `backend/` (`cd backend && pip install -r requirements.txt`)
- [ ] T007 Create book docs (`book/docs/intro.md`, `chapter-1-getting-started.md`, ..., `rag-chatbot/index.md`)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Book builds and deploys (P1) 🎯 MVP

**Goal**: The Docusaurus book builds locally and deploys to GitHub Pages.

**Independent Test**: `book` builds (`cd book && npm ci && npm run build`) and preview runs (`npm start`). GitHub Actions successfully deploys `book/` to GitHub Pages.

### Implementation for User Story 1

- [ ] T008 [US1] Build Docusaurus site locally (`cd book && npm run build`)
- [ ] T009 [US1] Create GitHub Actions workflow to build and deploy Docusaurus to GitHub Pages (`.github/workflows/deploy.yml`)
- [ ] T010 [US1] Test GitHub Actions deployment

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Ingest book content (P1)

**Goal**: The ingest script processes book content, chunks it, embeds it, and upserts it into Qdrant.

**Independent Test**: Running `python backend/ingest.py` successfully upserts records to Qdrant (verify collection `calcu_book`). Qdrant collection named `calcu_book` with payloads `{ source, chunk_index, text }`.

### Implementation for User Story 2

- [ ] T011 [US2] Implement `backend/ingest.py` (chunk, embed, upsert to Qdrant)
- [ ] T012 [US2] Configure Qdrant collection named `calcu_book` with specified payloads.
- [ ] T013 [US2] Test `backend/ingest.py` locally

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - `POST /query` endpoint (P1)

**Goal**: The backend exposes a `POST /query` endpoint that accepts questions and optional `selectionText`, returning an answer and contexts.

**Independent Test**: `POST /query` returns sensible answers for book queries. Selection-only mode returns direct answers from the selection; if not present, returns exact refusal string.

### Implementation for User Story 3

- [ ] T014 [US3] Implement `POST /query` endpoint in `backend/app.py`
- [ ] T015 [US3] Implement selection-only strict mode for `POST /query` (return `I don't know from the provided text.` if answer not in selection)
- [ ] T016 [US3] Integrate OpenAI embeddings and chat model into `POST /query`
- [ ] T017 [US3] Add basic local tests for `POST /query` (e.g., `pytest backend/test_app.py`)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Chat UI functionality (P1)

**Goal**: The React chat widget can capture highlighted text, send it with questions, and display answers and context summaries.

**Independent Test**: Chat widget posts to backend and displays answers; selection capture works.

### Implementation for User Story 4

- [ ] T018 [US4] Create `book/src/components/ChatWidget.jsx`
- [ ] T019 [US4] Create `book/src/components/SelectedTextHelper.jsx`
- [ ] T020 [US4] Implement text highlighting capture in `SelectedTextHelper.jsx`
- [ ] T021 [US4] Wire `ChatWidget.jsx` to `POST /query` endpoint
- [ ] T022 [US4] Display answer and context summary in `ChatWidget.jsx`

---

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T023 Add unit / smoke tests for backend in `backend/tests/`
- [ ] T024 Add Dockerfile for backend in `backend/Dockerfile` and test Docker build
- [ ] T025 Update `README_DEPLOY.md` with complete deploy instructions
- [ ] T026 Final code cleanup and refactoring

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence