import google.generativeai as genai

api_key = ''
genai.configure(api_key=api_key)

def generate_quiz(topic):
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Generate 3 multiple-choice questions about {topic}. Format each question as: Q1. [Question] A) [Option 1] B) [Option 2] C) [Option 3] D) [Option 4] Correct Answer: [Letter]"
        response = model.generate_content(prompt)
        quiz_data = []
        questions = response.text.strip().split("\n\n")  
        for question in questions:
            lines = question.split("\n")
            if len(lines) >= 6:  
                q_text = lines[0].strip()  
                options = [line.strip() for line in lines[1:5]]  
                correct_answer = lines[5].split(":")[1].strip()  
                quiz_data.append({
                    "question": q_text,
                    "options": options,
                    "correct_answer": correct_answer
                })
        return quiz_data
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return []
def evaluate_answer(question, user_answer):
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Is the answer '{user_answer}' correct for the question: {question}? Respond with 'Correct' or 'Incorrect'."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error evaluating answer: {e}")
        return "Error evaluating answer."