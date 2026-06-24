# 💡 Instincts AI

Transform raw thoughts into structured solutions using RICE & STAR frameworks.

## 🎯 Core Vision

**Instincts AI** is built on a simple belief: *When humans think of doing anything, they're curious, interested, or passionate. All they need is structure.*

This app turns your raw thoughts, ideas, and curiosities into actionable plans using two proven frameworks:

- **RICE** (Input Analysis): Structures your initial thought
- **STAR** (Output Feedback): Creates a solution path

## ✨ Features

### 🧠 Core Instincts (Main Feature)
- **Raw Thought Input**: Type or speak your curiosity
- **RICE Analysis**: Relevance, Integration, Clarity, Execution breakdown
- **STAR Framework**: Situation → Task → Action → Result
- **Audio Support**: Listen to your analysis (Text-to-Speech)
- **Instant Feedback**: Get structured insights in seconds

### 🎯 Interview Coach (Secondary Feature)
- Practice interview responses
- RICE framework for input analysis
- STAR framework for output feedback
- Detailed performance scoring
- Actionable improvement suggestions

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/Rohithmora07/Instincts_AI.git
cd Instincts_AI
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Secrets
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-groq-api-key"
```

Get your Groq API key at: https://console.groq.com/

### 5. Run the App
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 📋 How to Use

### Core Instincts
1. **Share your thought**: Type or speak your raw idea
2. **Get structured**: RICE framework analyzes your input
3. **Discover solutions**: STAR framework creates action steps
4. **Listen back**: Optional audio narration of your analysis

### Interview Coach
1. **Select job role**: Choose your target position
2. **Paste question**: Add the interview question
3. **Provide answer**: Type your response
4. **Get feedback**: Instant RICE & STAR analysis

---

## 🔧 Tech Stack

- **Frontend**: Streamlit (Python)
- **LLM**: Groq (Llama 3.3 70B)
- **Speech-to-Text**: Google Speech Recognition
- **Text-to-Speech**: Google Cloud Text-to-Speech API
- **Styling**: Custom CSS + Streamlit components

---

## 📦 Project Structure

```
Instincts_AI/
├── app.py                      # Main app navigation
├── pages/
│   ├── 1_core_instincts.py    # Raw thought → RICE → STAR
│   └── 2_interview_coach.py   # Interview practice & analysis
├── .streamlit/
│   └── secrets.toml           # API keys (create this)
├── requirements.txt           # Dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

---

## 🎓 Frameworks Explained

### RICE Framework (Input Analysis)
- **Relevance** (R): How well does this connect to your goals?
- **Integration** (I): How does this fit your current situation?
- **Clarity** (C): Is your thought clear and well-articulated?
- **Execution** (E): What's needed to act on this?

### STAR Framework (Solution Development)
- **Situation** (S): What's your current state?
- **Task** (T): What's your main goal or challenge?
- **Action** (A): What concrete steps will you take?
- **Result** (R): What's the expected outcome?

---

## 🔐 API Keys Required

### Groq API (Required)
1. Go to https://console.groq.com/
2. Sign up for a free account
3. Create an API key
4. Add to `.streamlit/secrets.toml`

### Google Cloud (Optional - for Text-to-Speech)
1. Create a Google Cloud project
2. Enable Text-to-Speech API
3. Create service account credentials
4. Download JSON key and add path to environment

---

## 💡 Example Use Cases

### Core Instincts
- *"I'm interested in data analysis but don't know where to start"*
- *"I want to balance learning and earning"*
- *"How do I improve my public speaking?"*
- *"What should my career path look like?"*

### Interview Coach
- Practice for Data Analyst interviews
- Prepare STAR answers for behavioral questions
- Get instant feedback on technical explanations
- Improve clarity and structure

---

## 🛣️ Roadmap

- [ ] Multi-language support
- [ ] Persistent database (save analyses)
- [ ] Progress tracking over time
- [ ] Custom framework creation
- [ ] Team collaboration features
- [ ] Export insights as PDF/DOCX
- [ ] Mobile app

---

## 🤝 Contributing

Found a bug or have an idea? Issues and PRs welcome!

---

## 📄 License

MIT License - see LICENSE file

---

## 👤 Author

Built by **Rohith Mora** ([GitHub](https://github.com/Rohithmora07))

*Final year B.Tech AI student | Data Analytics + Gen AI Enthusiast*

---

## ❤️ Acknowledgments

- Groq for incredible LLM inference
- Streamlit for making app development simple
- Google Cloud for speech & text APIs

---

## 📞 Support

Have questions? 
- Check the [Issues](https://github.com/Rohithmora07/Instincts_AI/issues) section
- Start a [Discussion](https://github.com/Rohithmora07/Instincts_AI/discussions)

---

**Remember**: Your instincts are right. You just need structure to turn them into reality. 🚀
