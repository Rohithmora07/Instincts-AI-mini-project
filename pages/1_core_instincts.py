import streamlit as st
from groq import Groq
import json
from datetime import datetime

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
        border-bottom: 2px solid #d4af37;
        padding-bottom: 12px;
    }
    
    .stTextInput input,
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #d4af37 !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
        font-size: 1em !important;
        padding: 12px !important;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2) !important;
    }
    
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
    
    h2, h3, h4 {
        color: #ffd700 !important;
        border-bottom: 2px solid #d4af37;
        padding-bottom: 10px;
    }
    
    hr {
        border-color: #d4af37 !important;
    }
</style>
""", unsafe_allow_html=True)

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

if "instincts_history" not in st.session_state:
    st.session_state.instincts_history = []

st.markdown("""
<div class="hero-container">
    <div class="hero-title">🧠 Core Instincts</div>
    <div class="hero-subtitle">Your curiosity. Structured. Solved.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("Share your raw thought, curiosity, or passion. We'll structure it using **RICE** (analyze the input) and **STAR** (create actionable solutions).")

st.markdown("---")
st.markdown("### 📝 Share Your Thought")

raw_thought = st.text_area(
    "Your thought:",
    placeholder="e.g., I'm curious about how to balance career growth with learning, or I have a passion for data analysis but don't know where to start...",
    height=120,
    label_visibility="collapsed"
)

st.markdown("---")

if st.button("✨ Structure & Solve", use_container_width=True):
    if not raw_thought or raw_thought.strip() == "":
        st.error("❌ Please share your thought")
    else:
        with st.spinner("🔄 Analyzing..."):
            try:
                prompt = f"""You are a brutally honest advisor analyzing raw thinking. Be SPECIFIC. Be CRITICAL. Vary scores 2-9 range.

**Raw Thought:** {raw_thought}

ANALYZE DEEPLY:
- What assumptions are hidden?
- What gaps exist?
- What are they underestimating?

Return ONLY valid JSON:
{{
    "raw_thought_refined": "Restate exactly what they said",
    "rice_analysis": {{
        "relevance": {{"score": 5, "feedback": "Is this important? Why/why not?"}},
        "integration": {{"score": 4, "feedback": "Does this fit their reality? What context missing?"}},
        "clarity": {{"score": 3, "feedback": "What's unclear? What must they answer first?"}},
        "execution": {{"score": 2, "feedback": "Real barriers? What underestimated?"}}
    }},
    "star_framework": {{
        "situation": "Their ACTUAL current state",
        "task": "The REAL problem they're solving",
        "actions": [
            {{"step": 1, "action": "First action with clear output", "timeframe": "days"}},
            {{"step": 2, "action": "Second action with measurable result", "timeframe": "days"}},
            {{"step": 3, "action": "Third action to test direction", "timeframe": "days"}}
        ],
        "result": "Concrete outcome"
    }},
    "overall_confidence": 60,
    "critical_gaps": ["Gap 1", "Gap 2", "Gap 3"],
    "key_insight": "Honest, uncomfortable insight",
    "red_flags": ["Flag 1", "Flag 2", "Flag 3"],
    "next_steps": ["First: validate", "Then: measure", "Finally: decide"]
}}"""

                response = create_json_completion(prompt)
                
                result_text = response.choices[0].message.content
                json_start = result_text.find("{")
                json_end = result_text.rfind("}") + 1
                
                if json_start == -1:
                    st.error("❌ Parse error. Try again.")
                    st.stop()
                
                analysis = parse_json_response(result_text)
                
                st.session_state.instincts_history.append({
                    "timestamp": datetime.now(),
                    "thought": raw_thought,
                    "analysis": analysis
                })
                
                st.markdown('---')
                st.markdown('<div class="card"><div class="card-title">🎯 Your Structured Insight</div></div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="card" style="margin-top: 0;"><strong>Refined:</strong><br>{analysis.get("raw_thought_refined", "")}</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div class="score-box"><div class="score-number">{analysis.get("overall_confidence", 0)}%</div><div class="score-label">Confidence</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="score-box"><div class="score-number" style="color: #fb923c;">{len(analysis.get("star_framework", {}).get("actions", []))}</div><div class="score-label">Actions</div></div>', unsafe_allow_html=True)
                
                st.markdown("### 🍚 RICE Analysis")
                rice = analysis.get("rice_analysis", {})
                cols = st.columns(4)
                rice_data = [
                    ("Relevance", rice.get("relevance", {})),
                    ("Integration", rice.get("integration", {})),
                    ("Clarity", rice.get("clarity", {})),
                    ("Execution", rice.get("execution", {}))
                ]
                
                for i, (label, data) in enumerate(rice_data):
                    with cols[i]:
                        st.markdown(f'<div class="score-box"><div class="score-number" style="font-size: 2em;">{data.get("score", 0)}</div><div class="score-label">{label}</div></div>', unsafe_allow_html=True)
                        st.caption(data.get("feedback", ""))
                
                st.markdown("### ⭐ STAR Framework")
                star = analysis.get("star_framework", {})
                
                st.markdown(f'<div class="feedback-section"><div class="feedback-title">📍 Situation</div><div class="feedback-content">{star.get("situation", "")}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="feedback-section"><div class="feedback-title">🎯 Task</div><div class="feedback-content">{star.get("task", "")}</div></div>', unsafe_allow_html=True)
                
                st.markdown("**🚀 Action Steps:**")
                for action in star.get("actions", []):
                    st.markdown(f"**Step {action.get('step', 1)}:** {action.get('action', '')}  \n⏱️ *{action.get('timeframe', '')}*")
                
                st.markdown(f'<div class="feedback-section"><div class="feedback-title">✅ Expected Result</div><div class="feedback-content">{star.get("result", "")}</div></div>', unsafe_allow_html=True)
                
                st.markdown("### 💡 Key Insight")
                st.info(analysis.get("key_insight", ""))
                
                st.markdown("### ⚠️ Critical Gaps")
                for gap in analysis.get("critical_gaps", []):
                    st.markdown(f"- {gap}")
                
                st.markdown("### 🚩 Red Flags")
                for flag in analysis.get("red_flags", []):
                    st.markdown(f"- {flag}")
                
                st.markdown("### 📋 Next Steps")
                for i, step in enumerate(analysis.get("next_steps", []), 1):
                    st.markdown(f"**{i}.** {step}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

if st.session_state.instincts_history:
    with st.sidebar:
        st.markdown("### 📚 History")
        for i, item in enumerate(reversed(st.session_state.instincts_history[-5:]), 1):
            with st.expander(f"{i}. {item['thought'][:50]}..."):
                st.write(f"**Refined:** {item['analysis'].get('raw_thought_refined', '')}")
                st.write(f"**Confidence:** {item['analysis'].get('overall_confidence', 0)}%")
