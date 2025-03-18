from flask import Flask, render_template, request, jsonify
import random
import os

# Create Flask app
app = Flask(__name__, template_folder=".")

# Basic academic Q&A responses
academic_responses = {
    "courses": [
        "We offer a wide range of courses across multiple disciplines. Could you specify which department you're interested in?",
        "Our course catalog includes both undergraduate and graduate options. Are you looking for a specific level or subject area?",
        "Popular courses this semester include Data Science 101, Introduction to Psychology, and Business Ethics. Would you like more information on any of these?"
    ],
    "majors": [
        "We offer over 50 undergraduate majors and 30 graduate programs. Some popular choices include Computer Science, Business Administration, and Psychology.",
        "Our most competitive majors include Engineering, Nursing, and Computer Science. Each has specific admission requirements.",
        "When choosing a major, consider your interests, career goals, and academic strengths. Would you like to discuss a specific major?"
    ],
    "registration": [
        "Registration for the next semester typically opens 2 months before classes begin. Current students register based on credit hours completed.",
        "To register for classes, log in to the student portal and use the course registration tool. You'll need your student ID and password.",
        "Registration deadlines are strictly enforced. Late registration may result in additional fees."
    ],
    "deadlines": [
        "Important upcoming deadlines: Course registration (April 15), Tuition payment (August 1), Drop/Add period (First two weeks of semester).",
        "Scholarship application deadlines vary by program, but most university scholarships are due by February 1 for the following academic year.",
        "Thesis and dissertation submission deadlines are posted on the graduate school website."
    ],
    "financial_aid": [
        "Financial aid options include grants, scholarships, work-study, and loans. Have you submitted your FAFSA yet?",
        "Scholarship applications are evaluated based on academic achievement, financial need, and sometimes specific criteria set by donors.",
        "Our financial aid office offers one-on-one counseling to help students maximize their aid packages and minimize debt."
    ],
    "campus": [
        "Campus resources include the library, tutoring center, writing center, counseling services, and career center. All are free for enrolled students.",
        "The student health center provides medical care, mental health services, and wellness programs.",
        "Our library offers 24/7 access during finals week, with librarians available to help with research questions."
    ],
    "specific_courses": {
        "cs35101": "CS 35101 - Computer Organization\n\nCredits: 3\n\nDescription: Computer system organization, including performance measures, instruction sets, computer arithmetic, central processing unit, pipelining, memory hierarchy and parallel processors.\n\nPrerequisites: Minimum C grade in the following courses: CS 10062 or CS 13001; or CS 13011 and CS 13012.\n\nOffered: Fall, Spring, Summer",
        
        "cs23022": "CS 23022 - Discrete Structures for Computer Science\n\nCredits: 3\n\nDescription: Discrete structures for computer scientists with a focus on: mathematical reasoning, combinatorial analysis, discrete structures, algorithmic thinking, applications and modeling.\n\nPrerequisites: Minimum C grade in MATH 11009 or MATH 11010 or MATH 11022, or ALEKS score of 78.\n\nOffered: Fall, Spring, Summer",
        
        "cs10051": "CS 10051 - Computer Science Principles\n\nCredits: 3\n\nDescription: An introductory, broad and hands-on coverage of aspects of computer science, including algorithms, problem solving, operating systems concepts, computer architecture, programming languages and modern applications. Three-credit lecture with one-credit lab.\n\nPrerequisites: None\n\nOffered: Fall, Spring",
        
        "bsci10001": "BSCI 10001 - Human Biology\n\nCredits: 3\n\nDescription: Study of the scientific method and life's properties, emphasizing human biology. Topics include energy, genetics, reproduction, development disease, nutrition and physical fitness in humans. This course may not be used to fulfill major or minor requirements in the following programs: B.A. Biology, B.S. Biology, B.S. Biotechnology, B.S. Botany, B.S. Environmental and Conservation Biology, B.S. Medical Laboratory Science, B.S. Zoology and the Biological Sciences minor.\n\nPrerequisites: None\n\nOffered: Fall",
        
        "bsci10002": "BSCI 10002 - Life on Planet Earth\n\nCredits: 3\n\nDescription: Explores the fascinating breadth of life on Earth including the unique ecology and survival strategies of animals, plants and microbes in their natural habitats. This course may not be used to fulfill major or minor requirements in the following programs: B.A. Biology, B.S. Biology, B.S. Biotechnology, B.S. Botany, B.S. Environmental and Conservation Biology, B.S. Medical Laboratory Science, B.S. Zoology and the Biological Sciences minor.\n\nPrerequisites: None\n\nOffered: Fall, Spring"
    },
    "default": [
        "I'm here to help with academic questions. Could you provide more details about what you're looking for?",
        "That's an interesting question. Let me connect you with the appropriate department for more specific information.",
        "I'm still learning about that area. Can you ask me something about courses, majors, registration, deadlines, financial aid, or campus resources instead?"
    ]
}

def generate_academic_response(query):
    """Generate a response based on academic query keywords"""
    query = query.lower()
    
    # Debug statement
    print(f"Received query: {query}")
    
    # Check for specific course inquiries
    query_no_spaces = query.replace(" ", "").lower()

    if "cs35101" in query_no_spaces or "computer organization" in query.lower():
        return academic_responses["specific_courses"]["cs35101"]
    elif "cs23022" in query_no_spaces or "discrete structures" in query.lower():
        return academic_responses["specific_courses"]["cs23022"]
    elif "cs10051" in query_no_spaces or "computer science principles" in query.lower():
        return academic_responses["specific_courses"]["cs10051"]
    elif "bsci10001" in query_no_spaces or "human biology" in query.lower():
        return academic_responses["specific_courses"]["bsci10001"]
    elif "bsci10002" in query_no_spaces or "life on planet earth" in query.lower():
        return academic_responses["specific_courses"]["bsci10002"]
    
    # Check for keywords and categorize the query
    if any(word in query for word in ["course", "class", "semester", "curriculum", "prerequisite"]):
        responses = academic_responses["courses"]
    elif any(word in query for word in ["major", "minor", "degree", "program", "concentration"]):
        responses = academic_responses["majors"]
    elif any(word in query for word in ["register", "registration", "sign up", "enroll"]):
        responses = academic_responses["registration"]
    elif any(word in query for word in ["deadline", "due date", "when is", "schedule"]):
        responses = academic_responses["deadlines"]
    elif any(word in query for word in ["financial", "scholarship", "tuition", "fafsa", "aid", "grant", "loan"]):
        responses = academic_responses["financial_aid"]
    elif any(word in query for word in ["campus", "resource", "facility", "library", "dorm", "housing"]):
        responses = academic_responses["campus"]
    else:
        responses = academic_responses["default"]
    
    # Return a random response from the appropriate category
    selected_response = random.choice(responses)
    print(f"Generated response: {selected_response}")
    return selected_response

@app.route("/")
def index():
    print("Index route accessed")
    return render_template('flash.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    print(f"Chat endpoint accessed with method: {request.method}")
    print(f"Form data: {request.form}")
    
    try:
        if request.method == "POST":
            msg = request.form.get("msg", "")
            print(f"Message received: {msg}")
            
            # Generate a meaningful response
            response = generate_academic_response(msg)
            print(f"Response generated: {response}")
            
            return response
        else:
            return "Please use POST method to send messages."
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return f"Sorry, I encountered an error processing your request. Please try again. Error: {str(e)}"

if __name__ == "__main__":
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=5500, debug=True)