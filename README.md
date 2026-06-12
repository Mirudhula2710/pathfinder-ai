# 🧭 PathfinderAI — Your CS Career Roadmap, Personalized.

> **Microsoft Agents League Hackathon 2026** — Built by Mirudhula B, 1st Year CSE, SRMIST

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20App-7c6af7?style=for-the-badge)](https://pathfinder-ai-mirudhula-chlj26ysr-mirudhula2710s-projects.vercel.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/Mirudhula2710/pathfinder-ai)
[![Powered by](https://img.shields.io/badge/Powered%20by-GitHub%20Models%20%7C%20Azure%20AI%20Foundry-0078d4?style=for-the-badge&logo=microsoft)](https://github.com/marketplace/models)

---

## 🎯 The Problem

Every year, hundreds of thousands of Computer Science students graduate without a clear path to their goals. Career counselling is expensive. Generic roadmaps online don't account for your current skills, your available time, your country, or your specific goals.

**Students are left guessing what to study, in what order, and from where.**

This problem is especially acute for students in developing countries — where access to mentorship is limited and the stakes of getting it wrong are high.

---

## 💡 The Solution

**PathfinderAI** is a free, AI-powered career mentor that generates a fully personalized, week-by-week learning roadmap for any CS student — anywhere in the world.

In under 30 seconds, it:
- Analyses your current skill level honestly
- Identifies your exact skill gaps
- Maps the best **free resources** to fill those gaps
- Builds a realistic **week-by-week plan** tailored to your available study hours
- Shows you **how the AI reasoned** about your profile (transparent multi-step thinking)
- Provides a built-in **career chatbot** for ongoing guidance

---

## 🤖 How the AI Agent Works

PathfinderAI uses a **multi-step reasoning agent** built on GPT-4o-mini via GitHub Models (Azure AI Foundry):

```
Step 1 — Profile Analysis
    ↓ Understands the student's current situation, skills, country context
Step 2 — Gap Analysis  
    ↓ Identifies exactly what skills are missing and why they matter
Step 3 — Strategy Formation
    ↓ Decides the optimal learning approach for this specific student
Step 4 — Timeline Construction
    ↓ Builds a realistic week-by-week plan based on available hours
    ↓
OUTPUT: Personalized roadmap with tasks, free resources, milestones
```

Every reasoning step is **shown to the user** — not hidden — making the agent transparent and trustworthy.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🧠 **Multi-step Reasoning** | 4 visible AI reasoning steps shown for every roadmap |
| 🎯 **Multi-goal Support** | Select multiple goals — AI combines them into one roadmap |
| 🌍 **Global & Country-aware** | Tailors advice based on current country and aspiring country |
| 📊 **Skill Gap Analysis** | Animated progress bars showing current vs target skill levels |
| 📅 **Week-by-Week Plan** | Detailed tasks, free resources, and milestones per week |
| ✅ **Task Checkboxes** | Track your progress by checking off completed tasks |
| 💬 **AI Career Chatbot** | Built-in chatbot for roadmap questions and general career advice |
| ✏️ **Custom Goals & Skills** | Add your own goals and skills beyond the preset options |
| 🔗 **Clickable Resources** | Every resource card shows title, type, domain, and opens in new tab |
| 📱 **Mobile Friendly** | Fully responsive design works on all screen sizes |
| 🆓 **Completely Free** | Only recommends free resources — no paid courses ever |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              Frontend (HTML/CSS/JS)          │
│  - Student profile form                      │
│  - Multi-select goals & skills chips         │
│  - Country selector                          │
│  - Roadmap display with reasoning panel      │
│  - AI chatbot interface                      │
└──────────────────┬──────────────────────────┘
                   │ HTTP POST /generate-roadmap
                   │ HTTP POST /chat
┌──────────────────▼──────────────────────────┐
│           Backend (Python + Flask)           │
│  - Input validation                          │
│  - Prompt engineering                        │
│  - JSON response parsing                     │
│  - Error handling & timeout management       │
└──────────────────┬──────────────────────────┘
                   │ OpenAI SDK
┌──────────────────▼──────────────────────────┐
│     GitHub Models — Azure AI Foundry         │
│     Model: GPT-4o-mini                       │
│     Endpoint: models.inference.ai.azure.com  │
│     Microsoft IQ Layer: Foundry IQ ✅        │
└─────────────────────────────────────────────┘
```

---

## 🔧 Microsoft IQ Integration

This project uses **Foundry IQ** via GitHub Models, which is powered by Azure AI Foundry:

- **Endpoint:** `https://models.inference.ai.azure.com`
- **Model:** `gpt-4o-mini`
- **SDK:** OpenAI Python SDK with Azure AI Foundry base URL
- **Features used:** Multi-turn chat, structured JSON output, system prompts, multi-step reasoning

---

## 🚀 Run Locally

### Prerequisites
- Python 3.8+
- GitHub account (for free API token)

### Setup

**1. Clone the repository**
```bash
git clone https://github.com/Mirudhula2710/pathfinder-ai.git
cd pathfinder-ai
```

**2. Install dependencies**
```bash
pip install flask flask-cors openai
```

**3. Get your free GitHub Models token**
- Go to https://github.com/marketplace/models
- Click your profile → Settings → Developer settings → Personal access tokens
- Generate a new token (classic) with `read:user` scope

**4. Create your .env file**
```
GITHUB_TOKEN=ghp_your_token_here
```

**5. Run the app**
```bash
python app.py
```

**6. Open in browser**
```
http://localhost:5000
```

---

## 📁 Project Structure

```
pathfinder-ai/
├── app.py              # Flask backend — routes, AI agent, chat endpoint
├── index.html          # Complete frontend — UI, form, roadmap display, chatbot
├── requirements.txt    # Python dependencies
├── .gitignore          # Protects .env from being committed
└── README.md           # This file
```

---

## 🎯 Hackathon Track

**Track:** Creative Apps + Reasoning Agents

**Why Creative Apps:** PathfinderAI is a novel application of AI reasoning to solve a real human problem — career guidance for students who can't afford a mentor.

**Why Reasoning Agents:** The core of PathfinderAI is a transparent multi-step reasoning agent that visibly thinks through a student's profile before generating output — not a simple prompt-response system.

---

## 👩‍💻 About the Builder

**Mirudhula B** — 1st Year Computer Science Engineering student at SRMIST, Chennai, India.

I built PathfinderAI because I am the target user. As a first-year student, I had no idea what to study, in what order, or how to reach my goals. I searched for a tool like this and couldn't find one that was free, personalized, and actually understood my situation as a student in India.

So I built it during the Microsoft Agents League Hackathon 2026 — my first ever hackathon — going from zero knowledge of AI APIs to a fully deployed application in 10 days.

---

## 🌐 Live Demo

👉 **[https://pathfinder-ai-mirudhula-chlj26ysr-mirudhula2710s-projects.vercel.app/](https://pathfinder-ai-mirudhula-chlj26ysr-mirudhula2710s-projects.vercel.app/)**

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built with 💜 for the Microsoft Agents League Hackathon 2026*
