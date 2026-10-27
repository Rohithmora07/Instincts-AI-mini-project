import streamlit as st

from backend.curriculum_grounding import ground_domain
from history import add_plan, initialize_history
from backend.llm import generate_learning_plan
from backend.progress_tracking import get_latest_plan, init_db, save_plan
from backend.rice_profiling import compute_rice_vector
from ui import inject_styles, render_hero, render_history, render_plan, render_profile_form, render_progress
from backend.utils import build_profile


st.set_page_config(page_title="Instincts AI | Learning Companion", page_icon="🎓", layout="wide")

init_db()
initialize_history()
inject_styles()
render_hero()

if "current_plan" not in st.session_state or st.session_state.current_plan is None:
    latest = get_latest_plan()
    if latest:
        st.session_state.current_plan = latest["plan"]
        st.session_state.current_plan_id = latest["plan_id"]

profile = render_profile_form()

if profile:
    rice_vector = compute_rice_vector(profile)
    grounding = ground_domain(profile["goal"])
    with st.spinner("Building your personalized learning roadmap..."):
        try:
            plan = generate_learning_plan(profile, rice_vector, grounding)
            st.session_state.current_plan = plan
            st.session_state.current_plan_id = save_plan(profile, plan)
            add_plan(profile, plan)
        except Exception as error:
            st.error(f"Unable to generate a plan right now: {error}")

if st.session_state.get("current_plan"):
    render_plan(st.session_state.current_plan)
    render_progress(st.session_state.current_plan_id)

render_history()