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
            "description": "The Computer Science program prepares students for careers in software development, data analysis, and systems design through rigorous training in algorithms, programming languages, and computational problem-solving.",
            "careers": "Software Developer, Data Scientist, Systems Analyst, Cybersecurity Specialist, Web Developer, Database Administrator, AI/Machine Learning Engineer",
            "requirements": "120 credit hours including core CS courses, mathematics sequence, science electives, and technical specializations",
            "core_courses": ["CS 150: Introduction to Programming", "CS 250: Data Structures", "CS 260: Computer Organization", "CS 321: Operating Systems", "CS 330: Database Systems", "CS 450: Algorithms"],
            "advising": "Computer Science majors should meet with their advisor at least once per semester to ensure proper course sequencing."
        },
        {
            "name": "Business Administration",
            "department": "College of Business",
            "degree": "BBA",
            "description": "The Business Administration program provides comprehensive training in management, marketing, finance, and operations, preparing students for diverse business careers through practical applications and case studies.",
            "careers": "Business Analyst, Marketing Manager, Financial Advisor, Human Resources Manager, Operations Manager, Entrepreneur, Project Manager",
            "requirements": "120 credit hours including business core, economics and accounting foundations, and specialized concentration courses",
            "core_courses": ["BUS 101: Introduction to Business", "ACCT 201: Principles of Accounting I", "ECON 201: Principles of Microeconomics", "FIN 300: Business Finance", "MGMT 303: Principles of Management", "MKTG 301: Principles of Marketing"],
            "advising": "Business students should declare their concentration by the end of sophomore year to ensure timely graduation."
        },
        {
            "name": "Psychology",
            "department": "College of Arts and Sciences",
            "degree": "BA/BS",
            "description": "The Psychology program explores human behavior and mental processes through scientific research and application, offering both BA and BS tracks depending on career goals and research interests.",
            "careers": "Mental Health Counselor, Research Assistant, Human Resources Specialist, Social Services Coordinator, Rehabilitation Specialist, Market Researcher",
            "requirements": "120 credit hours including psychology core, research methods, statistics, and specialization electives",
            "core_courses": ["PSYC 101: Introduction to Psychology", "PSYC 210: Research Methods", "PSYC 305: Cognitive Psychology", "PSYC 315: Developmental Psychology", "PSYC 401: Abnormal Psychology", "PSYC 490: Senior Seminar"],
            "advising": "The BS track requires more science and mathematics courses, while the BA track allows more flexibility with foreign language requirements."
        },
        {
            "name": "English",
            "department": "College of Arts and Sciences",
            "degree": "BA",
            "description": "The English program develops critical thinking, analytical reading, and effective writing skills through the study of literature, language, and rhetoric from diverse cultural perspectives.",
            "careers": "Editor, Technical Writer, Content Creator, Communications Specialist, Teacher, Publisher, Journalist, Public Relations Specialist",
            "requirements": "120 credit hours including literature surveys, composition courses, linguistics, and specialized period or genre studies",
            "core_courses": ["ENG 101: Composition I", "ENG 220: Introduction to Literature", "ENG 301: Creative Writing", "ENG 310: Literary Criticism", "ENG 415: Shakespeare", "ENG 490: Senior Thesis"],
            "advising": "English majors can specialize in literature, creative writing, or professional writing tracks based on career goals."
        },
        {
            "name": "Biology",
            "department": "College of Sciences",
            "degree": "BS",
            "description": "The Biology program provides thorough grounding in biological sciences through classroom, laboratory, and field experiences, preparing students for careers in research, healthcare, and environmental sectors.",
            "careers": "Research Scientist, Laboratory Technician, Healthcare Professional, Environmental Consultant, Biotechnologist, Pharmaceutical Representative",
            "requirements": "124 credit hours including biology core, chemistry sequences, physics, mathematics, and specialized upper-division electives",
            "core_courses": ["BIOL 110: Principles of Biology", "BIOL 210: Cell Biology", "BIOL 301: Genetics", "BIOL 320: Ecology", "BIOL 410: Molecular Biology", "BIOL 490: Research Seminar"],
            "advising": "Biology majors should consider their post-graduation plans early, as medical, dental, and graduate school preparation may require additional coursework."
        }
    ],

    # Academic calendar with important dates
    "calendar": {
        "fall registration": "April 1-15, with specific dates assigned by class standing",
        "spring registration": "November 1-15, with specific dates assigned by class standing",
        "summer registration": "March 15-30, all students can register on the first day",
        "fall semester start": "August 25, with classes beginning on the following Monday",
        "fall semester end": "December 15, with final exams ending the week before",
        "spring semester start": "January 15, with classes beginning on the following Monday",
        "spring semester end": "May 10, with commencement ceremonies the following weekend",
        "fall break": "October 10-14, with no classes in session",
        "spring break": "March 12-16, with no classes in session",
        "withdrawal deadline": "10 weeks into the semester (check the academic calendar for the exact date for the current term)",
        "graduation application": "Must be submitted at least three months before the end of your final semester",
        "finals week": "Occurs during the last two weeks of each semester, with schedule available one month prior"
    },

    # Academic policies and procedures
    "policies": {
        "academic_standing": {
            "good_standing": "Cumulative GPA of 2.0 or higher",
            "academic_warning": "First semester with GPA below 2.0",
            "academic_probation": "Second consecutive semester with GPA below 2.0",
            "academic_suspension": "Third consecutive semester with GPA below 2.0",
            "readmission": "Students on academic suspension must sit out one semester before applying for readmission"
        },
        "grading": {
            "scale": "A (4.0), A- (3.7), B+ (3.3), B (3.0), B- (2.7), C+ (2.3), C (2.0), C- (1.7), D+ (1.3), D (1.0), F (0.0)",
            "pass_fail": "Option available for electives outside major; P grades not calculated in GPA",
            "incomplete": "Given only for extenuating circumstances; must be completed within one semester",
            "grade_appeals": "Must be initiated within two weeks of grade posting"
        },
        "deans_list": "Semester GPA of 3.5 or higher while enrolled in at least 12 credit hours",
        "latin_honors": {
            "cum_laude": "Cumulative GPA of 3.5-3.69",
            "magna_cum_laude": "Cumulative GPA of 3.7-3.89",
            "summa_cum_laude": "Cumulative GPA of 3.9-4.0"
        },
        "academic_integrity": "Violations include plagiarism, cheating, unauthorized collaboration, and fabrication, with penalties ranging from course failure to expulsion"
    },

    # Registration and enrollment procedures
    "registration": {
        "eligibility": "Students must be in good academic standing and clear of any registration holds",
        "advising": "Meeting with an academic advisor is required to receive a registration PIN before each registration period",
        "course_load": {
            "full_time": "12-18 credit hours per semester",
            "part_time": "1-11 credit hours per semester",
            "overload": "More than 18 credit hours requires dean's permission"
        },
        "add_drop": "Courses can be added or dropped without penalty during the first week of classes",
        "withdrawal": "Students can withdraw from courses until the withdrawal deadline, resulting in a W grade that doesn't affect GPA",
        "waitlist": "Automatically processed as spaces become available; students have 24 hours to register once notified",
        "holds": "Common holds include advising holds, financial holds, health record holds, and academic standing holds"
    },

    # Financial information
    "financial": {
        "tuition": {
            "in_state": "$350 per credit hour",
            "out_of_state": "$950 per credit hour",
            "graduate": "$650 per credit hour",
            "fees": "Additional fees apply for labs, online courses, and certain majors"
        },
        "payment_deadlines": "Tuition is due two weeks before the start of each semester",
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
        "refunds": "Prorated based on withdrawal date; 100% refund during first week, no refunds after fourth week"
    },

    # Campus resources and services
    "resources": {
        "academic_success_center": {
            "services": "Tutoring, study skills workshops, supplemental instruction",
            "hours": "Monday-Thursday 9am-8pm, Friday 9am-5pm, Sunday 2pm-8pm",
            "location": "Library, Second Floor"
        },
        "writing_center": {
            "services": "One-on-one consultations for writing assignments at any stage",
            "appointments": "Schedule online or walk-in during operating hours",
            "hours": "Monday-Thursday 10am-7pm, Friday 10am-4pm",
            "location": "Humanities Building, Room 210"
        },
        "library": {
            "services": "Research assistance, study spaces, technology checkout, interlibrary loan",
            "hours": "Monday-Thursday 7am-12am, Friday 7am-8pm, Saturday 10am-8pm, Sunday 12pm-12am",
            "resources": "Online databases, journals, books, multimedia collections",
            "extended_hours": "24/7 during finals week"
        },
        "counseling_center": {
            "services": "Individual therapy, group sessions, crisis intervention, wellness workshops",
            "appointments": "Initial consultations available within 48 hours",
            "hours": "Monday-Friday 8am-5pm, crisis services available 24/7",
            "location": "Student Health Building, First Floor"
        },
        "career_services": {
            "services": "Resume reviews, mock interviews, job search assistance, career counseling",
            "events": "Career fairs held each semester, employer information sessions",
            "hours": "Monday-Friday 8:30am-5pm, extended hours by appointment",
            "location": "Student Union, Third Floor"
        },
        "disability_services": {
            "services": "Academic accommodations, assistive technology, testing modifications",
            "registration": "Submit documentation at least two weeks before accommodations are needed",
            "hours": "Monday-Friday 8am-5pm",
            "location": "Student Services Building, Room 120"
        }
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
        
        # Double major questions
        if re.search(r'\b(double major|dual degree|two majors)\b', text):
            return "Pursuing a double major means completing all requirements for two different major programs simultaneously. This typically requires careful planning and may extend your time to graduation. Double majors are beneficial for interdisciplinary career paths but require strong time management skills. You'll need advisors from both departments and must fulfill all core requirements for both programs. Some combinations have overlapping requirements, making them more manageable to complete within four years."
        
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
            return f"The Fall semester typically starts around August 25th and ends around December 15th. The Spring semester starts around January 15th and ends around May 10th. Summer sessions vary in length, with options for 5-week, 8-week, and 10-week terms between May and August. Today is {formatted_date}. The exact dates for the current and upcoming semesters can be found on the university's academic calendar."
        
        # General calendar information
        return f"Today is {formatted_date}. The academic calendar includes important dates such as registration periods, semester start/end dates, breaks, withdrawal deadlines, and final exam schedules. It's available on the university website and is updated for each academic year. Planning around these dates is crucial for academic success. Is there a specific academic deadline or event you're inquiring about?"

    # Registration and enrollment questions
    if re.search(r'\b(register|registration|sign up|enroll|add class|drop class|withdraw|waitlist)\b', text):
        # Withdrawal specific response
        if re.search(r'\b(withdraw|withdrawal|drop after|late drop)\b', text):
            return "Course withdrawal after the drop/add period but before the withdrawal deadline results in a 'W' grade on your transcript. A 'W' grade doesn't affect your GPA but does count as an attempt for repeat course policies and financial aid calculations. The withdrawal deadline is typically around the 10th week of the semester. After this deadline, withdrawals are only permitted for extenuating circumstances with dean's approval. Always consult with your advisor and financial aid office before withdrawing from courses."
        
        # Waitlist specific response
        if re.search(r'\b(waitlist|full class|closed section|get into full)\b', text):
            return "When a course reaches its enrollment capacity, you can join the waitlist through the registration system. Waitlisted students are automatically enrolled in order as spaces become available. Once notified of an opening, you have 24 hours to confirm your enrollment before the spot is offered to the next student. Regularly check your position on the waitlist and your university email for notifications. It's advisable to have backup courses ready in case you don't get into waitlisted sections."
        
        # Drop/add specific response
        if re.search(r'\b(drop|add|change schedule|swap)\b', text):
            return "The drop/add period allows you to adjust your schedule without penalty during the first week of classes (typically the first five business days of the semester). During this time, you can add available courses, drop courses without a record on your transcript, and switch between different sections. After this period, dropping courses results in a 'W' grade and adding courses requires instructor permission. All schedule changes are made through the online registration system or at the registrar's office."
        
        # Hold/PIN specific response
        if re.search(r'\b(hold|pin|cannot register|blocked|prevented)\b', text):
            return "Registration holds prevent you from registering for courses until specific requirements are addressed. Common holds include advising holds (requiring a meeting with your academic advisor to receive a registration PIN), financial holds (unpaid tuition or fees), health record holds (missing immunization records), and academic standing holds. You can view your holds in the student portal. Address each hold with the appropriate department before registration to ensure you can register on your assigned date."
        
        # General registration information
        return "The registration process begins with academic advising to plan your course schedule and receive your registration PIN. Registration dates are assigned based on class standing, with priority given to students with more earned credits. The process is completed through the student portal, where you can search for courses, check for prerequisite requirements, view available sections, and build your schedule. It's recommended to register as early as possible and have backup options prepared in case your preferred sections are full."

    # Financial questions
    if re.search(r'\b(tuition|cost|financial aid|fafsa|scholarship|payment|pay|loan|grant|work study|money|afford)\b', text):
        # FAFSA specific response
        if re.search(r'\b(fafsa|financial aid application|federal aid)\b', text):
            return "The Free Application for Federal Student Aid (FAFSA) should be submitted annually by March 1st for priority consideration. The application becomes available on October 1st for the following academic year. Filing early increases your chances of receiving need-based grants and work-study positions. Be sure to include our university's school code on your application. The financial aid office offers workshops to help with FAFSA completion throughout the academic year."
        
        # Scholarship specific response
        if re.search(r'\b(scholarship|academic award|merit|grant money)\b', text):
            return "Scholarships are available through the university, academic departments, and external organizations. University scholarships include merit-based awards (based on GPA and test scores) and need-based awards (determined by financial need). Departmental scholarships are specific to certain majors or programs. Most scholarship applications require essays, recommendation letters, and academic transcripts. The general scholarship application deadline is February 1st for the following academic year, but some have different deadlines."
        
        # Payment plan specific response
        if re.search(r'\b(payment plan|installment|pay over time|monthly payment)\b', text):
            return "Payment plans allow you to divide your tuition and fees into installments throughout the semester rather than paying one lump sum. Typically, plans require an initial down payment (25% of the total) and divide the remainder into 3-4 monthly payments. There's a small enrollment fee for using the payment plan (usually $35-50). To enroll, visit the student accounts section of the portal or contact the bursar's office. Enrollment in payment plans typically closes two weeks after the semester begins."
        
        # Work-study specific response
        if re.search(r'\b(work study|work-study|campus job|student employment)\b', text):
            return "Federal Work-Study is a financial aid program that provides part-time employment opportunities on campus for eligible students who demonstrate financial need through the FAFSA. Work-study positions offer flexible schedules that accommodate your class schedule, typically 10-20 hours per week. Pay rates start at minimum wage and increase based on experience and position. These positions provide valuable work experience while helping to fund your education. Work-study awards appear on your financial aid package, but you must apply for specific positions."
        
        # Tuition specific response
        if re.search(r'\b(tuition|cost|price|fee|expensive|afford)\b', text):
            return "Tuition rates vary based on your program, residency status, and credit hour load. Current rates are approximately $350 per credit hour for in-state students and $950 per credit hour for out-of-state students. Additional fees apply for labs, online courses, and certain programs. Full-time students (12-18 credits) pay a block rate that caps tuition at 15 credit hours. Payment is due two weeks before the start of each semester. The student accounts office can provide a personalized cost estimate based on your specific situation."
        
        # Financial aid general response
        return "The university offers comprehensive financial aid options including scholarships, grants, loans, and work-study positions. To be considered for all aid types, submit your FAFSA by March 1st for the following academic year. Financial aid packages typically combine different types of aid based on both merit and need. To maintain eligibility, you must make satisfactory academic progress (2.0 GPA and completing 67% of attempted credits). The financial aid office offers one-on-one counseling to help you understand your options and develop a plan to finance your education."

    # Academic standing and GPA questions
    if re.search(r'\b(gpa|grade|academic standing|probation|dean\'s list|honors|transcript)\b', text):
        # GPA calculation and requirements
        if re.search(r'\b(gpa|grade point average|grades|points)\b', text):
            if re.search(r'\b(calculate|computation|figure out|determine)\b', text):
                return "GPA is calculated on a 4.0 scale where A=4.0, B=3.0, C=2.0, D=1.0, and F=0.0 (with plus/minus modifiers affecting the points: A- = 3.7, B+ = 3.3, etc.). To calculate your GPA, multiply the grade points for each course by the credit hours, sum these values, and divide by the total credit hours. For example, an A (4.0) in a 3-credit course equals 12 grade points. The student portal provides both semester and cumulative GPA calculations after grades are posted."
            
            if re.search(r'\b(need|require|maintain|minimum|drop|below|increase|improve)\b', text):
                if re.search(r'\b(below|drop|low)\b', text) and re.search(r'\b(2\.0|2|two)\b', text):
                    return "If your cumulative GPA drops below 2.0, you'll be placed on academic warning for your first semester below this threshold. During this semester, you'll need to work with your advisor to develop an academic success plan and may be required to utilize campus resources like tutoring. If your GPA remains below 2.0 for a second consecutive semester, you'll be placed on academic probation with restrictions on course load and extracurricular activities. A third consecutive semester below 2.0 may result in academic suspension."
                return "You need to maintain a minimum cumulative GPA of 2.0 to remain in good academic standing. Some programs and scholarships require higher GPAs (typically 3.0 or above). The Dean's List requires a semester GPA of 3.5 or higher while taking at least 12 credit hours. Latin honors at graduation require minimum cumulative GPAs of 3.5 (cum laude), 3.7 (magna cum laude), or 3.9 (summa cum laude). Your GPA is updated at the end of each semester after all grades are submitted."
        
        # Dean's List specific response
        if re.search(r'\b(dean\'?s list|academic honors|president\'?s list)\b', text):
            return "The Dean's List recognizes students who achieve academic excellence each semester. To qualify, you must earn a semester GPA of 3.5 or higher while taking at least 12 credit hours of graded coursework (P/F courses don't count toward the 12-hour minimum). Dean's List recognition appears on your transcript and you'll receive a certificate of achievement. Students who make the Dean's List for multiple semesters may qualify for additional scholarship opportunities and are often recognized at departmental award ceremonies."
        
        # Academic probation specific response
        if re.search(r'\b(probation|warning|suspension|dismissal|poor grades|failing)\b', text):
            return "Academic probation occurs when your cumulative GPA falls below 2.0 for two consecutive semesters. While on probation, you'll need to work closely with your advisor, may be limited to 13 credit hours, and must create an academic success plan. You'll also be required to use academic support services such as tutoring and study skills workshops. Students on probation typically have one semester to raise their GPA above 2.0 or face academic suspension, which would require sitting out for at least one semester before applying for readmission."
        
        # Transcript specific response
        if re.search(r'\b(transcript|record|academic history)\b', text):
            return "Your academic transcript is the official record of your coursework, including courses taken, grades received, GPA, and academic standing. Official transcripts can be ordered through the registrar's office for a small fee ($10 per copy) and are required for graduate school applications, job applications, and transferring credits. Unofficial transcripts are available for free through your student portal and are sufficient for most on-campus purposes. Processing time is typically 1-3 business days for official transcripts, and electronic delivery options are available for many institutions."
        
        # General academic standing information
        return "Academic standing is determined by your cumulative GPA. A minimum 2.0 GPA is required to remain in good standing. If your GPA falls below this threshold, you'll progress through academic warning, probation, and potentially suspension if the issue isn't resolved. The university recognizes academic achievement through the Dean's List each semester (3.5+ GPA) and Latin honors at graduation (cum laude, magna cum laude, summa cum laude). Your academic advisor can help you develop strategies to maintain or improve your academic standing."

    # Campus resources questions
    if re.search(r'\b(resource|help|service|support|tutor|counseling|advising|library|lab|center|office)\b', text):
        # Tutoring specific response
        if re.search(r'\b(tutor|academic help|study|learning|homework help)\b', text):
            return "The Academic Success Center offers free tutoring services for most 100-300 level courses. Tutors are upper-level students who excelled in the courses they support and have received specialized training. Both individual and group sessions are available, and you can schedule appointments online through the student portal or drop in during operating hours (Monday-Thursday 9am-8pm, Friday 9am-5pm, Sunday 2pm-8pm). The center also offers supplemental instruction for historically challenging courses and study skills workshops throughout the semester."
        
        # Writing center specific response
        if re.search(r'\b(writing|paper|essay|research paper|thesis|dissertation)\b', text):
            return "The Writing Center provides free assistance with all types of writing assignments at any stage of the writing process, from brainstorming to final editing. Writing consultants can help with structure, clarity, citations, grammar, and discipline-specific writing conventions. Appointments can be scheduled online through the student portal, and both in-person and virtual sessions are available. The center operates Monday-Thursday 10am-7pm and Friday 10am-4pm in the Humanities Building, Room 210. Plan ahead during busy times like midterms and finals when appointments fill quickly."
        
        # Library specific response
        if re.search(r'\b(library|research|book|database|journal|article|study space)\b', text):
            return "The University Library provides access to extensive research materials, study spaces, and academic resources. Services include research assistance from subject librarians, technology checkout (laptops, cameras, recording equipment), interlibrary loan, and group study room reservations. The library operates Monday-Thursday 7am-12am, Friday 7am-8pm, Saturday 10am-8pm, and Sunday 12pm-12am, with extended 24/7 hours during finals week. Online resources include hundreds of specialized databases, e-journals, e-books, and streaming media accessible with your university credentials from anywhere."
        
        # Counseling specific response
        if re.search(r'\b(mental health|counseling|therapy|stress|anxiety|depression|wellness)\b', text):
            return "The Counseling Center offers confidential support for mental health and personal concerns, including individual therapy, group sessions, crisis intervention, and wellness workshops. Services address issues such as stress, anxiety, depression, relationships, adjustment difficulties, and academic concerns. Initial consultations are free for all students, with ongoing services available at low or no cost depending on your insurance. The center operates Monday-Friday 8am-5pm in the Student Health Building, with crisis services available 24/7 by calling the main number. You can schedule an appointment by phone or through the student health portal."
        
        # Career services specific response
        if re.search(r'\b(career|job|intern|internship|resume|interview|employment)\b', text):
            return "Career Services provides comprehensive career development support including personalized career counseling, resume and cover letter reviews, mock interviews, job search strategies, and internship coordination. They maintain an online job board specifically for students and alumni and host career fairs each semester. The office operates Monday-Friday 8:30am-5pm in the Student Union, with extended hours by appointment. Services begin in your first year with career exploration and continue through graduation with job placement assistance. It's recommended to engage with Career Services early and often throughout your academic journey."
        
        # Academic advising specific response
        if re.search(r'\b(advis|advisor|advising|guidance|course selection|schedule|plan|graduation|degree audit)\b', text):
            return "Academic advisors help you navigate degree requirements, plan course schedules, explore majors and minors, and connect with campus resources. First-year students are assigned to professional advisors in the University Advising Center, while upper-division students work with faculty advisors in their major department. Advising appointments are required before registration each semester to review your academic progress and obtain your registration PIN. It's recommended to prepare for these meetings by reviewing your degree audit and creating a tentative schedule. You can schedule advising appointments through the student portal."
        
        # General resources information
        return "The university offers numerous support services to help you succeed academically and personally. These include the Academic Success Center (tutoring), Writing Center, Library, Counseling Center, Career Services, Disability Services, and Student Health Center. Most services are free to enrolled students and can be accessed by appointment or during drop-in hours. These resources are designed to support your holistic development and academic success. I recommend exploring these services early in your academic career rather than waiting until challenges arise. Which specific resource would you like to know more about?"

    # Advising/scheduling an appointment question
    if re.search(r'\b(schedule|appointment|meet|how do i|when can i)\b', text) and re.search(r'\b(advisor|adviser|advising|academic advisor)\b', text):
        return "To schedule an appointment with your academic advisor, log into the student portal and navigate to the 'Advising' section. From there, you can see your assigned advisor and their available appointment times. Choose a time that works for your schedule and include a brief note about what you'd like to discuss. Most advisors offer both in-person and virtual meeting options. First-year students work with advisors in the University Advising Center, while upper-division students work with faculty advisors in their major department. Prepare for your meeting by reviewing your degree audit and bringing questions about your academic path."

    # If no specific category is matched, provide a thoughtful general response
    return f"Thank you for your question. As your academic advisor, I can help with information about courses, majors, registration, deadlines, financial aid, campus resources, and other aspects of university life. Based on your inquiry, I'm not certain exactly what information you're looking for. Could you provide more specific details about your question? This will help me give you the most accurate and helpful response possible."

if __name__ == '__main__':
    print("Starting Flask application...")
    # Set host to '0.0.0.0' to make it accessible from any IP and specify port 5500 explicitly
    app.run(host='0.0.0.0', port=5500, debug=True)