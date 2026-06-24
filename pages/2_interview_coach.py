import streamlit as st
from groq import Groq
import json
from datetime import datetime
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
# Initialize Groq client
@st.cache_resource
def init_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = init_groq_client()

def create_json_completion(prompt):
    completion_args = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 2048,
        "response_format": {"type": "json_object"},
    }

    try:
        return client.chat.completions.create(**completion_args)
    except TypeError:
        completion_args.pop("response_format", None)
        return client.chat.completions.create(**completion_args)
    except Exception as e:
        message = str(e).lower()
        if "response_format" not in message and "json" not in message:
            raise

        completion_args.pop("response_format", None)
        return client.chat.completions.create(**completion_args)

def parse_json_response(result_text):
    json_start = result_text.find("{")
    if json_start == -1:
        raise ValueError("Could not find a JSON object in the model response.")

    decoder = json.JSONDecoder()
    return decoder.raw_decode(result_text[json_start:])[0]

# Initialize session state
if "interview_history" not in st.session_state:
    st.session_state.interview_history = []

# Page title
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🎯 Interview Coach</div>
    <div class="hero-subtitle">Master RICE & STAR frameworks for interview success</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
Practice your interview responses and get instant feedback using **RICE** (input analysis) 
and **STAR** (output feedback) frameworks.
""")

# Main Layout
col1, col2 = st.columns([1, 1], gap="large")

# LEFT COLUMN: Input Section
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📋 Interview Setup</div>', unsafe_allow_html=True)
    
    # Job Role Selection
    role = st.selectbox(
        "Target Job Role",
        [
            "Data Analyst",
            "Data Engineer",
            "Business Analyst",
            "Product Manager",
            "Software Engineer",
            "ML Engineer",
            "Other"
        ],
        help="Select the position you're interviewing for"
    )
    
    if role == "Other":
        role = st.text_input("Specify your role:")
    
    # Interview Question
    st.markdown("**Interview Question**")
    question = st.text_area(
        "Paste the interview question here",
        placeholder="e.g., How will you clean raw data? Walk me through your approach...",
        height=100,
        label_visibility="collapsed"
    )
    
    # Your Response
    st.markdown("**Your Response (Spoken or Transcribed)**")
    answer = st.text_area(
        "Paste your response here",
        placeholder="Provide your full interview answer here...",
        height=120,
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN: Framework Guide
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚡ Framework Guide</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **RICE Framework (Input Analysis)**
    - **R**elevance: How well does your answer address the question?
    - **I**ntegration: How do you connect concepts together?
    - **C**larity: How clearly do you explain your approach?
    - **E**xecution: Is your method practical and actionable?
    
    **STAR Framework (Output Feedback)**
    - **S**ituation: Do you set proper context?
    - **T**ask: Is the goal or challenge clear?
    - **A**ction: Are your steps concrete and specific?
    - **R**esult: Do you show measurable outcomes?
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis Button
st.markdown('<div style="text-align: center; margin: 40px 0;">', unsafe_allow_html=True)

if st.button("🚀 Analyze My Response", use_container_width=True):
    if not role or not question or not answer:
        st.error("❌ Please fill in all fields: Job Role, Question, and Response")
    else:
        with st.spinner("🔄 Analyzing your response using RICE and STAR frameworks..."):
            try:
                # Build analysis prompt
                prompt = f"""You are an expert interview coach. Analyze this interview response using RICE and STAR frameworks.

**Target Job Role:** {role}
**Interview Question:** {question}
**Candidate's Response:** {answer}

