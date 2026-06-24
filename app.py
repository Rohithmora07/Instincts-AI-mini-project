import streamlit as st

st.set_page_config(page_title="Instincts AI", page_icon="💡", layout="centered")
# Add this at the TOP of app.py, pages/1_core_instincts.py, and pages/2_interview_coach.py

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%);
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: transparent;
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border-radius: 16px;
        margin-bottom: 40px;
        border: 2px solid #d4af37;
    }
    
    .hero-title {
        font-size: 3.5em;
        font-weight: 900;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.3em;
        color: #a0a0b0;
        font-weight: 300;
    }
    
    /* Card Styling */
    .card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #d4af37;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(212, 175, 55, 0.1);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        border-color: #ffd700;
        box-shadow: 0 12px 48px rgba(212, 175, 55, 0.3);
        transform: translateY(-2px);
    }
    
    .card-title {
        font-size: 1.4em;
        font-weight: 700;
        color: #ffd700;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 2px solid #d4af37;
        padding-bottom: 12px;
    }
    
    /* Input Fields */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #d4af37 !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
        font-size: 1em !important;
        padding: 12px !important;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2) !important;
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: 2px solid #d4af37 !important;
        border-radius: 8px !important;
        padding: 12px 32px !important;
        font-weight: 700 !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5) !important;
        border-color: #ffd700 !important;
    }
    
    /* Score Box */
    .score-box {
        background: rgba(99, 102, 241, 0.1);
        border: 2px solid #d4af37;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .score-box:hover {
        border-color: #ffd700;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }
    
    .score-number {
        font-size: 2.5em;
        font-weight: 900;
        color: #ffd700;
        margin-bottom: 8px;
    }
    
    .score-label {
        font-size: 0.9em;
        color: #a0a0b0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Framework Badges */
    .rice-badge {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.05));
        color: #4ade80;
        border: 2px solid #d4af37;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
        margin-right: 8px;
    }
    
    .star-badge {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.2), rgba(249, 115, 22, 0.05));
        color: #fb923c;
        border: 2px solid #d4af37;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Feedback Section */
    .feedback-section {
        background: rgba(34, 197, 94, 0.05);
        border-left: 4px solid #ffd700;
        border: 2px solid #d4af37;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }
    
    .feedback-title {
        color: #ffd700;
        font-weight: 700;
        margin-bottom: 8px;
        font-size: 1.1em;
    }
    
    .feedback-content {
        color: #e0e0e0;
        line-height: 1.6;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #ffd700 !important;
        border-bottom: 2px solid #d4af37;
        padding-bottom: 10px;
    }
    
    /* Divider */
    hr {
        border-color: #d4af37 !important;
    }
    
    /* Info/Success/Error Boxes */
    .stInfo {
        border: 2px solid #d4af37 !important;
        background-color: rgba(212, 175, 55, 0.1) !important;
    }
    
    .stSuccess {
        border: 2px solid #4ade80 !important;
    }
    
    .stError {
        border: 2px solid #ef4444 !important;
    }
    
    .stWarning {
        border: 2px solid #fbbf24 !important;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    body { background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%); }
    .hero { text-align: center; padding: 60px 20px; }
    .hero h1 { font-size: 3em; color: #6366f1; margin: 20px 0; }
    .hero p { color: #a0a0b0; font-size: 1.2em; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>💡 Instincts AI</h1>
    <p>Transform raw thoughts into structured solutions</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("🧠 Core Instincts", use_container_width=True):
        st.switch_page("pages/1_core_instincts.py")

with col2:
    if st.button("🎯 Interview Coach", use_container_width=True):
        st.switch_page("pages/2_interview_coach.py")