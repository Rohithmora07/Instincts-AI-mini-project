# Instincts AI

Instincts AI is an adaptive AI learning companion. It turns a learner's goal and RICE profile—Resources, Intensity, Constraints, and Experience—into a personalized learning roadmap.

## Workflow

`Learner Goal → RICE Profiling → LLM → Personalized Learning Plan`

The plan includes a goal summary, staged learning path, four-week roadmap, recommended resources, practice strategy, milestones, and expected outcome. It does not score or evaluate learners.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml` before generating plans:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

## Project structure

```text
app.py       # Application composition
ui.py        # Streamlit interface and styles
prompts.py   # Learning-plan prompt
llm.py       # Groq client and LLM call
utils.py     # Profile and response helpers
history.py   # Session history
```
