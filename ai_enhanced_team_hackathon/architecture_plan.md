High-Level Architecture Plan

Project: AI Study & Flashcard Generator

Directory: holbertonschool-ai4devs/ai_enhanced_team_hackathon

1. System Architecture Overview

The application follows a decoupled Client–Server–LLM architecture designed for rapid hackathon development, clean separation of concerns, and reliable structured JSON outputs from the AI model.

+-------------------------------------------------------------------+
|                        Frontend (Client)                          |
|  React / Next.js + Tailwind CSS                                   |
|  - Notes Input & File Uploader                                    |
|  - Interactive Flashcard Viewer & Quiz Engine                     |
|  - CSV / Markdown Exporter                                        |
+---------------------------------+---------------------------------+
                                  | REST API (JSON over HTTPS)
                                  v
+-------------------------------------------------------------------+
|                        Backend (API Server)                       |
|  Python (FastAPI) or Node.js (Express)                            |
|  - Input Validation & Text Chunking                               |
|  - Prompt Orchestration & Schema Enforcement                      |
|  - Deck CRUD & Export Formatting                                  |
+----------------+----------------------------------+---------------+
                 |                                  |
                 v                                  v
+---------------------------------+  +------------------------------+
|       Database (Persistence)    |  |      External LLM API        |
|  PostgreSQL / SQLite            |  |  OpenAI / Gemini API         |
|  - Users, Decks, Flashcards,    |  |  - Structured JSON Output    |
|    and QuizQuestions            |  |    (Cards + MCQ generation)  |
+---------------------------------+  +------------------------------+


2. Component Breakdown

Frontend Layer

Tech Stack: React (Vite or Next.js) with Tailwind CSS for rapid, responsive UI styling.

Responsibilities:

Provide a clean input interface for pasting text or reading .txt/.md files locally via the browser FileReader API.

Render smooth CSS 3D flip animations for flashcards and keyboard navigation (Space to flip, ArrowLeft/ArrowRight to navigate).

Manage local quiz state (selected answers, score calculation, and review mode).

Generate client-side .csv and .md downloads using Blob URLs.

Backend API Layer

Tech Stack: Python with FastAPI (chosen for native Pydantic schema validation and fast async I/O).

Key Endpoints:

POST /api/decks/generate — Accepts raw text, calls the LLM service, saves the deck/cards/quiz to the DB, and returns the structured payload.

GET /api/decks/{deck_id} — Retrieves a saved study deck with its flashcards and quiz questions.

PATCH /api/flashcards/{card_id} — Updates card text or is_mastered status.

GET /api/decks/{deck_id}/export?format=csv|md — Returns downloadable formatted study material.

AI / LLM Integration Layer

Prompt Strategy: Use system instructions enforcing strict JSON schema output (via Structured Outputs / JSON mode) so the backend reliably receives:

A concise deck title

8–12 atomic flashcards (question, answer)

5 quiz_questions (prompt, options[4], correct_index, explanation)

Guardrails: Enforce character limits on input text (e.g., max 15,000 characters for MVP) and handle LLM timeouts or malformed responses gracefully with automatic retries.

Data Persistence Layer

Tech Stack: SQLite for zero-config local hackathon development, easily swappable to PostgreSQL for deployment via SQLAlchemy ORM.

3. Data Flow (Generate Study Deck)

User Input: User pastes lecture notes and clicks "Generate Study Set".

API Request: Frontend sends POST /api/decks/generate with { "source_text": "..." }.

LLM Processing: Backend validates text length, injects the text into the prompt template, and requests structured JSON from the LLM API.

Storage: Backend parses the validated response, persists StudyDeck, Flashcard, and QuizQuestion records, and returns HTTP 201 Created with the full JSON object.

Interactive Study: Frontend transitions immediately to the Flashcard & Quiz workspace.

4. Team Execution & Task Split

Alice (AI Prompt Strategist): Design and test the JSON-schema prompts for high-quality flashcards and distractors in multiple-choice questions.

Bob (Frontend Dev): Build the input screen, interactive flashcard deck UI, and quiz component.

Carol (Backend/API Dev): Set up FastAPI, database models, LLM API integration, and REST endpoints.

Dave (UI/UX & Testing Lead): Refine responsive styling, implement CSV/Markdown export, and run end-to-end QA tests.
