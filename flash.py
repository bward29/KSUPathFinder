from flask import Flask, render_template, request, jsonify
import os
import re
from datetime import datetime
import random



# Create Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('flash.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        # Generate comprehensive response
        response = generate_academic_advisor_response(msg)
        return response
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

# Comprehensive academic database
academic_database = {
    # Courses with detailed information
    "courses": [
        {
            "code": "CS 35101",
            "name": "Computer Organiation",
            "credits": 3,
            "description": "Computer system organization, including performance measures, instruction sets, computer arithmetic, central processing unit, pipelining, memory hierarchy and parallel processors.",
            "prerequisites": "Minimum C grade in the following courses: CS 10062 or CS 13001; or CS 13011 and CS 13012.",
            "offered": "Fall, Spring, Summer",
        },
        {
            "code": "CS 23022",
            "name": "Discrete Structures for Computer Science",
            "credits": 3,
            "description": "Discrete structures for computer scientists with a focus on: mathematical reasoning, combinatorial analysis, discrete structures, algorithmic thinking, applications and modeling.",
            "prerequisites": "Minimum C grade in MATH 11009 or MATH 11010 or MATH 11022, or ALEKS score of 78.",
            "offered": "Fall, Spring, Summer",
        },
        {
            "code": "CS 10051",
            "name": "Computer Science Principles",
            "credits": 3,
            "description": "An introductory, broad and hands-on coverage of aspects of computer science, including algorithms, problem solving, operating systems concepts, computer architecture, programming languages and modern applications. Three-credit lecture with one-credit lab.",
            "prerequisites": "None",
            "offered": "Fall, Spring",
        },
        {
            "code": "BSCI 10001",
            "name": "Human Biology",
            "credits": 3,
            "description": "Study of the scientific method and life's properties, emphasizing human biology. Topics include energy, genetics, reproduction, development disease, nutrition and physical fitness in humans. This course may not be used to fulfill major or minor requirements in the following programs: B.A. Biology, B.S. Biology, B.S. Biotechnology, B.S. Botany, B.S. Environmental and Conservation Biology, B.S. Medical Laboratory Science, B.S. Zoology and the Biological Sciences minor.",
            "prerequisites": "None",
            "offered": "Fall",
        },
        {
            "code": "BSCI 10002",
            "name": "Life on Planet Earth",
            "credits": 3,
            "description": "Explores the fascinating breadth of life on Earth including the unique ecology and survival strategies of animals, plants and microbes in their natural habitats. This course may not be used to fulfill major or minor requirements in the following programs: B.A. Biology, B.S. Biology, B.S. Biotechnology, B.S. Botany, B.S. Environmental and Conservation Biology, B.S. Medical Laboratory Science, B.S. Zoology and the Biological Sciences minor.",
            "prerequisites": "None",
            "offered": "Fall, Spring",
        },
        {
            "code": "BSCI 11010",
            "name": "Foundational Anatomy and Physiology I",
            "credits": 3,
            "description": "Anatomy and physiology to include organization of the human body, cells, tissues, organs and systems; integumentary, skeletal, muscular and respiratory systems; and overviews of the nervous and circulatory system. This course is taught on Kent State's regional campuses for associate degree programs. This course may not be used to fulfill major or minor requirements in the following programs: B.A. Biology, B.S. Biology, B.S. Biotechnology, B.S. Botany, B.S. Environmental and Conservation Biology, B.S. Medical Laboratory Science, B.S. Zoology and the Biological Sciences minor.",
            "prerequisites": "Special approval.",
            "offered": "Fall, Spring, Summer",
        },
        {
            "code": "SPAN 28202",
            "name": "Intermediate Spanish II",
            "credits": 3,
            "description": "A continuation of the development of listening, speaking, reading and writing skills using a variety of material on the Spanish language in the context of Hispanic cultures and specific areas of study like culture, business, justice, etc.",
            "prerequisites": "SPAN 28201",
            "offered": "Fall, Spring",
        },
        {
            "code": "SPAN 38421",
            "name": "Civilization of Spain",
            "credits": 3,
            "description": "General survey of evolution of Spanish civilization from antiquity to present day.",
            "prerequisites": "SPAN 38211",
            "offered": "Fall, Spring, Summer",
        },
        {
            "code": "SPAN 38424",
            "name": "Culture and Civilization of Latin America",
            "credits": 3,
            "description": "This course focuses on a study of the historical and cultural development of Latin America, with emphasis on Spanish America, as reflected in its geography, history, art, political and social institutions encompassing from Pre-Hispanic times to the present.",
            "prerequisites": "SPAN 38211 or SPAN 38213",
            "offered": "Fall, Spring",
        },
        {
            "code": "COMM 20001",
            "name": "Interpersonal Communication",
            "credits": 3,
            "description": "Introduction to human interpersonal communication. Components and structures situations and contexts are described nonevaluative focus with emphasis on informal experience.",
            "prerequisites": "None",
            "offered": "Spring",
        }
    ],

    # Major programs with detailed information
    "majors": [
        {
            "name": "Computer Science",
            "department": "College of Sciences",
            "degree": "BA/BS",
            "description": "The Bachelor of Science degree in Computer Science seeks to prepare students for careers as computing professionals, developing, managing and building software in a variety of industries, including finance, health care, entertainment, telecommunications and manufacturing.",
            "careers": "Software Developer, Data Scientist, Systems Analyst, Cybersecurity Specialist, Web Developer, Database Administrator, AI/Machine Learning Engineer",
            "requirements": "120 credit hours including core CS courses, mathematics sequence, science electives, and technical specializations",
        },
        {
            "name": "Business Administration",
            "department": "College of Business",
            "degree": "BBA",
            "description": "The Business Management B.B.A. program offers a comprehensive education in business fundamentals, management principles and leadership strategies to help you succeed in a wide range of industries.",
            "careers": "Business Analyst, Marketing Manager, Financial Advisor, Human Resources Manager, Operations Manager, Entrepreneur, Project Manager",
            "requirements": "120 credit hours including business core, economics and accounting foundations, and specialized concentration courses",
        },
        {
            "name": "Psychology",
            "department": "College of Arts and Sciences",
            "degree": "BA/BS",
            "description": "The Psychology program applies the science of understanding and explaining thoughts, emotions and behavior to solving real-world problems. Topics include stress, biological influences on behavior, growth and development of children and diagnosis and treatment of psychological disorders. Elective courses may be used to specialize in a number of areas of psychology and to gain hands-on experience in research labs. The degree prepares students for graduate school and employment in a range of fields, including clinical, applied and experimental areas of psychology and related fields such as education, law, human resources and health care.",
            "careers": "Mental Health Counselor, Research Assistant, Human Resources Specialist, Social Services Coordinator, Rehabilitation Specialist, Market Researcher",
            "requirements": "120 credit hours including psychology core, research methods, statistics, and specialization electives",
        },
        {
            "name": "English",
            "department": "College of Arts and Sciences",
            "degree": "BA",
            "description": "The English program prepares students to be insightful readers and innovative writers. Students are introduced to literary traditions and critical methods through core courses and encouraged to pursue personal interests in the selection of a concentration and elective courses. English classes challenge students to develop reading, research and writing skills that will equip them for a wide range of careers.",
            "careers": "Editor, Technical Writer, Content Creator, Communications Specialist, Teacher, Publisher, Journalist, Public Relations Specialist",
            "requirements": "120 credit hours including literature surveys, composition courses, linguistics, and specialized period or genre studies",
        },
        {
            "name": "Biology",
            "department": "College of Sciences",
            "degree": "BA/BS",
            "description": "The Biology program provides you with a solid foundation in the fundamental principles of biology, as well as advanced knowledge in specialized areas of the discipline. With state-of-the-art facilities, cutting-edge technology and experienced faculty, you will gain the skills needed to succeed in the fast-paced world of biology.",
            "careers": "Research Scientist, Laboratory Technician, Healthcare Professional, Environmental Consultant, Biotechnologist, Pharmaceutical Representative",
            "requirements": "120 credit hours including biology core, chemistry sequences, physics, mathematics, and specialized upper-division electives",
        }
    ],

    # Academic calendar with important dates
    "calendar": {
        "fall registration": "March 18-August 25th, with specific dates assigned by class standing",
        "spring registration": "September 30th-January 19th d, with specific dates assigned by class standing",
        "summer registration": "February 19th-May 24th, all students can register on the first day",
        "fall semester start": "August 19th",
        "fall semester end": "December 8th",
        "spring break": "March 10-16th, with classes beginning on the following Monday",
        "fall break": "October 3-6, with no classes in session",
        "finals week": "Occurs during the last two weeks of each semester, with schedule available one month prior"
    },

    # Academic policies and procedures
    "policies": {
        "academic_standing": {
            "good_standing": "Cumulative GPA of 2.0 or higher",
            "midterm_warning": "Students who earn a midterm GPA of less than 2.000 will be placed on midterm warning.",
            "academic_probation": "Students who fail to maintain a minimum 2.000 overall GPA will be placed on academic probation.",
            "academic_dismissal": "Students whose academic performance indicates a limited chance of obtaining the minimum grades required for graduation will be subject to dismissal from the university.",
        },
        "grading": {
            "scale": "A (4.0), A- (3.7), B+ (3.3), B (3.0), B- (2.7), C+ (2.3), C (2.0), C- (1.7), D+ (1.3), D (1.0), F (0.0)",
        },
        "deans_list": "Semester GPA of 3.5 or higher while enrolled in at least 12 credit hours",
        "latin_honors": {
            "cum_laude": "Cumulative GPA of 3.5-3.699",
            "magna_cum_laude": "Cumulative GPA of 3.7-3.899",
            "summa_cum_laude": "Cumulative GPA of 3.9-4.0"
        },
        "academic_integrity": "Violations include plagiarism, cheating, unauthorized collaboration, and fabrication, with penalties ranging from course failure to expulsion"
    },

    # Registration and enrollment procedures
    "registration": {
        "eligibility": "Students must be in good academic standing and clear of any registration holds.",
        "advising": "Meeting with an academic advisor is important before creating a schedule.",
        "course_load": {
            "full_time": "12-18 credit hours per semester",
            "part_time": "1-11 credit hours per semester",
            "overload": "More than 18 credit hours requires dean's permission"
        },
    },

    # Financial information
    "financial": {
        "tuition": {
            "in_state": "$335.57 per credit hour",
            "out_of_state": "$746.17 per credit hour",
            "graduate_in_state": "$268.30 per credit hour",
            "graduate_out_of_state": "$678.90 per credit hour",

            "fees": "Additional fees apply for labs, online courses, and certain majors"
        },
        "payment_deadlines": "Tuition is due three weeks after issued an e-bill",
        "payment_methods": "Credit card, electronic check, cash, or through approved payment plans",
        "financial_aid": {
            "fafsa_deadline": "March 1 for priority consideration for the following academic year",
            "types": "Grants, loans, work-study, and scholarships",
            "requirements": "Maintain satisfactory academic progress (2.0 GPA and 67% completion rate)"
        },
        "scholarships": {
            "merit_based": "Based on GPA, test scores, and academic achievements",
            "need_based": "Determined by financial need as calculated by FAFSA",
            "departmental": "Specific to certain majors or programs",
            "deadlines": "Typically February 1 for the following academic year"
        },
    },

    # Campus resources and services
    "resources": {
        "academic_success_center": {
            "services": "Tutoring, study skills workshops, supplemental instruction",
            "hours": "Monday-Thursday 8am-4pm, Friday 8am-5pm",
            "location": "40 Campus Center-Lower Level"
        },
        "writing_center": {
            "services": "One-on-one consultations for writing assignments at any stage",
            "appointments": "Schedule online or walk-in during operating hours",
            "hours": "Monday-Tuesday 9am-8pm, Wednesday-Thursday 9am-5pm, Friday 9am-2pm",
            "location": "Stark Campus Library"
        },
        "library": {
            "services": "Research assistance, study spaces, technology checkout, interlibrary loan",
            "hours": "Monday-Thursday 8am-8pm, Friday 8am-5pm",
            "resources": "Online databases, journals, books, multimedia collections",
        },

        },
        "career_services": {
            "services": "Resume reviews, mock interviews, job search assistance, career counseling",
            "hours": "Monday-Friday 8:30am-5pm, extended hours by appointment",
            "location": "Student Union, Third Floor"
        },
        "disability_services": {
            "services": "Academic accommodations, assistive technology, testing modifications",
            "registration": "Submit documentation at least two weeks before accommodations are needed",
            "location": "Library"
        }
    }

