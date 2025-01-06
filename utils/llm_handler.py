from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

class LLMHandler:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = MODEL_NAME

    def get_response(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        return completion.choices[0].message.content