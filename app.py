from flask import Flask, render_template, request, jsonify
from utils.gemini_utils import get_answer, infer_topic
from utils.mongo_utils import store_user_interaction, get_user_topics, update_user_progress, get_user_progress
from utils.recommendations import get_related_topics
from utils.quiz_utils import generate_quiz
from datetime import datetime

app = Flask(__name__)

USER_ID = "user_123"

@app.route("/")
def home():
    progress_data = get_user_progress(USER_ID)
    for progress in progress_data:
        if progress.get("quiz_scores") and progress.get("quizzes_taken"):
            progress["average_score"] = round(sum(progress["quiz_scores"]) / progress["quizzes_taken"], 2)
        else:
            progress["average_score"] = "N/A"
    
    return render_template("index.html", progress_data=progress_data, sum=sum)


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question")
    if not user_input:
        return jsonify({"error": "Please provide a question."}), 400
    answer = get_answer(user_input)

    topic = infer_topic(user_input)
    store_user_interaction(USER_ID, user_input, topic)

    recommendations = get_related_topics(topic)

    return jsonify({
        "answer": answer,
        "recommendations": recommendations
    })

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz_route():
    topic = request.json.get("topic")
    if not topic:
        return jsonify({"error": "Please provide a topic."}), 400
    
    quiz = generate_quiz(topic)
    return jsonify({"quiz": quiz, "topic": topic})  

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    data = request.json
    user_id = data.get("user_id")
    topic = data.get("topic")
    score = data.get("score")
    num_questions = data.get("num_questions")  

    if not user_id or not topic or score is None or num_questions is None:
        return jsonify({"error": "Invalid data provided."}), 400

    update_user_progress(user_id, topic, num_questions=num_questions, quiz_score=score)

    progress_data = get_user_progress(user_id)
    for progress in progress_data:
        if progress["topic"] == topic:
            return jsonify({
                "success": True,
                "topic": topic,
                "num_questions": progress["num_questions"],
                "quiz_score": score,
                "last_accessed": progress["last_accessed"].strftime('%Y-%m-%d %H:%M')
            })

    return jsonify({"error": "Progress data not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)