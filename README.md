# 🧠 Instincts AI — Personalized AI Learning Platform

Instincts AI is an AI-powered personalized learning platform that transforms a learner's goals, experience, available resources, study intensity, and practical constraints into a structured learning roadmap.

The platform integrates deterministic RICE-based learner profiling, curated curriculum grounding, Large Language Model (LLM) orchestration, and persistent progress tracking to create personalized learning experiences.

By combining structured learner context with AI-generated content, Instincts AI helps learners organize their study plans, discover relevant learning resources, follow structured roadmaps, and track their learning activities.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Workflow](#-system-workflow)
- [System Architecture](#-system-architecture)
- [RICE-Based Learner Profiling](#-rice-based-learner-profiling)
- [Curriculum Grounding](#-curriculum-grounding)
- [AI Learning Plan Generation](#-ai-learning-plan-generation)
- [Practice Evaluation and Progress Tracking](#-practice-evaluation-and-progress-tracking)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation and Setup](#-installation-and-setup)
- [Environment Configuration](#-environment-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Testing and Evaluation](#-testing-and-evaluation)
- [Current Limitations](#-current-limitations)
- [Future Enhancements](#-future-enhancements)
- [Security](#-security)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

Creating an effective learning plan requires more than selecting topics. Learners have different experience levels, resource availability, study commitments, and practical constraints that influence how they approach a learning goal.

Instincts AI addresses these factors through a modular workflow that combines deterministic profiling with AI-generated learning content.

The application:

1. Collects the learner's goal and study preferences.
2. Validates the submitted information through the backend.
3. Calculates a normalized learner profile using RICE-based rules.
4. Matches the learner's goal against a curated curriculum resource catalogue.
5. Constructs an LLM prompt using the available learner context.
6. Generates and processes a personalized learning plan through the Groq API.
7. Presents the generated roadmap through the React frontend.
8. Stores learning plans and checkpoint information in SQLite.
9. Supports practice submissions, AI-generated feedback, attempt history, and progress summaries.

The architecture separates deterministic profiling and curriculum matching from language-model generation, providing a structured foundation for personalized learning.

## ✨ Key Features

### 1. Personalized Learning Roadmaps

Generates structured learning plans based on the learner's goal and profile.

A generated roadmap can include:

- Goal summary
- Staged learning path
- Four-week learning roadmap
- Recommended learning resources
- Practice strategy
- Milestones and checkpoints
- Expected learning outcome

### 2. RICE-Based Learner Profiling

Uses a project-specific RICE model based on four learner inputs:

- **Resources:** Learning resources available to the learner.
- **Intensity:** Selected study intensity.
- **Constraints:** Practical limitations affecting the learning process.
- **Experience:** Existing familiarity with the subject.

The backend converts these inputs into normalized values and derives three profile components:

- Pace
- Difficulty
- Availability

The profile is calculated using deterministic rules rather than generated directly by the LLM.

### 3. Curated Curriculum Grounding

Uses `curated_resources.json` to associate learning goals with predefined curriculum domains and resources.

The grounding module:

- Matches goal keywords against curated domain keywords.
- Identifies a matching domain when the implemented conditions are satisfied.
- Retrieves associated resource entries.
- Supplies available curriculum context to the learning-plan generation workflow.
- Handles goals for which no curated domain matches.

The current implementation uses keyword matching rather than semantic embeddings or vector-database retrieval.

### 4. Groq LLM Integration

Integrates the Groq API for AI-powered learning-plan generation and practice evaluation.

The LLM orchestration workflow includes:

- Structured prompt construction
- Learner-profile context
- Curated resource context when available
- Model request handling
- Structured response processing
- Response normalization

The configured model in the shared implementation is `openai/gpt-oss-120b`.

### 5. Learning Plan Persistence

Uses SQLite to persist learning and progress information.

The persistence layer supports application workflows involving:

- Learning-plan storage and retrieval
- Latest-plan retrieval
- Checkpoint status
- Practice attempts
- Progress information

### 6. Practice Evaluation

Supports practice submissions and AI-generated feedback.

The evaluation workflow accepts a practice task and learner solution, sends the relevant information for LLM-based evaluation, and returns a model-generated score and feedback.

Practice results can be recorded and retrieved as part of the learner's activity history.

### 7. Progress Tracking

Provides progress-related functionality associated with learning plans and practice activities.

Supported information includes:

- Checkpoint status
- Practice attempt history
- Recorded practice scores
- Best recorded score
- Learning progress summaries

---

## 🔄 System Workflow

```text
                    Learner
                       |
                       v
             React + Vite Frontend
                       |
                       v
                FastAPI Backend
                       |
                       v
               Request Validation
                       |
                       v
             RICE Profiling Module
                       |
                       v
          Curriculum Grounding Module
                       |
                       v
              Prompt Construction
                       |
                       v
                 Groq LLM API
                       |
                       v
          Response Processing and
                Normalization
                       |
                       v
            Personalized Learning Plan
                       |
                +------+------+
                |             |
                v             v
          SQLite Database   React UI
                |             |
                v             v
        Plans, Checkpoints   Roadmap and
        and Practice Data    Progress View
```

The frontend manages user interaction and presentation. The backend coordinates request validation, learner profiling, curriculum grounding, LLM requests, response processing, and database operations.

## 🏗️ System Architecture

Instincts AI follows a modular client-server architecture consisting of frontend, backend, profiling, curriculum grounding, LLM orchestration, and persistence components.

### Frontend Layer

**Technologies:** React, Vite, JavaScript

Responsibilities:

- Collect learner inputs.
- Display generated learning plans.
- Present roadmap stages and milestones.
- Support practice interactions.
- Display evaluation feedback and progress information.
- Communicate with the backend API.

### Backend Layer

**Technology:** FastAPI

Responsibilities:

- Validate incoming requests.
- Coordinate profiling and curriculum grounding.
- Construct LLM requests.
- Process model responses.
- Manage learning-plan and progress workflows.
- Expose application functionality through API endpoints.

### Learner Profiling Layer

**Module:** `rice_profiling.py`

Calculates normalized learner-profile values using predefined category mappings and deterministic formulas.

### Curriculum Grounding Layer

**Module:** `curriculum_grounding.py`

**Catalogue:** `curated_resources.json`

Matches learner goals against curated domain keywords and returns the available resource context.

### LLM Orchestration Layer

**Module:** `llm.py`

Manages the Groq client, model requests, generation settings, and response processing.

### Progress Tracking Layer

**Module:** `progress_tracking.py`

Supports progress-related application functionality.

### Persistence Layer

**Technology:** SQLite

**Database:** `instincts_ai.db`

Stores application data used by learning-plan, checkpoint, practice, and progress workflows.

---

## 🧮 RICE-Based Learner Profiling

The RICE profiling module transforms learner inputs into normalized numerical values.

| Component | Description |
|---|---|
| Resources | Represents the learner's available learning resources. |
| Intensity | Represents the selected study intensity. |
| Constraints | Represents meaningful practical constraints. |
| Experience | Represents existing subject familiarity. |

The resulting learner profile contains three components:

| Profile Component | Description |
|---|---|
| Pace | Derived learning-pace value. |
| Difficulty | Derived learning-difficulty value. |
| Availability | Derived availability value. |

The implementation uses predefined category mappings and deterministic calculations, making the profiling output reproducible for equivalent inputs.

The profile is subsequently used as structured context during learning-plan generation.

## 📚 Curriculum Grounding

The curriculum-grounding module connects learner goals with resources defined in `curated_resources.json`.

### Matching Process

1. Receive the learner's goal.
2. Load the curated domain catalogue.
3. Compare the goal against the available domain keywords.
4. Identify a matching domain when a keyword match is found.
5. Retrieve the associated curated resources.
6. Supply the available resource context to prompt construction.
7. Handle unmatched goals through the application's fallback behavior.

### Supported Learning Domains

The curated catalogue includes learning areas such as:

- Python programming
- Java programming
- Data analytics
- Data science
- Machine learning
- Web development
- Data Structures and Algorithms for placements
- Cloud computing
- Cybersecurity
- UI/UX design
- Digital marketing
- Business analytics with Excel
- App development
- Content writing

The catalogue provides domain-specific context for learning-plan generation when a matching domain is identified.

## 🤖 AI Learning Plan Generation

The learning-plan generation module combines learner context, profiling output, and available curriculum information.

### Input

- Learner goal
- Normalized RICE profile
- Available curated resource context
- Prompt instructions

### Processing

The backend constructs a structured prompt and sends the request to the configured Groq model. The returned response is processed and normalized before being delivered to the frontend.

The LLM generation settings include a temperature of `0.2` in the shared implementation. Token limits and structured-output handling are configured in `llm.py`.

### Output

The generated learning plan can contain:

- Goal summary
- Ordered learning stages
- Four-week roadmap
- Recommended resources
- Practice strategy
- Milestones and checkpoints
- Expected learning outcome

Deterministic backend modules manage learner profiling and keyword-based curriculum matching, while the language model generates the learning-plan content.

## 📈 Practice Evaluation and Progress Tracking

The practice workflow supports learner submissions and LLM-generated feedback.

```text
Learner Selects a Topic
          |
          v
Learner Provides a Practice Task
          |
          v
Learner Submits a Solution
          |
          v
Backend Sends Evaluation Request
          |
          v
LLM Generates Score and Feedback
          |
          v
Backend Records the Attempt
          |
          v
Frontend Displays the Result
          |
          v
Practice History and Progress
          Can Be Retrieved
```

Practice results and recorded learning activities support progress-history workflows.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Frontend | React | User interface |
| Frontend tooling | Vite | Development server and build tooling |
| Backend | FastAPI | API and application logic |
| Programming language | Python | Backend implementation |
| LLM provider | Groq API | AI generation and evaluation |
| Configured model | `openai/gpt-oss-120b` | Language-model requests |
| Database | SQLite | Local application persistence |
| Resource catalogue | JSON | Curated domains and resources |
| Configuration | Environment variables | API-key configuration |

---

## 📁 Project Structure

```text
Instincts_AI/
│
├── backend/
│   ├── curated_resources.json
│   ├── curriculum_grounding.py
│   ├── instincts_ai.db
│   ├── llm.py
│   ├── main.py
│   ├── progress_tracking.py
│   ├── prompts.py
│   ├── README_BACKEND_PATCH.md
│   ├── requirements.txt
│   ├── rice_profiling.py
│   └── utils.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   └── vite.config.js
│
├── .agents/
├── .streamlit/
├── app.py
├── check_db.py
├── check_models.py
├── history.py
├── instincts_ai.db
├── README.md
├── SECURITY-REVIEW.md
└── ui.py
```

### Backend Modules

| File | Responsibility |
|---|---|
| `main.py` | FastAPI application and API routes |
| `llm.py` | Groq client and LLM request handling |
| `rice_profiling.py` | RICE-based learner-profile calculations |
| `curriculum_grounding.py` | Keyword-based domain matching |
| `curated_resources.json` | Curated resource catalogue |
| `prompts.py` | Prompt construction |
| `progress_tracking.py` | Progress-tracking functionality |
| `utils.py` | Shared utility functions |
| `requirements.txt` | Python dependencies |

### Frontend Components

| File or Directory | Responsibility |
|---|---|
| `src/` | Frontend application source |
| `public/` | Static assets |
| `package.json` | Frontend dependencies and scripts |
| `package-lock.json` | Locked npm dependency tree |
| `vite.config.js` | Vite configuration |
| `index.html` | Frontend entry HTML |

---

## 💻 Prerequisites

- Python compatible with the backend dependencies
- Node.js and npm
- Git
- A Groq API key

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd Instincts_AI
```

### 2. Install Backend Dependencies

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment.

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure the API Key

Create a `.env` file inside the `backend/` directory:

```env
GROQ_API_KEY=your-groq-api-key
```

### 4. Install Frontend Dependencies

Open a separate terminal and navigate to the frontend directory:

```bash
cd frontend
npm install
```

### 5. Configure the Backend URL

The frontend communicates with the FastAPI backend through its configured API base URL.

For local development, the backend address is typically:

```text
http://127.0.0.1:8000
```

## 🚀 Running the Application

### Start the Backend

From the `backend/` directory, activate the virtual environment and run:

```bash
uvicorn main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

### Start the Frontend

From the `frontend/` directory, run:

```bash
npm run dev
```

Open the local URL displayed by Vite in the terminal.

## 📖 API Documentation

The FastAPI interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The documentation interface provides access to the API routes registered by the backend application.

---

## 🧪 Testing and Evaluation

Instincts AI supports functional testing of its primary workflows, including learning-plan generation, curriculum matching, checkpoint updates, practice evaluation, practice history, and progress retrieval.

### Evaluation Metrics

| Metric | Description |
|---|---|
| Roadmap Completeness | Measures the presence of required learning-plan components. |
| Resource Validity | Measures the proportion of audited resources that meet predefined validity criteria. |
| End-to-End Latency | Measures the time required to complete a generation request. |
| Token Consumption | Records prompt and completion token usage. |
| Practice-Score Agreement | Compares model-generated scores with independent expert ratings. |
| Ablation Analysis | Examines the contributions of RICE profiling and curriculum grounding. |

### Baseline Configurations

| Configuration | RICE Profiling | Curriculum Grounding |
|---|---|---|
| Generic LLM Baseline | Disabled | Disabled |
| RICE-Only | Enabled | Disabled |
| Grounding-Only | Disabled | Enabled |
| Complete Instincts AI | Enabled | Enabled |

These configurations provide a basis for comparing the effects of learner profiling and curriculum grounding on generated learning plans.

---

## ⚠️ Current Limitations

- Curriculum grounding relies on literal keyword matching.
- Unmatched goals may not receive curated resource recommendations.
- Curated resources require separate checks for relevance and availability.
- Generated learning plans may vary in completeness and usefulness.
- Practice evaluation relies on LLM-generated scores and feedback.
- Checkpoint status records completion information but does not independently establish subject mastery.
- Quantitative comparisons require systematic evaluation under consistent conditions.

## 🔭 Future Enhancements

- Semantic retrieval for improved goal matching.
- Expanded curriculum coverage and resource validation.
- Controlled baseline and ablation experiments.
- Expert validation of practice evaluation.
- Adaptive learning roadmaps based on learner progress.
- Improved authentication and user-specific data management.
- Expanded automated testing.
- Performance monitoring for latency and token consumption.
- Production deployment and database scalability improvements.

## 🔐 Security

- API credentials are configured through environment variables.
- The backend uses the `GROQ_API_KEY` environment variable for Groq authentication.
- Application data is persisted using SQLite.
- Security review and deployment configuration are maintained alongside the project.

## 🤝 Contributing

Contributions are welcome in the areas of learner profiling, curriculum grounding, prompt engineering, frontend development, progress tracking, testing, and application reliability.

## 📄 License

The project license can be specified here when a license has been selected.
