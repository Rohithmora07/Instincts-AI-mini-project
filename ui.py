import streamlit as st

from backend.utils import build_profile
from backend.progress_tracking import get_checkpoints, update_checkpoint_status


def render_progress(plan_id: int) -> None:
    st.markdown("<br><div class='section-label'>Track your progress</div>", unsafe_allow_html=True)
    checkpoints = get_checkpoints(plan_id)
    status_options = ["not_started", "completed", "struggling", "skipped"]
    for cp in checkpoints:
        current_index = status_options.index(cp["status"])
        new_status = st.radio(
            cp["text"], status_options, index=current_index,
            horizontal=True, key=f"checkpoint_{cp['id']}",
        )
        if new_status != cp["status"]:
            update_checkpoint_status(cp["id"], new_status)

def inject_styles() -> None:
    st.markdown("""
    <style>
      .stApp { background: radial-gradient(circle at top right, #26164a 0, #100d1f 34%, #090914 76%); color: #f5f1ff; }
      .block-container { max-width: 1180px; padding-top: 2.8rem; padding-bottom: 4rem; }
      .hero { padding: 2.4rem 2.5rem; border: 1px solid rgba(225, 184, 84, .58); border-radius: 22px; background: linear-gradient(120deg, rgba(112, 68, 185, .32), rgba(20, 15, 42, .65)); margin-bottom: 2rem; }
      .eyebrow { color: #e7bf62; font-size: .83rem; letter-spacing: .14em; font-weight: 700; text-transform: uppercase; }
      .hero h1 { color: #fbf7ff; font-size: clamp(2.4rem, 5vw, 4.2rem); margin: .35rem 0; letter-spacing: -.045em; }
      .hero p { color: #d6cce7; font-size: 1.12rem; margin: 0; }
      .section-label { color: #e7bf62; font-size: .82rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; margin-bottom: .4rem; }
      .form-card, .plan-card { background: rgba(26, 21, 45, .84); border: 1px solid rgba(151, 113, 218, .35); border-radius: 18px; padding: 1.45rem; margin-bottom: 1rem; }
      .flow { display: flex; gap: .65rem; flex-wrap: wrap; align-items: center; color: #dcd1ef; margin-top: 1.25rem; font-size: .94rem; }
      .flow span { background: rgba(231, 191, 98, .12); border: 1px solid rgba(231, 191, 98, .28); border-radius: 999px; padding: .38rem .7rem; }
      .stButton > button { background: linear-gradient(110deg, #7d4bd2, #a865e5) !important; color: white !important; border: 1px solid #e7bf62 !important; border-radius: 10px !important; font-weight: 750 !important; min-height: 3rem; }
      .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div { background: #151124 !important; color: #f5f1ff !important; border-color: #7652ac !important; }
      div[data-testid="stExpander"] { background: rgba(26, 21, 45, .72); border: 1px solid rgba(151, 113, 218, .36); border-radius: 13px; margin-bottom: .75rem; }
      div[data-testid="stExpander"] summary { color: #f1d788; font-weight: 700; }
      .history-item { color: #d6cce7; font-size: .91rem; }
    </style>
    """, unsafe_allow_html=True)


def render_hero() -> None:
    st.markdown("""
    <section class="hero">
      <div class="eyebrow">Personalized learning, clearly structured</div>
      <h1>🎓 Instincts AI</h1>
      <p>Adaptive AI Learning Companion</p>
      <p style="margin-top:.7rem">Transform your learning goal into a personalized roadmap using RICE profiling.</p>
      <div class="flow"><span>🎯 Learner Goal</span><b>↓</b><span>🧭 RICE Profiling</span><b>↓</b><span>✨ LLM</span><b>↓</b><span>🗺️ Personalized Learning Plan</span></div>
    </section>
    """, unsafe_allow_html=True)


def render_profile_form() -> dict | None:
    st.markdown('<div class="section-label">Build your roadmap</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("Step 1 · Learner Goal")
        goal = st.text_area("What do you want to learn?", placeholder="I want to become a Data Analyst in 6 months.\n\nOr\n\nI want to master Python for placements.", height=150)
        st.subheader("Step 2 · RICE Profile")
        left, right = st.columns(2)
        with left:
            resources = st.multiselect("Resources", ["Laptop", "Internet", "Books", "Paid Courses", "Free Courses", "Mentor", "None"])
            experience = st.selectbox("Experience", ["Beginner", "Intermediate", "Advanced"])
        with right:
            intensity = st.selectbox("Intensity", ["Low — 30 min/day", "Medium — 1 hour/day", "High — 2–3 hours/day", "Very High — 4+ hours/day"])
            constraints = st.multiselect("Constraints", ["College", "Job", "Budget", "Slow Internet", "Family Responsibilities", "None"])
        submitted = st.button("✨ Generate Personalized Plan", use_container_width=True)

    if not submitted:
        return None
    if not goal.strip():
        st.warning("Please enter a learning goal before generating your roadmap.")
        return None
    return build_profile(goal, resources, intensity, constraints, experience)


def render_plan(plan: dict[str, str]) -> None:
    st.markdown("<br><div class='section-label'>Your personalized learning plan</div>", unsafe_allow_html=True)
    sections = [
        ("🎯 Goal Summary", "goal_summary"),
        ("🧭 Recommended Learning Path", "learning_path"),
        ("🗓️ Weekly Roadmap", "weekly_roadmap"),
        ("📚 Recommended Resources", "recommended_resources"),
        ("🧪 Practice Strategy", "practice_strategy"),
        ("🏁 Milestones", "milestones"),
        ("✨ Expected Outcome", "expected_outcome"),
    ]
    for title, key in sections:
        with st.expander(title, expanded=key in {"goal_summary", "learning_path"}):
            st.markdown(plan[key])


def render_history() -> None:
    history = st.session_state.learning_plan_history
    if not history:
        return
    with st.sidebar:
        st.header("🗂️ Plan History")
        for item in reversed(history[-5:]):
            goal = item["profile"]["goal"]
            with st.expander(goal[:54] + ("…" if len(goal) > 54 else "")):
                st.caption(item["created_at"].strftime("%d %b, %I:%M %p"))
                st.markdown(item["plan"]["goal_summary"])
