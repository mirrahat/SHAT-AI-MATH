from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI
import os
import textstat
from datetime import datetime

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model_id = os.getenv("FINE_TUNED_MODEL")

client = OpenAI(api_key=api_key)
app = Flask(__name__)

def evaluate_structure(question):
    options = ["A)", "B)", "C)", "D)"]
    return all(opt in question for opt in options)

def grammar_and_readability_score(text):
    flesch_score = textstat.flesch_reading_ease(text)
    grade_level = textstat.flesch_kincaid_grade(text)
    return {
        "readability_score": flesch_score,
        "estimated_grade_level": grade_level
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt")

        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}]
            )

            question = response.choices[0].message.content.strip()
            structure_ok = evaluate_structure(question)
            readability = grammar_and_readability_score(question)

            return render_template("index.html", prompt=prompt, question=question, evaluation={
                "structure_valid": structure_ok,
                **readability
            })

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
