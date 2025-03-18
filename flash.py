from flask import Flask, render_template, request, send_from_directory
import random
import re
import os

# Create Flask app
app = Flask(__name__, template_folder=".")

# Basic academic Q&A responses
academic_responses = {
    "greetings": [
        "Hello! How can I assist you with your academic questions today?",
        "Hi there! I'm here to help with any academic-related questions you might have.",
        "Good day! What academic information are you looking for today?"
    ],
    "thanks": [
        "You're welcome! Is there anything else I can help you with?",
        "Glad I could help! Do you have any other questions?",
        "It's my pleasure to assist you. What else would you like to know about academic life?"
    ],
    "courses": [
        "We offer a wide range of courses across multiple disciplines. Could you specify which department you're interested in?",
        "Our course catalog includes both undergraduate and graduate options. Are you looking for a specific level or subject area?",
    ],
    "specific_courses": {
        "cs35101": "CS 35101 - Computer Organization\n\nCredits: 3\n\nDescription: Computer system organization, including performance measures, instruction sets, computer arithmetic, central processing unit, pipelining, memory hierarchy and parallel processors.\n\nPrerequisites: Minimum C grade in the following courses: CS 10062 or CS 13001; or CS 13011 and CS 13012.\n\nOffered: Fall, Spring, Summer",
        "cs23022": "CS 23022 - Discrete Structures for Computer Science\n\nCredits: 3\n\nDescription: Discrete structures for computer scientists with a focus on: mathematical reasoning, combinatorial analysis, discrete structures, algorithmic thinking, applications and modeling.\n\nPrerequisites: Minimum C grade in MATH 11009 or MATH 11010 or MATH 11022, or ALEKS score of 78.\n\nOffered: Fall, Spring, Summer",
        "cs10051": "CS 10051 - Computer Science Principles\n\nCredits: 3\n\nDescription: An introductory, broad and hands-on coverage of aspects of computer science, including algorithms, problem solving, operating systems concepts, computer architecture, programming languages and modern applications. Three-credit lecture with one-credit lab.\n\nPrerequisites: None\n\nOffered: Fall, Spring",
        "bsci10001": "BSCI 10001 - Human Biology\n\nCredits: 3\n\nDescription: Study of the scientific method and life's properties, emphasizing human biology. Topics include energy, genetics, reproduction, development disease, nutrition and physical fitness in humans. This course may not be used to fulfill major or minor requirements in the following programs: B.A. Biology, B.S. Biology, B.S. Biotechnology, B.S. Botany, B.S. Environmental and Conservation Biology, B.S. Medical Laboratory Science, B.S. Zoology and the Biological Sciences minor.\n\nPrerequisites: None\n\nOffered: Fall",
        "bsci10002": "BSCI 10002 - Life on Planet Earth\n\nCredits: 3\n\nDescription: Explores the fascinating breadth of life on Earth including the unique ecology and survival strategies of animals, plants and microbes in their natural habitats. This course may not be used to fulfill major or minor requirements in the following programs: B.A. Biology, B.S. Biology, B.S. Biotechnology, B.S. Botany, B.S. Environmental and Conservation Biology, B.S. Medical Laboratory Science, B.S. Zoology and the Biological Sciences minor.\n\nPrerequisites: None\n\nOffered: Fall, Spring"
    },
    "specific_majors": {
        "computerScience": "Computer Science\n\nDepartment: College of Sciences\n\nDegree: BA/BS\n\nDescription: The Bachelor of Science degree in Computer Science seeks to prepare students for careers as computing professionals, developing, managing and building software in a variety of industries, including finance, health care, entertainment, telecommunications and manufacturing.\n\nCareers: Software Developer, Data Scientist, Systems Analyst, Cybersecurity Specialist, Web Developer, Database Administrator, AI/Machine Learning Engineer\n\nRequirements: 120 credit hours including core CS courses, mathematics sequence, science electives, and technical specializations.",
        "businessAdministration": "Business Administration\n\nDepartment: College of Business\n\nDegree: BBA\n\nDescription: The Business Management B.B.A. program offers a comprehensive education in business fundamentals, management principles and leadership strategies to help you succeed in a wide range of industries.\n\nCareers: Business Analyst, Marketing Manager, Financial Advisor, Human Resources Manager, Operations Manager, Entrepreneur, Project Manager\n\nRequirements: 120 credit hours including business core, economics and accounting foundations, and specialized concentration courses",
        "psychology": "Psychology\n\nDepartment: College of Arts and Sciences\n\nDegree: BA/BS\n\nDescription: The Psychology program applies the science of understanding and explaining thoughts, emotions and behavior to solving real-world problems. Topics include stress, biological influences on behavior, growth and development of children and diagnosis and treatment of psychological disorders. Elective courses may be used to specialize in a number of areas of psychology and to gain hands-on experience in research labs. The degree prepares students for graduate school and employment in a range of fields, including clinical, applied and experimental areas of psychology and related fields such as education, law, human resources and health care.\n\nCareers: Mental Health Counselor, Research Assistant, Human Resources Specialist, Social Services Coordinator, Rehabilitation Specialist, Market Researcher\n\nRequirements: 120 credit hours including psychology core, research methods, statistics, and specialization electives."
    },
    "calendar": {
        "fall_registration": "Fall Registration\n\nDates: March 18-August 25th\n\nDetails: Specific registration dates are assigned by class standing.",
        "spring_registration": "Spring Registration\n\nDates: September 30th-January 19th\n\nDetails: Specific registration dates are assigned by class standing.",
        "summer_registration": "Summer Registration\n\nDates: February 19th-May 24th\n\nDetails: All students can register on the first day.",
        "semester_dates": "Semester Dates\n\nFall semester: August 19th – December 8th\n\nSpring Break: March 10-16th, with classes beginning on the following Monday\n\nFall Break: October 3-6, with no classes in session\n\nFinals Week: Occurs during the last two weeks of each semester, with schedule available one month prior"
    },
    "policies": {
        "academic_standing": "Academic Standing\n\nGood Standing: Cumulative GPA of 2.0 or higher\n\nMidterm Warning: Students who earn a midterm GPA of less than 2.000 will be placed on midterm warning.\n\nAcademic Probation: Students who fail to maintain a minimum 2.000 overall GPA will be placed on academic probation.\n\nAcademic Dismissal: Students whose academic performance indicates a limited chance of obtaining the minimum grades required for graduation will be subject to dismissal from the university.",
        "grading": "Grading Scale\n\nA (4.0), A- (3.7), B+ (3.3), B (3.0), B- (2.7), C+ (2.3), C (2.0), C- (1.7), D+ (1.3), D (1.0), F (0.0)",
        "honors": "Academic Honors\n\nDean's List: Semester GPA of 3.5 or higher while enrolled in at least 12 credit hours.\n\nPresident's List: Semester GPA of 4.0 or higher while enrolled in at least 12 credit hours.\n\nLatin Honors:\nCum Laude: Cumulative GPA of 3.5-3.699\nMagna Cum Laude: Cumulative GPA of 3.7-3.899\nSumma Cum Laude: Cumulative GPA of 3.9-4.0"
    },
    "enrollment": {
        "requirements": "Enrollment Requirements\n\nEligibility: Students must be in good academic standing and clear of any registration holds.\n\nAdvising: Meeting with an academic advisor is important before creating a schedule.\n\nCourse Load: Full time (12-18 credit hours per semester), Part Time (1-11 credit hours per semester), Overload (More than 18 hours requires Dean's permission)"
    },
    "financial": {
        "tuition": "Tuition Rates\n\nUndergraduate In-State: $335.57 per credit hour\n\nUndergraduate Out-of-State: $746.17 per credit hour\n\nGraduate In-State: $268.30 per credit hour\n\nGraduate Out-of-State: $678.90 per credit hour\n\nAdditional Information: Fees apply for labs, online courses, and certain majors.",
        "payment": "Payment Information\n\nPayment Deadline: Tuition is due three weeks after issued an e-bill\n\nPayment Methods: Credit card, electronic check, cash, or through approved payment plans",
        "aid": "Financial Aid\n\nFAFSA Deadline: March 1 for priority consideration for the following academic year\n\nTypes: Grants, loans, work-study, and scholarships\n\nRequirements: Maintain satisfactory academic progress (2.0 GPA and 67% completion rate)",
        "scholarships": "Scholarships\n\nMerit-based: Based on GPA, test scores, and academic achievements\n\nNeed-based: Determined by financial need as calculated by FAFSA\n\nDepartmental: Specific to certain majors or programs\n\nDeadlines: Typically February 1 for the following academic year"
    },
    "resources": {
        "academic_success": "Academic Success Center\n\nServices: Tutoring, study skills workshops, supplemental instruction\n\nHours: Monday-Thursday 8am-4pm, Friday 8am-5pm\n\nLocation: 40 Campus Center-Lower Level",
        "writing_center": "Writing Center\n\nServices: One-on-one consultations for writing assignments at any stage\n\nHours: Monday-Tuesday 9am-8pm, Wednesday-Thursday 9am-5pm, Friday 9am-2pm\n\nLocation: Stark Campus Library\n\nAppointments: Schedule online or walk-in during operating hours",
        "library": "Library\n\nServices: Research assistance, study spaces, technology checkout, interlibrary loan\n\nHours: Monday-Thursday 8am-8pm, Friday 8am-5pm\n\nResources: Online databases, journals, books, multimedia collections",
        "career_services": "Career Services\n\nServices: Resume reviews, mock interviews, job search assistance, career counseling\n\nHours: Monday-Friday 8:30am-5pm, extended hours by appointment\n\nLocation: Within the Library",
        "disability_services": "Disability Services\n\nServices: Academic accommodations, assistive technology, testing modifications\n\nRegistration: Submit CALs (course accommodation letters) in Access KSU at least two weeks before each semester."
    },
    "majors": [
        "We offer over 50 undergraduate majors and 30 graduate programs. Some popular choices include Computer Science, Business Administration, and Psychology.",
        "Our most competitive majors include Engineering, Nursing, and Computer Science. Each has specific admission requirements.",
        "When choosing a major, consider your interests, career goals, and academic strengths. Would you like to discuss a specific major?"
    ],
    "registration": [
        "Registration opens based on class standing, with seniors registering first. Have you checked your assigned registration date?",
        "To register for classes, log into the student portal and use the course search function to find available sections.",
        "Before registering, I recommend meeting with your academic advisor to ensure you're on track with your program requirements."
    ],
    "deadlines": [
        "Important upcoming deadlines include registration, drop/add periods, and withdrawal dates. Which specific deadline are you asking about?",
        "The final withdrawal deadline is typically around the 10th week of the semester. After this date, withdrawals require special approval.",
        "Tuition payment deadlines are usually three weeks after you receive your e-bill. Late payments may incur additional fees."
    ],
    "campus": [
        "Our campus offers numerous resources including the library, tutoring services, writing center, career services, and counseling center.",
        "Student housing options include traditional residence halls, apartment-style living, and off-campus apartments within walking distance.",
        "Campus facilities are generally open from 7am to 11pm on weekdays, with modified hours on weekends. The library offers extended hours during finals week."
    ],
    "financial_aid": [
        "Financial aid options include grants, scholarships, work-study, and loans. Have you submitted your FAFSA yet?",
        "Scholarship applications are evaluated based on academic achievement, financial need, and sometimes specific criteria set by donors.",
        "Our financial aid office offers one-on-one counseling to help students maximize their aid packages and minimize debt."
    ],
    "default": [
        "I'm here to help with academic questions. Could you provide more details about what you're looking for?",
        "That's an interesting question. Let me connect you with the appropriate department for more specific information.",
        "I'm still learning about that area. Can you ask me something about courses, majors, registration, deadlines, financial aid, or campus resources instead?"
    ]
}

