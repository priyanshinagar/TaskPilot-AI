import google.generativeai as genai
from flask import Flask, render_template, request
from datetime import date

genai.configure(api_key="AQ.Ab8RN6K0FNmwk3dLYEYjnjcog57VikzVPkkhrNF8bWNKnMx_IA")

model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    task = request.form["task"]
    deadline = request.form["deadline"]
    priority = request.form["priority"]
    today = date.today()

    prompt = f"""
    Today's Date: {today}

You are TaskPilot AI, an intelligent productivity assistant.

Task: {task}
Deadline: {deadline}
Priority: {priority}

Today's date should be considered while creating the plan.

Instructions:
- First calculate how many days are left until the deadline.
- Base the entire plan ONLY on the remaining time.
- If only a few days are left, give an intensive short plan.
- If a few weeks are left, divide the work week-wise.
- If months are left, divide it month-wise.
- Never create a 1-year or 2-year roadmap unless the deadline is actually that far away.
- Mention approximately how many days are left.

Return ONLY HTML.

Use this structure:

<h2>📊 Task Analysis</h2>

<h3>⏳ Time Remaining</h3>
<p>...</p>

<h3>⏱ Estimated Study Time</h3>
<p>...</p>

<h3>📈 Difficulty</h3>
<p>...</p>

<h3>📅 Personalized Plan</h3>
<ul>
<li>...</li>
<li>...</li>
<li>...</li>
</ul>

<h3>💡 Motivation</h3>
<p>...</p>

Do not use Markdown.
Do not use **, ### or backticks.
Only HTML.
"""
    response = model.generate_content(prompt)

    return render_template(
        "result.html",
        task=task,
        deadline=deadline,
        priority=priority,
        response=response.text
    )


if __name__ == "__main__":
    app.run(debug=True)