Return ONLY valid JSON (no markdown, no explanation, no extra text):
{{
    "rice_analysis": {{
        "relevance": {{"score": 8, "feedback": "specific feedback"}},
        "integration": {{"score": 7, "feedback": "specific feedback"}},
        "clarity": {{"score": 8, "feedback": "specific feedback"}},
        "execution": {{"score": 8, "feedback": "specific feedback"}}
    }},
    "star_analysis": {{
        "situation": {{"score": 8, "feedback": "specific feedback"}},
        "task": {{"score": 7, "feedback": "specific feedback"}},
        "action": {{"score": 8, "feedback": "specific feedback"}},
        "result": {{"score": 8, "feedback": "specific feedback"}}
    }},
    "overall_score": 78,
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "improvements": ["area 1", "area 2", "area 3"],
    "action_items": ["action 1", "action 2", "action 3"]
}}"""

                # Call Groq API
                response = create_json_completion(prompt)
                
                result_text = response.choices[0].message.content
                
                # Parse JSON with better error handling
                try:
                    json_start = result_text.find("{")
                    json_end = result_text.rfind("}") + 1
                    
                    if json_start == -1 or json_end == 0:
                        st.error("❌ Could not find JSON in response. Please try again.")
                        st.stop()
                    
                    json_str = result_text[json_start:json_end]
                    analysis = parse_json_response(result_text)
                    
                except json.JSONDecodeError as e:
                    st.error(f"❌ Error parsing JSON: {str(e)}")
                    st.info(f"Response received: {result_text[:500]}...")
                    st.stop()
                
                # Save to history
                st.session_state.interview_history.append({
                    "timestamp": datetime.now(),
                    "role": role,
                    "question": question,
                    "analysis": analysis
                })
                
                # Display Results
                st.markdown('---')
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f'<div class="card-title">📊 Analysis Results</div>', unsafe_allow_html=True)
                
                # Overall Score
                overall = analysis.get("overall_score", 0)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="score-box">
                        <div class="score-number">{overall}</div>
                        <div class="score-label">Overall Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # RICE Average
                rice_scores = [
                    analysis["rice_analysis"]["relevance"]["score"],
                    analysis["rice_analysis"]["integration"]["score"],
                    analysis["rice_analysis"]["clarity"]["score"],
                    analysis["rice_analysis"]["execution"]["score"]
                ]
                rice_avg = sum(rice_scores) / len(rice_scores)
                
                with col2:
                    st.markdown(f"""
                    <div class="score-box">
                        <div class="score-number">{rice_avg:.1f}</div>
                        <div class="score-label">RICE Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # STAR Average
                star_scores = [
                    analysis["star_analysis"]["situation"]["score"],
                    analysis["star_analysis"]["task"]["score"],
                    analysis["star_analysis"]["action"]["score"],
                    analysis["star_analysis"]["result"]["score"]
                ]
                star_avg = sum(star_scores) / len(star_scores)
                
                with col3:
                    st.markdown(f"""
                    <div class="score-box">
                        <div class="score-number">{star_avg:.1f}</div>
                        <div class="score-label">STAR Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Detailed Breakdown
                col_rice, col_star = st.columns(2, gap="large")
                
                # RICE Framework Details
                with col_rice:
                    st.markdown("""
                    <div class="card">
                        <div class="card-title">
                            <span class="rice-badge">RICE</span>Input Analysis
                        </div>
                    """, unsafe_allow_html=True)
                    
                    rice = analysis["rice_analysis"]
                    for key, data in rice.items():
                        score = data["score"]
                        feedback = data["feedback"]
                        st.markdown(f"""
                        <div class="feedback-section">
                            <div class="feedback-title">{key.replace('_', ' ').title()} ({score}/10)</div>
                            <div class="feedback-content">{feedback}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # STAR Framework Details
                with col_star:
                    st.markdown("""
                    <div class="card">
                        <div class="card-title">
                            <span class="star-badge">STAR</span>Output Feedback
                        </div>
                    """, unsafe_allow_html=True)
                    
                    star = analysis["star_analysis"]
                    for key, data in star.items():
                        score = data["score"]
                        feedback = data["feedback"]
                        st.markdown(f"""
                        <div class="feedback-section" style="border-left-color: #fb923c;">
                            <div class="feedback-title" style="color: #fb923c;">{key.replace('_', ' ').title()} ({score}/10)</div>
                            <div class="feedback-content">{feedback}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Strengths & Improvements
                col_strength, col_improve = st.columns(2, gap="large")
                
                with col_strength:
                    st.markdown("""
                    <div class="card">
                        <div class="card-title">✅ Strengths</div>
                    """, unsafe_allow_html=True)
                    for strength in analysis.get("strengths", []):
                        st.markdown(f'- {strength}')
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_improve:
                    st.markdown("""
                    <div class="card">
                        <div class="card-title">🎯 Areas to Improve</div>
                    """, unsafe_allow_html=True)
                    for improvement in analysis.get("improvements", []):
                        st.markdown(f'- {improvement}')
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Action Items
                st.markdown("""
                <div class="card">
                    <div class="card-title">🚀 Next Steps</div>
                """, unsafe_allow_html=True)
                for i, action in enumerate(analysis.get("action_items", []), 1):
                    st.markdown(f'**{i}.** {action}')
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    ❌ <strong>Error during analysis:</strong> {str(e)}
                </div>
                """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style="text-align: center; color: #808090; font-size: 0.9em; margin-top: 40px;">
    Interview Intelligence Coach | Powered by Groq + Llama 3.3 | Built with Streamlit
</div>
""", unsafe_allow_html=True)