def generate_academic_response(query):
    """Generate a response based on academic query keywords"""
    query = query.lower().strip()
    
    # Handle empty messages
    if not query:
        return "I didn't catch that. Could you please repeat your question?"
    
    # Check for greetings first
    if re.match(r'^(hi|hello|hey|greetings|howdy|hola)', query):
        return random.choice(academic_responses["greetings"])
    
    # Check for thank you messages
    if re.search(r'(thank|thanks|thx|ty)', query):
        return random.choice(academic_responses["thanks"])
    
    # Check for specific course inquiries
    query_no_spaces = query.replace(" ", "").lower()

    # Add direct handling for single word "majors" query
    if query == "majors":
        return random.choice(academic_responses["majors"])
    
    # Specific courses
    if "cs35101" in query_no_spaces or "computer organization" in query:
        return academic_responses["specific_courses"]["cs35101"]
    elif "cs23022" in query_no_spaces or "discrete structures" in query:
        return academic_responses["specific_courses"]["cs23022"]
    elif "cs10051" in query_no_spaces or "computer science principles" in query:
        return academic_responses["specific_courses"]["cs10051"]
    elif "bsci10001" in query_no_spaces or "human biology" in query:
        return academic_responses["specific_courses"]["bsci10001"]
    elif "bsci10002" in query_no_spaces or "life on planet earth" in query:
        return academic_responses["specific_courses"]["bsci10002"]
    
    # Specific majors
    elif query == "computer science" or "computer science major" in query or ("computer science" in query and "degree" in query):
     return academic_responses["specific_majors"]["computerScience"]
    elif query == "business administration" or query == "business" or "business administration" in query or ("business" in query and "major" in query):
     return academic_responses["specific_majors"]["businessAdministration"]
    elif query == "psychology" or "psychology major" in query or ("psychology" in query and "degree" in query):
     return academic_responses["specific_majors"]["psychology"]
    
    # Calendar information
    elif "fall registration" in query:
        return academic_responses["calendar"]["fall_registration"]
    elif "spring registration" in query:
        return academic_responses["calendar"]["spring_registration"]
    elif "summer registration" in query:
        return academic_responses["calendar"]["summer_registration"]
    elif "semester dates" in query or "academic calendar" in query or "fall break" in query or "spring break" in query:
        return academic_responses["calendar"]["semester_dates"]
    elif "calendar" in query:
        return ("Academic Calendar Information:\n\n"
                "- Fall Registration\n"
                "- Spring Registration\n"
                "- Summer Registration\n"
                "- Semester Dates\n\n"
                "Which calendar information would you like more details about?")
    
    # Academic policies
    elif "academic standing" in query or "good standing" in query or "probation" in query or "dismissal" in query:
        return academic_responses["policies"]["academic_standing"]
    elif "grading" in query or "grade scale" in query or "gpa scale" in query:
        return academic_responses["policies"]["grading"]
    elif "honors" in query or "dean's list" in query or "president's list" in query or "latin honors" in query or "cum laude" in query:
        return academic_responses["policies"]["honors"]
    elif "policies" in query or "academic policies" in query:
        return ("Academic Policies Information:\n\n"
                "- Academic Standing\n"
                "- Grading Scale\n"
                "- Academic Honors\n\n"
                "Which policy would you like more information about?")
    
    # Enrollment information
    elif "enrollment requirements" in query or "enrollment" in query or "course load" in query or "credit hours" in query or "full time" in query or "part time" in query:
        return academic_responses["enrollment"]["requirements"]
    
    # Financial information
    elif "tuition" in query or "cost per credit" in query:
        return academic_responses["financial"]["tuition"]
    elif "payment" in query or "pay tuition" in query or "e-bill" in query:
        return academic_responses["financial"]["payment"]
    elif "financial aid" in query or "fafsa" in query or "aid" in query:
        return academic_responses["financial"]["aid"]
    elif "scholarship" in query or "merit" in query:
        return academic_responses["financial"]["scholarships"]
    elif "financial" in query:
        return ("Financial Information:\n\n"
                "- Tuition Rates\n"
                "- Payment Information\n"
                "- Financial Aid\n"
                "- Scholarships\n\n"
                "Which financial information would you like more details about?")
    
    # Resources
    elif "academic success" in query or "tutoring" in query:
        return academic_responses["resources"]["academic_success"]
    elif "writing" in query or "writing center" in query:
        return academic_responses["resources"]["writing_center"]
    elif "library" in query:
        return academic_responses["resources"]["library"]
    elif "career" in query or "career services" in query or "resume" in query or "job" in query:
        return academic_responses["resources"]["career_services"]
    elif "disability" in query or "disability services" in query or "accommodations" in query:
        return academic_responses["resources"]["disability_services"]
    elif query == "resources" or "campus resources" in query:
        return ("Campus Resources and Services:\n\n"
                "- Academic Success Center\n"
                "- Writing Center\n"
                "- Library\n"
                "- Career Services\n"
                "- Disability Services\n\n"
                "Which resource would you like more information about?")
    
    # Default responses for general categories
    elif any(word in query for word in ["course", "class", "semester", "curriculum", "prerequisite"]):
        return random.choice(academic_responses["courses"])
    elif any(word in query for word in ["major", "minor", "degree", "program", "concentration"]):
        return random.choice(academic_responses["majors"])
    elif any(word in query for word in ["register", "registration", "sign up", "enroll"]):
        return random.choice(academic_responses["registration"])
    elif any(word in query for word in ["deadline", "due date", "when is", "schedule"]):
        return random.choice(academic_responses["deadlines"])
    elif any(word in query for word in ["financial", "scholarship", "tuition", "fafsa", "aid", "grant", "loan"]):
        return random.choice(academic_responses["financial_aid"])
    elif any(word in query for word in ["campus", "resource", "facility", "library", "dorm", "housing"]):
        return random.choice(academic_responses["campus"])
    else:
        return random.choice(academic_responses["default"])

# Route to serve index.html
@app.route("/")
def index():
    print("Index route accessed")
    return render_template('index.html')

# Route to serve the flash.html file
@app.route("/flash.html")
def flash_html():
    return render_template('flash.html')

# Route to serve the help.html file
@app.route("/help.html")
def help_html():
    return render_template('help.html')

# Keep these for backward compatibility with older code
@app.route("/flash")
def flash_page():
    return render_template('flash.html')

@app.route("/help")
def help_page():
    return render_template('help.html')

# API endpoint for chat functionality
@app.route("/get", methods=["GET", "POST"])
def chat():
    print(f"Chat endpoint accessed with method: {request.method}")
    
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
        return f"Sorry, I encountered an error processing your request. Please try again."

# Add static file serving for GitHub Pages compatibility
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == "__main__":
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=5500, debug=True)