def generate_academic_advisor_response(text):
    """Generate a comprehensive academic advisor response with improved readability and accuracy."""
    text = text.lower().strip()
    
    # Get current date information
    current_date = datetime.now()
    formatted_date = current_date.strftime("%A, %B %d, %Y")
    
    # Function to find most relevant course
    def find_course(input_text):
        # First try exact course code match
        code_match = next((course for course in academic_database["courses"] if 
                          course["code"].lower() in input_text), None)
        
        if code_match:
            return code_match
        
        # Then try course name match
        name_match = next((course for course in academic_database["courses"] if 
                          course["name"].lower() in input_text), None)
        
        if name_match:
            return name_match
        
        # Finally, try partial matches on key terms
        subject_matches = [course for course in academic_database["courses"] if 
                          any(word in input_text for word in course["name"].lower().split() if len(word) > 3)]
        
        if subject_matches:
            return subject_matches[0]
        
        return None
    
    # Function to find most relevant major
    def find_major(input_text):
        # First try exact major name match
        name_match = next((major for major in academic_database["majors"] if 
                          major["name"].lower() in input_text), None)
        
        if name_match:
            return name_match
        
        # Then try department match
        dept_match = next((major for major in academic_database["majors"] if 
                          major["department"].lower() in input_text), None)
        
        if dept_match:
            return dept_match
        
        # Finally, try matches on career keywords
        career_matches = [major for major in academic_database["majors"] if 
                         any(career_term in major["careers"].lower() for career_term in input_text.split() if len(career_term) > 4)]
        
        if career_matches:
            return career_matches[0]
        
        return None

    # Check for greetings
    if re.search(r'\b(hello|hi|hey|greetings|howdy)\b', text):
        return "Hello! I'm your AI Academic Advisor. I can help with questions about courses, majors, registration, deadlines, financial aid, and campus resources. What specific academic information are you looking for today?"

    # Check for gratitude
    if re.search(r'\b(thanks|thank you|appreciate|grateful)\b', text):
        return "You're welcome! I'm happy to help with any academic questions you have. Feel free to ask about courses, majors, deadlines, or anything else related to your academic journey."

    # Check for farewells
    if re.search(r'\b(bye|goodbye|see you|farewell)\b', text):
        return "Goodbye! Feel free to return anytime you have questions about your academic journey. Wishing you success in your studies!"

    # Check for identity questions
    if re.search(r'\b(who are you|what are you|about you)\b', text):
        return "I'm an AI Academic Advisor designed to help students navigate their educational journey. I provide detailed information about courses, majors, registration procedures, deadlines, financial aid options, and campus resources to help make your academic experience more successful. How can I assist you specifically today?"

    # Course-related questions
    if re.search(r'\b(course|class|subject|credits?|prerequisites?)\b', text):
        course = find_course(text)
        
        # Found specific course
        if course:
            return f"{course['code']}: {course['name']} ({course['credits']} credits)\n\n{course['description']}\n\nPrerequisites: {course['prerequisites']}\nTypically offered: {course['offered']}\nRequirements: {course['requirements']}\nRecommended next course: {course['next_course']}\n\nWould you like information about related courses or how this fits into a specific major?"
        
        # Check for prerequisite questions
        if re.search(r'\b(prerequisite|prereq|before taking|required for)\b', text):
            return "Prerequisites ensure you have the necessary background knowledge for success in more advanced courses. They're listed in the course catalog and registration system for each course. Most introductory (100-level) courses don't have prerequisites, while upper-division courses typically require foundational coursework. Is there a specific course you'd like to know the prerequisites for?"
        
        # Check for credit questions
        if re.search(r'\b(credit hour|credits|how many credits)\b', text):
            return "Most lecture courses are worth 3 credit hours and typically meet for 3 hours per week. Laboratory courses and courses with significant hands-on components may be worth 4-5 credits. Full-time students take 12-18 credits per semester, and most degree programs require 120-124 total credit hours for graduation. One credit hour generally represents one hour of classroom instruction plus 2-3 hours of outside work per week."
        
        # General course information
        return "Our university offers a wide range of courses across multiple disciplines. Courses are numbered to indicate level: 1000-2000 level (freshman/sophomore), 3000-4000 level (junior/senior), and 5000+ (graduate). Each course has specific prerequisites, credit values, and learning outcomes. Most courses are 3 credits and meet 2-3 times per week. Could you specify which course or subject area you're interested in learning more about?"

    # Major-related questions
    if re.search(r'\b(major|degree|program|concentration|minor|field|study)\b', text):
        major = find_major(text)
        
        # Found specific major
        if major:
            core_courses = ", ".join(major["core_courses"])
            return f"{major['name']} ({major['degree']}) - {major['department']}\n\nProgram Description: {major['description']}\n\nCareer Opportunities: {major['careers']}\n\nDegree Requirements: {major['requirements']}\n\nCore Courses: {core_courses}\n\nAdvising Note: {major['advising']}\n\nWould you like information about related minors or specific course sequences for this program?"
        
        # Declaring major questions
        if re.search(r'\b(declare|declaring|choose|choosing|pick|picking|select|selecting)\b', text) and re.search(r'\b(major|program)\b', text):
            return "Most undergraduate students should declare a major by the end of their sophomore year (60 credit hours). The process involves meeting with an advisor from your intended department and completing a major declaration form. Many students change their major at least once during college, so exploration is encouraged early on. To declare a major, schedule an appointment with the department you're interested in to discuss requirements and the declaration process."
        
        # Minor questions
        if re.search(r'\b(minor|secondary|additional)\b', text):
            return "A minor is a secondary area of study that requires 15-21 credit hours of coursework. Minors complement your major by developing additional skills that enhance your career prospects. For example, a Computer Science major might minor in Business, or an English major might minor in Professional Writing. Minors appear on your transcript but not on your diploma. You can declare a minor after completing at least 30 credit hours by submitting a minor declaration form to the appropriate department."
        
        # General major information
        return "Our university offers numerous undergraduate major programs across various colleges and departments. Each major has specific course requirements, elective options, and career pathways. Most bachelor's degrees require 120-124 total credit hours, including general education requirements, major courses, and electives. Some programs have specific GPA requirements or application processes for admission. What specific major or academic field are you interested in exploring?"

    # Calendar and deadline questions
    if re.search(r'\b(when|deadline|due date|calendar|date|schedule|start|begin|end)\b', text):
        # Check for specific calendar terms
        for event, date in academic_database["calendar"].items():
            if event in text:
                return f"{event.title()} is scheduled for {date}. Today is {formatted_date}. This information is also available on the university website's academic calendar. I recommend adding important academic dates to your personal calendar at the beginning of each semester."
        
        # Registration specific response
        if re.search(r'\b(registration|register|sign up|enroll)\b', text):
            return f"Registration dates are determined by class standing: seniors register first, followed by juniors, sophomores, and freshmen. Today is {formatted_date}. Fall registration typically occurs in April, Spring registration in November, and Summer registration in March. Before registering, you'll need to meet with your academic advisor to discuss course selections and obtain your registration PIN. Registration is completed through the student portal, and I recommend preparing a list of backup courses in case your first choices are full."
        
        # Finals specific response
        if re.search(r'\b(final|exam|test)\b', text):
            return f"Finals week typically takes place during the last two weeks of each semester. Today is {formatted_date}. The exact schedule for each course will be announced by your professors or posted on the university website about a month before finals begin. The schedule is typically arranged to avoid having multiple exams on the same day. I recommend preparing early and checking for any potential exam conflicts as soon as the schedule is released."
        
        # Semester start/end dates
        if re.search(r'\b(semester|term|quarter)\b', text) and re.search(r'\b(start|begin|end|finish)\b', text):
            return f"The Fall semester typically starts around August 25th and ends around December 10th. The Spring semester starts around January 15th and ends around May 10th. Summer sessions vary in length, with options for 5-week, 8-week, and 10-week terms between May and August. Today is {formatted_date}. The exact dates for the current and upcoming semesters can be found on the university's academic calendar."
        
        # General calendar information
        return f"Today is {formatted_date}. The academic calendar includes important dates such as registration periods, semester start/end dates, breaks, withdrawal deadlines, and final exam schedules. It's available on the university website and is updated for each academic year. Planning around these dates is crucial for academic success. Is there a specific academic deadline or event you're inquiring about?"

    # Registration and enrollment questions
    if re.search(r'\b(register|registration|sign up|enroll|add class|drop class|withdraw|waitlist)\b', text):
        # Withdrawal specific response
        if re.search(r'\b(withdraw|withdrawal|drop after|late drop)\b', text):
            return "Course withdrawal after the drop/add period but before the withdrawal deadline results in a 'W' grade on your transcript. A 'W' grade doesn't affect your GPA but does count as an attempt for repeat course policies and financial aid calculations. The withdrawal deadline is typically around the beginning of the semester. After this deadline, withdrawals are only permitted for extenuating circumstances with dean's approval. Always consult with your advisor and financial aid office before withdrawing from courses."
        
        # General registration information
        return "The registration process begins with academic advising to plan your course schedule. Registration dates are assigned based on class standing, with priority given to students with more earned credits. The process is completed through FlashLine, where you can search for courses, check for prerequisite requirements, view available sections, and build your schedule. It's recommended to register as early as possible and have backup options prepared in case your preferred sections are full."
