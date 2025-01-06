CONVERSATION_PROMPTS = {
    "start": "Welcome! Type 'start' to begin.",
    "greeting": "Hello! I'm the TalentScout AI Hiring Assistant. Could you please share your full name?",
    "email": "Great! Could you please provide your email address?",
    "phone": "What's your contact number?",
    "experience": "How many years of professional experience do you have? [e.g. 2.5]",
    "location": "Where are you currently located?",
    "position": "Which position are you interested in?\nAvailable positions:\n- Python Developer\n- Machine Learning Engineer\n- Data Analyst",
    "tech_stack": "Please list your technical skills relevant to the position (programming languages, frameworks, tools):",
    "work_experience": "Please describe your relevant work experience and key projects:",
    "resume_link": "Please provide a link to your resume (must start with http:// or https://):",
    "technical_questions": "Based on your position, here are some technical questions: [enter start to begin]",
    "farewell": "Thank you for your time! We'll review your information and get back to you soon. We'll contact you at {email} if your profile matches our requirements."
}

SYSTEM_PROMPT = """You are an AI hiring assistant for TalentScout, a tech recruitment agency. 
Your role is to gather candidate information and assess their technical skills.
Be professional but friendly, and ensure responses are relevant to the candidate's chosen position."""

TECH_QUESTIONS_PROMPT = """Generate position-specific technical questions for a {position} role.
Include a mix of Python fundamentals and {position}-specific concepts.
Questions should assess both theoretical knowledge and practical experience.
Focus areas for {position}: {focus_areas}"""

POSITION_FOCUS_AREAS = {
    "python developer": "Python, web frameworks, databases, API design",
    "machine learning": "Python, ML algorithms, deep learning, data preprocessing",
    "data analyst": "Python, data visualization, statistical analysis, SQL"
}