from random import sample
from typing import List, Dict
from groq import Groq
import logging
from functools import lru_cache
from config import GROQ_API_KEY, MODEL_NAME

class TechQuestions:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = MODEL_NAME
        self.difficulty_prompts = {
            "basic": "Focus on fundamental concepts and basic implementation questions.",
            "intermediate": "Include questions about best practices and common use cases.",
            "advanced": "Cover complex scenarios, optimization, and architectural decisions."
        }

    @lru_cache(maxsize=128)
    def generate_questions(self, position: str, tech_stack: str, level: str) -> List[str]:
        try:
            prompt = f"""Generate 3 {level} technical interview questions for a {position} position.
            Technical skills: {tech_stack}
            Level guidelines: {self.difficulty_prompts[level]}
            Format: Return exactly 3 questions, one per line."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            questions = response.choices[0].message.content.strip().split("\n")
            return [q.strip() for q in questions if q.strip()]
            
        except Exception as e:
            logging.error(f"Error generating questions: {str(e)}")
            return self._get_default_questions(position, level)

    def get_questions_for_position(self, position: str, tech_stack: List[str] = None) -> List[str]:
        if tech_stack is None:
            tech_stack = []
            
        position = position.lower()
        tech_stack = [t.lower().strip() for t in tech_stack]
        questions = []
        
        for level in ["basic", "intermediate", "advanced"]:
            tech_string = ", ".join(tech_stack) or position
            questions.extend(self.generate_questions(position, tech_string, level))
        
        return questions[:5]

    def _get_default_questions(self, position: str, level: str) -> List[str]:
        defaults = {
            "basic": [
                "What are the key concepts in your field?",
                "Explain version control basics",
                "How do you approach debugging?"
            ],
            "intermediate": [
                "Describe a challenging project",
                "How do you ensure code quality?",
                "Explain your testing strategy"
            ],
            "advanced": [
                "How do you handle scalability?",
                "Explain system design principles",
                "How do you optimize performance?"
            ]
        }
        return defaults.get(level, defaults["basic"])