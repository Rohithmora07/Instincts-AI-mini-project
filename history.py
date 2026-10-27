from datetime import datetime

import streamlit as st


def initialize_history() -> None:
    st.session_state.setdefault("learning_plan_history", [])
    st.session_state.setdefault("current_plan", None)


def add_plan(profile: dict, plan: dict) -> None:
    st.session_state.learning_plan_history.append(
        {"created_at": datetime.now(), "profile": profile, "plan": plan}
    )
