import google.generativeai as genai
import markdown

api_key = ''
genai.configure(api_key=api_key)

def get_answer(question):
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(question)
        
        html_response = markdown.markdown(response.text)
        return html_response
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {str(e)}"

def infer_topic(question):
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Identify the main topic of the following question: {question}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error inferring topic: {e}")
        return "General"        