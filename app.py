from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os, json

def load_env():
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip()
    except FileNotFoundError:
        pass

load_env()

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not found. Add it to your .env file.")

app = Flask(__name__, static_folder='.')
CORS(app)

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=GITHUB_TOKEN,
    timeout=120.0,
)

ROADMAP_SYSTEM_PROMPT = """You are PathfinderAI, an expert career and study mentor for Computer Science students worldwide.

You MUST reason step by step before generating the roadmap. Show your thinking clearly.

Respond in this EXACT JSON format with NO extra text:
{
  "reasoning": {
    "step1_profile": "Your analysis of the student's current situation in 2-3 sentences",
    "step2_gaps": "What specific skills are missing and why they matter for the goal",
    "step3_strategy": "Your strategic approach for this specific student",
    "step4_timeline": "How you decided to structure the timeline and why"
  },
  "studentName": "string",
  "goal": "string",
  "timelineWeeks": number,
  "summary": "2-3 sentence personalized summary",
  "roadmapDescription": "3-4 sentence description of what this roadmap covers, why it's structured this way, and what the student will achieve by the end",
  "gapAnalysis": [
    {
      "skill": "Skill name",
      "currentPercent": 10,
      "targetPercent": 80,
      "reason": "Why this skill matters for the goal"
    }
  ],
  "weeks": [
    {
      "weekNumber": 1,
      "title": "Week title",
      "focus": "What this week is about in 1-2 sentences",
      "tasks": ["specific task 1", "specific task 2", "specific task 3"],
      "resources": [
        {"name": "Resource name", "url": "https://...", "type": "YouTube/Website/Course"}
      ],
      "milestone": "Exactly what you can do by end of this week"
    }
  ],
  "tips": ["tip1", "tip2", "tip3", "tip4"],
  "motivationalMessage": "A warm, personalized message addressing the student by name"
}

Rules:
- currentPercent = honest estimate based on student's stated skills (not 0 if they listed it)
- Only FREE resources (YouTube, GeeksforGeeks, NPTEL, LeetCode free, etc.)
- Be specific, not vague. 4-12 weeks based on timeline.
- reasoning steps must be genuine analysis"""

CHAT_SYSTEM_PROMPT = """You are PathfinderAI, a friendly and expert career mentor for Computer Science students worldwide.

You have access to the student's profile and their generated roadmap (if available).

You can help with:
1. Questions about their specific roadmap (e.g. "explain week 3", "what should I do first?")
2. General career advice for Indian CS students (placements, GATE, MS abroad, DSA tips, etc.)
3. Resource recommendations (always free)
4. Motivation and study tips
5. Explaining technical concepts simply

Rules:
- Be warm, encouraging, and specific
- Always give actionable advice
- Keep responses concise (3-5 sentences max unless explaining something technical)
- Reference their roadmap/profile when relevant
- Use simple language (they are a beginner)
- If asked about paid resources, suggest free alternatives"""


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/generate-roadmap', methods=['POST'])
def generate_roadmap():
    try:
        data = request.json
        name = (data.get('name') or '').strip()
        skills = (data.get('skills') or '').strip()
        goals = data.get('goals', [])
        skillsToLearn = data.get('skillsToLearn', [])

        if not name:
            return jsonify({"success": False, "error": "Please enter your name."}), 400
        if not skills:
            return jsonify({"success": False, "error": "Please enter your current skills."}), 400
        if not goals:
            return jsonify({"success": False, "error": "Please select at least one goal."}), 400

        goals_str = ", ".join(goals)
        skills_to_learn_str = ", ".join(skillsToLearn) if skillsToLearn else "Not specified"
        current_country = data.get('currentCountry') or 'Not specified'
        aspiring_country = data.get('aspiringCountry') or 'Not specified'

        user_message = f"""
Student Profile:
- Name: {name}
- Year: {data.get('year', '1st Year')} CSE at {data.get('college', 'Not specified')}
- Currently in: {current_country}
- Wants to work/settle in: {aspiring_country}
- Current Skills: {skills}
- Goals: {goals_str}
- Skills they want to build: {skills_to_learn_str}
- Target: {data.get('target', 'Not specified')}
- Study Time: {data.get('hoursPerDay', '2')} hours per day
- Timeline: {data.get('timeline', '3')} months
- Extra context: {data.get('context', 'None')}

Important: Tailor the roadmap to their country context. If aspiring country differs from current, include relevant advice (visa requirements awareness, country-specific job market, relevant certifications). Use resources and platforms popular in their region. They have MULTIPLE goals — structure the roadmap to cover all of them intelligently. Return only valid JSON.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": ROADMAP_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=4000,
        )

        raw = response.choices[0].message.content.strip()
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()

        roadmap = json.loads(raw)
        return jsonify({"success": True, "roadmap": roadmap})

    except json.JSONDecodeError:
        return jsonify({"success": False, "error": "AI response could not be parsed. Please try again."}), 500
    except Exception as e:
        error_msg = str(e)
        if "timeout" in error_msg.lower():
            return jsonify({"success": False, "error": "AI took too long. Please try again."}), 504
        return jsonify({"success": False, "error": "Something went wrong. Please try again."}), 500


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        messages = data.get('messages', [])
        profile = data.get('profile', {})
        roadmap = data.get('roadmap', None)

        system = CHAT_SYSTEM_PROMPT

        if profile:
            country_info = ''
            if profile.get('currentCountry'):
                country_info += f"\n- Currently in: {profile.get('currentCountry')}"
            if profile.get('aspiringCountry'):
                country_info += f"\n- Wants to work/settle in: {profile.get('aspiringCountry')}"
            system += f"\n\nStudent Profile:\n- Name: {profile.get('name')}\n- Year: {profile.get('year')} at {profile.get('college')}{country_info}\n- Current Skills: {profile.get('skills')}\n- Goals: {', '.join(profile.get('goals', []))}\n- Skills to build: {', '.join(profile.get('skillsToLearn', []))}\n- Study time: {profile.get('hoursPerDay')} hrs/day"

        if roadmap:
            weeks_summary = "\n".join([f"Week {w['weekNumber']}: {w['title']} — {w['focus']}" for w in roadmap.get('weeks', [])])
            system += f"\n\nTheir Generated Roadmap Summary:\n{weeks_summary}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}] + messages,
            temperature=0.7,
            max_tokens=600,
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"success": True, "reply": reply})

    except Exception as e:
        return jsonify({"success": False, "error": "Chat error. Please try again."}), 500


if __name__ == '__main__':
    print("🚀 PathfinderAI is running at http://localhost:5000")
    app.run(debug=True, port=5000)
