from datetime import datetime
import re
from pydantic import BaseModel, EmailStr, field_validator, HttpUrl
from typing import List, Optional

class CandidateInfo(BaseModel):
    name: str
    email: EmailStr
    phone: str
    experience: float
    location: str
    position: str
    tech_stack: List[str]
    work_experience: str 
    resume_link: HttpUrl
    answers: Optional[str] = None
    timestamp: datetime = datetime.now()

    @field_validator('phone')
    def validate_phone(cls, v):
        # Simplified phone validation that accepts common formats
        v = v.strip()
        if not re.match(r'^\+?[\d\s-]{10,15}$', v):
            raise ValueError('Please enter a valid phone number (e.g., +1-234-567-8900)')
        return v

    @field_validator('name')
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty')
        if not re.match(r'^[a-zA-Z\s-]+$', v):
            raise ValueError('Name must only contain letters, spaces, or hyphens')
        return v.title()

    @field_validator('position')
    def validate_position(cls, v):
        valid_positions = ['python developer', 'machine learning', 'data analyst']
        if v.lower() not in valid_positions:
            raise ValueError(f'Position must be one of: {", ".join(valid_positions)}')
        return v.lower()

    @field_validator('experience')
    def validate_experience(cls, v):
        try:
            exp = float(v)
            if exp < 0:
                raise ValueError('Experience cannot be negative')
            if exp > 50:
                raise ValueError('Experience seems unrealistic')
            return exp
        except ValueError:
            raise ValueError('Please enter a valid number for experience')

    @field_validator('location')
    def validate_location(cls, v):
        if not v.strip():
            raise ValueError('Location cannot be empty')
        return v.title()

    @field_validator('tech_stack')
    def validate_tech_stack(cls, v):
        if not isinstance(v, list) or not v:
            raise ValueError('Please provide at least one technical skill')
        return [tech.strip().lower() for tech in v if tech.strip()]
    
    @field_validator('work_experience')
    def validate_work_experience(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Work experience details cannot be empty')
        if len(v) < 10:
            raise ValueError('Please provide more detailed work experience')
        return v

    @field_validator('resume_link')
    def validate_resume_link(cls, v):
        v = str(v).strip()
        if not v:
            raise ValueError('Resume link cannot be empty')
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Please provide a valid HTTP/HTTPS URL')
        return v

    @field_validator('answers')
    def validate_answers(cls, v):
        if v is None:
            return None
            
        v = v.strip()
        if not v:
            raise ValueError('Answers cannot be empty')
            
        # Split into individual Q&A pairs
        qa_pairs = v.split('\n')
        
        # Validate each answer
        for qa in qa_pairs:
            if qa.startswith('A:'):
                answer = qa.replace('A:', '').strip()
                if len(answer) < 10:
                    raise ValueError('Please provide more detailed answers (minimum 10 characters)')
                if answer.lower() in ['idk', 'i don\'t know', 'na', 'n/a']:
                    raise ValueError('Please provide meaningful answers to all questions')
        
        return v