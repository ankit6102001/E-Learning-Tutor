import google.generativeai as genai

api_key = ''
genai.configure(api_key=api_key)

def get_related_topics(topic):
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Generate a list of 3-5 related topics for: {topic}"
        response = model.generate_content(prompt)
        related_topics = response.text.strip().split("\n")  
        return [t.replace("-", "").strip() for t in related_topics] 
    except Exception as e:
        print(f"Error generating related topics: {e}")
        return []