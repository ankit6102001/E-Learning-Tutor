from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")  
db = client["e_learning_tutor"]
user_interactions = db["user_interactions"]
user_progress = db["user_progress"]

def store_user_interaction(user_id, question, topic):
    if not user_id or not question or not topic:
        raise ValueError("user_id, question, and topic are required.")

    interaction = {
        "user_id": user_id,
        "question": question,
        "topic": topic,
        "timestamp": datetime.now()
    }
    user_interactions.insert_one(interaction)

def get_user_topics(user_id):
    if not user_id:
        raise ValueError("user_id is required.")

    interactions = user_interactions.find({"user_id": user_id})
    topics = [interaction["topic"] for interaction in interactions]
    return list(set(topics))  


def update_user_progress(user_id, topic, num_questions=0, quiz_score=None):
    if not user_id or not topic:
        raise ValueError("user_id and topic are required.")

    progress_data = user_progress.find_one({"user_id": user_id, "topic": topic})
    if progress_data:
        update_data = {
            "$inc": {
                "num_questions": num_questions
            },
            "$push": {"quiz_scores": quiz_score} if quiz_score is not None else {},
            "$set": {"last_accessed": datetime.now()}
        }
        user_progress.update_one({"_id": progress_data["_id"]}, update_data)
    else:
        user_progress.insert_one({
            "user_id": user_id,
            "topic": topic,
            "num_questions": num_questions,
            "quiz_scores": [quiz_score] if quiz_score is not None else [],
            "last_accessed": datetime.now()
        })
def get_user_progress(user_id):
    if not user_id:
        raise ValueError("user_id is required.")

    return list(user_progress.find({"user_id": user_id}))