import json
from datetime import datetime
import os
import logging
from utils.llm_handler import LLMHandler
from utils.data_validator import CandidateInfo
from utils.tech_questions import TechQuestions
from templates.prompts import CONVERSATION_PROMPTS
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class ConversationManager:
    def __init__(self):
        self.llm = LLMHandler()
        self.tech_questions = TechQuestions()
        self.current_stage = "start"
        self.candidate_info = {}
        self.stages = [
            "start", "greeting", "email", "phone", "experience", "location", 
            "position", "tech_stack", "work_experience", "resume_link",  
            "technical_questions", "farewell"
        ]
        self.tech_questions_asked = False
        self.current_question_index = 0
        self.questions = []
        self.answers = []

    def process_input(self, user_input):
        logging.debug(f"Processing input at stage '{self.current_stage}' with input: {user_input}")
        
        if self.current_stage == "start" and user_input.lower() == "start":
            self.current_stage = "greeting"
            return CONVERSATION_PROMPTS["greeting"]
        
        if self.current_stage == "technical_questions":
            if not self.tech_questions_asked:
                self.tech_questions_asked = True
                return self.handle_technical_questions()
            else:
                # Store answer
                self.answers.append(user_input.strip())
                
                # Move to next question or finish
                if self.current_question_index < len(self.questions) - 1:
                    self.current_question_index += 1
                    return f"Question {self.current_question_index + 1}:\n{self.questions[self.current_question_index]}"
                else:
                    # Format Q&A pairs
                    qa_pairs = []
                    for i, (q, a) in enumerate(zip(self.questions, self.answers)):
                        qa_pairs.extend([f"Q{i+1}: {q}", f"A: {a}", ""])
                    
                    self.candidate_info["answers"] = "\n".join(qa_pairs).strip()
                    self.current_stage = "farewell"
                    
                    if self.validate_and_store_data():
                        return CONVERSATION_PROMPTS["farewell"].format(
                            email=self.candidate_info.get("email", "")
                        )
                    return "Thank you for your responses. We will review and get back to you."
        
        try:
            self.validate_input(user_input)
            self.update_candidate_info(user_input)
            next_stage = self.get_next_stage()
            self.current_stage = next_stage
            return CONVERSATION_PROMPTS[next_stage]
        except ValueError as e:
            logging.error(f"Validation error: {e}")
            return f"Invalid input: {e}. Please try again."
        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
            return "An unexpected error occurred. Please try again."


    def validate_input(self, user_input):
        if not user_input or len(user_input.strip()) == 0:
            raise ValueError("Input cannot be empty")
        
        if self.current_stage == "greeting":
            if not re.match(r'^[a-zA-Z\s-]+$', user_input):
                raise ValueError("Name must only contain letters, spaces, or hyphens")
        
        if self.current_stage == "email" and "@" not in user_input:
            raise ValueError("Please enter a valid email address")
        
        if self.current_stage == "phone":
            # Simplified phone validation
            phone_pattern = re.compile(r'^\+?[\d\s-]{10,15}$')
            if not phone_pattern.match(user_input.strip()):
                raise ValueError("Please enter a valid phone number (e.g., +91 1234567890)")
        
        if self.current_stage == "experience":
            try:
                experience = float(user_input)
                if experience < 0 or experience > 50:
                    raise ValueError("Experience must be between 0 and 50 years")
            except ValueError:
                raise ValueError("Please enter a valid number for years of experience")
            
        if self.current_stage == "work_experience":
            if len(user_input.strip()) < 10:
                raise ValueError("Please provide more detailed work experience")
                
        if self.current_stage == "resume_link":
            if not user_input.startswith(('http://', 'https://')):
                raise ValueError("Please provide a valid HTTP/HTTPS URL for your resume")
        
        if self.current_stage == "position":
            valid_positions = ["python developer", "machine learning", "data analyst"]
            if user_input.lower().strip() not in valid_positions:
                raise ValueError(f"Please select from available positions: {', '.join(valid_positions)}")


    def update_candidate_info(self, user_input):
        self.candidate_info[self.current_stage] = user_input.strip()
        logging.debug(f"Updated candidate info: {self.candidate_info}")

    def get_next_stage(self):
        current_index = self.stages.index(self.current_stage)
        return self.stages[min(current_index + 1, len(self.stages) - 1)]

    def handle_technical_questions(self):
        try:
            position = self.candidate_info.get("position", "").lower().strip()
            tech_stack = [
                t.strip() for t in self.candidate_info.get("tech_stack", "").split(",") if t.strip()
            ]
            
            if not tech_stack:
                self.current_stage = "farewell"
                return "No valid technologies provided. " + CONVERSATION_PROMPTS.get("farewell", "Goodbye.")
            
            # Generate and store questions
            self.questions = self.tech_questions.get_questions_for_position(position, tech_stack)
            self.current_question_index = 0
            self.answers = []
            
            # Return first question
            return f"Please answer the following questions one by one:\n\nQuestion 1:\n{self.questions[0]}"
            
        except Exception as e:
            logging.error(f"Error generating technical questions: {e}")
            self.current_stage = "farewell"
            return f"Error generating questions: {e}. " + CONVERSATION_PROMPTS.get("farewell", "Goodbye.")

    def validate_and_store_data(self):
        try:
            candidate_data = {
                "name": self.candidate_info.get("greeting", "").strip(),
                "email": self.candidate_info.get("email", "").strip(),
                "phone": self.candidate_info.get("phone", "").strip(),
                "experience": float(self.candidate_info.get("experience", 0)),
                "location": self.candidate_info.get("location", "").strip(),
                "position": self.candidate_info.get("position", "").strip().lower(),
                "tech_stack": [t.strip() for t in self.candidate_info.get("tech_stack", "").split(",") if t.strip()],
                "work_experience": self.candidate_info.get("work_experience", "").strip(),
                "resume_link": self.candidate_info.get("resume_link", "").strip(),
                "answers": self.candidate_info.get("answers", "").strip(),
                "questions": self.candidate_info.get("questions", []),  # Store questions too
                "timestamp": datetime.now().isoformat()
            }
            
            validated_data = CandidateInfo(**candidate_data)
            
            os.makedirs('candidates', exist_ok=True)
            safe_name = validated_data.name.replace(' ', '_').lower()
            filename = f"candidates/{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(candidate_data, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            logging.error(f"Error storing candidate data: {str(e)}")
            return False
