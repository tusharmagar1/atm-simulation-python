<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:000000,50:1a1200,100:E8A93B&height=200&section=header&text=AI%20E-Book%20RAG%20Assistant&fontSize=38&fontColor=E8A93B&animation=fadeIn&desc=Chat%20with%20your%20e-books%20using%20Groq%20LLMs%20%2B%20ChromaDB&descAlignY=62&descSize=17&fontColor=ffffff" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1000&color=E8A93B&center=true&vCenter=true&width=650&lines=%F0%9F%93%9A+Multi-Format+Book+Ingestion;%F0%9F%A7%A0+RAG+with+ChromaDB+%2B+HuggingFace+Embeddings;%E2%9A%A1+Groq+LLM+Streaming+Chat;%F0%9F%8E%93+AI+Quizzes%2C+Flashcards+%26+Notes;%F0%9F%94%92+Multi-Tenant+User+Isolation" alt="Typing SVG" />

<br/>

[![python](https://img.shields.io/badge/python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![fastapi](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#)
[![react](https://img.shields.io/badge/React_18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](#)
[![groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge&logo=lightning&logoColor=white)](#)
[![chromadb](https://img.shields.io/badge/ChromaDB-vector%20store-6E56CF?style=for-the-badge)](#)
[![license](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](#-license)

<br/>

<img src="https://skillicons.dev/icons?i=python,fastapi,react,vite,ts,tailwind,sqlite,docker&theme=dark" />

<br/><br/>

**[✨ Highlights](#-key-features--highlights)** &nbsp;•&nbsp;
**[📸 Screenshots](#-screenshots)** &nbsp;•&nbsp;
**[🏗 Structure](#%EF%B8%8F-folder-structure)** &nbsp;•&nbsp;
**[🛠 Tech Stack](#%EF%B8%8F-tech-stack)** &nbsp;•&nbsp;
**[🚀 Quick Start](#-local-quick-start)** &nbsp;•&nbsp;
**[📦 Deploy to GitHub](#-how-to-upload-project-to-github)**

</div>

<br/>

## 📌 Overview

A production-ready **Retrieval-Augmented Generation (RAG)** application for
uploading e-books (PDF, EPUB, DOCX, TXT), building a high-speed vector database
with **ChromaDB** & **HuggingFace Embeddings** (`BAAI/bge-small-en-v1.5`), and
conversing with content using **Groq LLMs** (`llama-3.3-70b-versatile`).

Featuring a **pitch-black tactile design system**, **ambient WebGL shader rays**,
**multi-tenant user isolation**, **route-level code splitting**, and **shimmer
loading skeletons** — this isn't a weekend RAG demo, it's built like a real product.

<br/>

## 📸 Screenshots

<table>
<tr>
<td width="50%">

**🔐 Sign In**
<img src="assets/screenshots/signin.png" width="100%"/>

</td>
<td width="50%">

**📝 Create Account**
<img src="assets/screenshots/signup.png" width="100%"/>

</td>
</tr>
<tr>
<td width="50%">

**📊 Dashboard**
<img src="assets/screenshots/dashboard.png" width="100%"/>

</td>
<td width="50%">

**📚 Library**
<img src="assets/screenshots/library.png" width="100%"/>

</td>
</tr>
<tr>
<td width="50%">

**💬 AI Reading Chat**
<img src="assets/screenshots/ai-chat.png" width="100%"/>

</td>
<td width="50%">

**🎓 AI Study Suite**
<img src="assets/screenshots/study-suite.png" width="100%"/>

</td>
</tr>
<tr>
<td width="50%">

**🔍 Semantic Search**
<img src="assets/screenshots/semantic-search.png" width="100%"/>

</td>
<td width="50%">

**🛠️ Dev Debugger**
<img src="assets/screenshots/dev-debugger.png" width="100%"/>

</td>
</tr>
</table>

<details>
<summary><b>⚙️ Settings — accent themes & model config</b></summary>
<br/>
<img src="assets/screenshots/settings.png" width="100%"/>
</details>

<br/>

## 🌟 Key Features & Highlights

### 🔒 Core RAG & Multi-Tenant Security
- **Multi-tenant user scoping** — complete database isolation per user for books, chat histories, settings, and generated study notes
- **Backend-enforced API security** — `GROQ_API_KEY` is managed strictly on the server (`backend/.env`); client browsers never store or expose API keys
- **Multi-format document ingestion** — PDF, EPUB, DOCX, and TXT with automatic cover extraction, page indexing, and chapter detection
- **Sentence-aware chunker** — recursive character text splitter with configurable window sizes and overlap thresholds
- **Local vector database (ChromaDB)** — HuggingFace `BAAI/bge-small-en-v1.5` embeddings (384 dimensions) with cosine similarity and MMR retrieval

### 🎨 Next-Gen UI & Visual Aesthetics
- **Pitch-black dark mode (`#000000`)** — deep pitch-black base palette with sleek neumorphic tactile surfaces and custom accent themes (Gold, Red, White)
- **Ambient WebGL background (`SideRays`)** — real-time WebGL shader light rays powered by `ogl`, rendering across all pages
- **MagicCard spotlight forms** — cursor-tracking gradient spotlight effect on Login and Signup cards
- **Ruixen gradient footer** — viewport-pinned animated rainbow gradient footer on Dashboard and Settings pages
- **CLS prevention & shimmer skeletons** — route code-splitting with `React.lazy`/`Suspense`, layout-matching page skeletons, lazy image loading, and 3D isometric loaders

### 🎓 AI Reading & Study Suite
- **Interactive AI reading chat** — streaming SSE responses, Markdown rendering with Tokyo Night Dark code highlighting, citation side-drawers, and session management
- **Book & chapter summarizer** — instant Bullet, Detailed, and Academic summary generation
- **Quiz generator** — automated MCQs, True/False, and short-answer quizzes with difficulty controls and scoring
- **Study flashcards** — animated flip-card deck with question, answer, and memory retention hints
- **AI smart notes** — save, edit, and export Markdown research notes
- **Dev debugger panel** — live vector database scorer, chunk boundary inspection, and collection metrics

<br/>

## 🏗️ Folder Structure

```text
ebook-rag/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI endpoints (auth, books, chat, search, ai_tools, debug, settings)
│   │   ├── core/         # Security, Pydantic settings & env config
│   │   ├── db/           # SQLAlchemy database session & migration helpers
│   │   ├── models/       # Database ORM schemas (User, UserSetting, Book, DocumentChunk, ChatSession, ChatMessage, AINote)
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── services/     # Settings, Auth, Book, Chat, Search, and AI Tools logic
│   │   └── rag/          # RAG pipeline (parsers, chunker, embeddings, vectorstore, retriever)
│   ├── requirements.txt  # Python backend dependencies
│   └── main.py           # FastAPI entrypoint
├── frontend/
│   ├── public/           # Static assets & brand logo PNGs
│   ├── src/
│   │   ├── components/   # Modular UI primitives, skeletons, loaders, SideRays, MagicCard, Navbar, AppFooter
│   │   ├── context/      # AuthContext, AppContext, ColorThemeContext
│   │   ├── pages/        # Dashboard, Library, Chat, AITools, Search, DevTools, Settings, AuthPage
│   │   └── services/     # Axios API client & SSE ReadableStream fetcher
│   ├── package.json      # Vite, React 18, Tailwind CSS, Framer Motion, OGL dependencies
│   └── vite.config.ts    # Build & proxy config
├── assets/
│   └── screenshots/       # README screenshots
└── README.md
```

<br/>

## 🛠️ Tech Stack

### Backend
| Component | Technology |
|---|---|
| Framework | FastAPI (Python 3.10+) & Uvicorn |
| Database | SQLite & SQLAlchemy ORM |
| LLM Engine | Groq API (`llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `deepseek-r1-distill-llama-70b`) |
| Embeddings | HuggingFace `BAAI/bge-small-en-v1.5` via `sentence-transformers` & `langchain-huggingface` |
| Vector Store | ChromaDB |
| Document Parsers | PyMuPDF (`fitz`), EbookLib, `python-docx`, BeautifulSoup4 |

### Frontend
| Component | Technology |
|---|---|
| Framework | React 18 + Vite + TypeScript |
| Styling | Tailwind CSS + custom pitch-black neumorphic design system |
| WebGL Shader | `ogl` (SideRays light background) |
| Animations | Framer Motion |
| Icons | Lucide React |
| Markdown Highlighting | React-Markdown + Rehype-Highlight (Tokyo Night Dark) |

<br/>

## 🚀 Local Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\activate
# Linux / macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from .env.example
cp .env.example .env

# Add your Groq API Key in backend/.env:
# GROQ_API_KEY=gsk_your_groq_key_here

# Run backend development server
uvicorn app.main:app --reload --port 8000
```

Backend API runs at **`http://127.0.0.1:8000`** (interactive Swagger docs at
`http://127.0.0.1:8000/docs`).

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install node dependencies
npm install

# Run frontend development server
npm run dev
```

Frontend web app runs at **`http://localhost:5173`**.

<br/>

## 📦 How to Upload Project to GitHub

Follow these steps to upload your repository to GitHub securely without exposing
secret environment variables or local vector binaries.

<details>
<summary><b>Step 1 — Verify Git status</b></summary>
<br/>

Ensure you are in the root `ebook-rag` directory and check that `.env` and
`venv` are ignored:
```bash
git status
```
</details>

<details>
<summary><b>Step 2 — Initialize & commit code</b></summary>
<br/>

```bash
# Initialize git repository (if not initialized)
git init

# Stage all files
git add .

# Create initial commit
git commit -m "feat: complete EBook RAG Tactile Suite with WebGL SideRays, skeleton loading, and multi-tenant security"
```
</details>

<details>
<summary><b>Step 3 — Create GitHub repository & push</b></summary>
<br/>

1. Go to [GitHub New Repository](https://github.com/new).
2. Enter repository name (e.g. `ebook-rag`).
3. Leave **"Initialize with README" unchecked** (since we already have a custom `README.md`).
4. Click **Create repository**.
5. Copy the terminal commands shown on GitHub and run them in your root directory:

```bash
# Set default branch to main
git branch -M main

# Add remote origin URL (replace URL with your repository link)
git remote add origin https://github.com/tusharmagar1/ebook-rag.git

# Push code to GitHub
git push -u origin main
```
</details>

<br/>

## 📜 License

Distributed under the [MIT License](LICENSE).

<br/>

## 👤 Author

<div align="center">

### Tushar Magar

[![GitHub](https://img.shields.io/badge/GitHub-tusharmagar1-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/tusharmagar1)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-tushar--magar-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tushar-magar-7b80a2255)

### ⭐ Support

If you found this project useful, consider giving it a star on GitHub.

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:E8A93B,50:1a1200,100:000000&height=150&section=footer" width="100%"/>

</div>
