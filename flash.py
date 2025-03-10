from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

# Create Flask app with CORS support
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('flash.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        # Instead of using OpenAI API, just return a simple response
        response = get_simple_ai_response(msg)
        return response
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

def get_simple_ai_response(text):
    """Generate a simple AI response without using external APIs."""
    # Simple response logic based on keywords
    text = text.lower()
    
    if "hello" in text or "hi" in text or "hey" in text:
        return "Hello! I'm your AI Academic Advisor. How can I help you today?"
    
    elif "who are you" in text or "what are you" in text:
        return "I'm an AI Academic Advisor, here to help answer your questions about courses, academics, and university life."
    
    elif "course" in text or "class" in text:
        return "I can help you find information about courses. What specific course or subject are you interested in?"
    
    elif "major" in text or "degree" in text:
        return "There are many exciting majors to choose from! What subjects are you most interested in?"
    
    elif "deadline" in text or "due date" in text or "when" in text:
        current_date = datetime.now()
        return f"Today is {current_date.strftime('%B %d, %Y')}. Most academic deadlines can be found on the university calendar. What specific deadline are you looking for?"
    
    elif "thank" in text:
        return "You're welcome! Feel free to ask if you have any other questions."
    
    elif "bye" in text or "goodbye" in text:
        return "Goodbye! Feel free to come back if you have more questions."
    
    else:
        return f"I received your message: '{text}'. As an academic advisor, I'm here to help with your educational questions. Could you provide more details about what you'd like to know?"

if __name__ == '__main__':
    print("Starting Flask application...")
    # Set host to '0.0.0.0' to make it accessible from any IP and specify port 5000 explicitly
    app.run(host='0.0.0.0', port=5500, debug=True)