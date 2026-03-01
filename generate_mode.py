import os
import re
import json
import uuid
from typing import List, Optional, Literal, cast
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

# --- DATA MODELS (Pydantic for JSON Validation) ---

class QuestionSchema(BaseModel): #whenever we want to create a new question, we will create an instance of this class. 
    """BaseModel is a class from the Pydantic library that provides data validation and parsing. It automatically checks if data coming from the LLM matches the expected strucutre."""
    """Blueprint for a single question from the LLM"""
    type: Literal["mcq", "freeform"] #value of type can only be "mcq" or "freeform". This is a validation rule that ensures that the LLM response is consistent and predictable.
    question_text: str 
    options: Optional[List[str]] = Field(None, description="List of 4 options if MCQ, else null") #if LLM is making a freeform questions, options will be null.
    correct_answer: str

class QuestionList(BaseModel):
    """Wrapper for the list of questions"""
    questions: List[QuestionSchema]

# --- LLM CLIENT (OOP) ---

class LLMClient:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Error: GEMINI_API_KEY not found in environment variables.")
        
        # Initialize the Google GenAI Client
        self.client = genai.Client(api_key=self.api_key)
        # Using a stable version string to avoid 404 errors found in some SDK versions
        self.model_name = "gemini-2.5-flash" 

    def fetch_questions(self, topic: str, existing_questions: Optional[List[str]] = None) -> List[QuestionSchema]: 
        """Optional parameter existing_questions is a list of question texts that we have already generated for this topic, which we will pass to the LLM to avoid duplicates"""
        """Calls the LLM and returns a list of parsed Question objects"""
        
        # We build the exclusion text if we have existing questions to avoid repeats
        exclusion_text = ""
        if existing_questions:
            recent_qs = "\n".join(existing_questions[-15:])
            """We take the last 15 questions as context for the LLM to avoid generating similar ones. This is a simple way to provide recent history without overwhelming the prompt.""" 
            exclusion_text = f"DO NOT repeat or overlap with these existing questions:\n{recent_qs}\n"

        prompt = (
            f"Generate 6 FRESH educational questions about: {topic}. "
            f"{exclusion_text}"
            f"Provide exactly 4 Multiple Choice Questions (MCQ) and 2 Freeform questions."
        )
        
        try:
             
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=QuestionList,
                temperature=0.9
                ) #temperature is a parameter that controls the creativity of the LLM's responses. A higher value like 0.9 encourages more diverse and creative outputs.
            )
            
            parsed_data = cast(QuestionList, response.parsed) #we cast the parsed response to our QuestionList model, which allows us to work with it as a structured Python object. 
            
            if parsed_data and hasattr(parsed_data, 'questions'): #has attribute check used to ensure that the parsed data has the expected structure.
                return parsed_data.questions
            return [] 
            
        except Exception as e:
            if "429" in str(e):
                print("\n⚠️  QUOTA EXHAUSTED: You're moving too fast for the free tier!")
                print("Wait about 30 seconds before trying to generate more questions.")
            else:
                print(f"❌ API Error: {e}")
            return []

# --- GENERATION MANAGER ---

class QuestionGenerator:
    def __init__(self):
        self.llm = LLMClient()
        # self.file_path is now set dynamically in the run() method based on the topic
        self.file_path = "" 

    def _get_filename_from_topic(self, topic: str) -> str:
        """Helper to convert topic into a clean filename like 'learn_english.json'"""
        clean_topic = re.sub(r'[^\w\s-]', '', topic).strip().lower()
        return clean_topic.replace(' ', '_') + ".json"

    def _get_existing_texts(self) -> List[str]:
        """Reads existing questions to prevent duplicates"""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                return [q.get("question_text", "") for q in data]
        except:
            return []

    def save_to_json(self, new_questions: List[dict]):
        """Persists questions to a JSON file, maintaining existing data"""
        data = []
        if os.path.exists(self.file_path): #if the file already exists, we read the existing data and append the new questions to it. This way we don't overwrite previous questions.
            with open(self.file_path, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError: #if the file exists but is empty or not valid JSON, we catch the error and just start with an empty list.
                    data = []

        data.extend(new_questions) #command to add the new questions to the existing data list.
        
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def run(self):
        """Main flow for the Generate Questions Mode"""
        topic = input("\nEnter an existing topic for new questions or type a new topic: ")
        
        # Determine the specific file for this topic
        self.file_path = self._get_filename_from_topic(topic)
        
        # Gather existing questions to send to the LLM as context
        existing_texts = self._get_existing_texts()
        
        if os.path.exists(self.file_path):
            print(f"--- Topic found! Adding unique questions to: {self.file_path} ---")
        else:
            print(f"--- New topic! Questions will be saved to: {self.file_path} ---")

        print(f"--- Requesting questions for '{topic}' from AI... ---")
        
        # Pass the existing questions to the fetcher to avoid repeats
        raw_questions = self.llm.fetch_questions(topic, existing_texts)
        
        if not raw_questions:
            print("Failed to generate questions. Please check your API key or connection.")
            return

        accepted_questions = []

        for q in raw_questions:
            print(f"\n--- GENERATED {q.type.upper()} ---")
            print(f"Question: {q.question_text}")
            if q.type == "mcq":
                print(f"Options: {', '.join(q.options or [])}")
            print(f"Correct Answer: {q.correct_answer}")

            action = input("\nAccept (a), Reject (r), or Edit (e)? ").lower() #here we give the user the option to accept, reject or edit each question generated by the LLM.

            if action in ['a', 'e']:
                if action == 'e':
                    q.question_text = input(f"Edit text [{q.question_text}]: ") or q.question_text
                    
                    # --- Logic to edit MCQ options ---
                    if q.type == "mcq" and q.options:
                        new_options = []
                        print("\nEditing Options (Press Enter to keep original):")
                        for i, opt in enumerate(q.options): #we loop through each option and give the user the chance to edit it.
                            edited_opt = input(f"Option {i+1} [{opt}]: ") or opt #if the user presses enter without typing anything, we keep the original option.
                            new_options.append(edited_opt) 
                        q.options = new_options
                    
                    q.correct_answer = input(f"Edit answer [{q.correct_answer}]: ") or q.correct_answer

                # Prepare dictionary with mandatory metadata
                q_dict = q.model_dump()
                q_dict.update({
                    "id": str(uuid.uuid4().hex)[:5], #this generates a Universally Unique Identifier (UUID) and takes the first 5 characters to create a short ID for each question.
                    "topic": topic,
                    "is_active": True,
                    "source": "LLM",
                    "stats": {"shown": 0, "correct": 0} #here we are initializing the stats for each question, which will be updated later when the user interacts with the questions in practice mode.
                })
                accepted_questions.append(q_dict)

        if accepted_questions:
            self.save_to_json(accepted_questions)
            print(f"\n✅ Successfully saved {len(accepted_questions)} questions to {self.file_path}!")
        else:
            print("\nNo questions were saved.")

# --- ENTRY POINT ---
# This allows us to run the question generator directly, and also makes it easy to import the LLMClient class in other scripts if needed.
if __name__ == "__main__":
    generator = QuestionGenerator()
    generator.run()