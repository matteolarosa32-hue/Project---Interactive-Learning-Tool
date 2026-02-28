import json
import os
import random
from datetime import datetime
from generate_mode import LLMClient
from google.genai import types

class TestMode: 
    def __init__(self):
        self.llm = LLMClient()
        self.file_path = ""
        self.results_file = "results.txt" #This is the file where we will append the test results, including the topic and score.

    def _get_available_topics(self):
        """Returns a list of available JSON topics in the directory"""
        files = [f for f in os.listdir('.') if f.endswith('.json')]
        return [{"pretty": f.replace('.json', '').replace('_', ' ').title(), "filename": f} for f in files]

    def _evaluate_freeform(self, question, correct_ref, user_ans):
        """Same logic as Practice Mode: LLM acts as the grader"""
        prompt = (
            f"Question: {question}\n"
            f"Reference Correct Answer: {correct_ref}\n"
            f"User's Answer: {user_ans}\n\n"
            "Is the user's answer conceptually correct? "
            "Respond ONLY with 'CORRECT' or 'INCORRECT' followed by a brief explanation."
        )
        try:
            response = self.llm.client.models.generate_content(
                model=self.llm.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0 # 0.0 is best for strict grading
                )
            )
            if response and response.text: #check response actually has text content before trying to process it.
                result = response.text.upper()
                is_correct = "CORRECT" in result.split()[0]
                return is_correct
            return False
        except Exception as e:
            print(f"Error during grading: {e}")
            return False

    def run_test(self, topic_info):
        self.file_path = topic_info['filename'] #Set the file path based on the user's topic selection. This allows us to load the correct set of questions for the test.
        with open(self.file_path, "r") as f:
            all_questions = json.load(f) 

        # Requirement: Only active questions
        active_pool = [q for q in all_questions if q.get("is_active", True)]

        if not active_pool:
            print("❌ No active questions available for this topic.")
            return

        # Requirement: User selects number of questions
        print(f"\nTotal active questions available: {len(active_pool)}") #counts the active questions for the selected topic and informs the user.
        try:
            num_to_take = int(input(f"How many questions for this test? (1-{len(active_pool)}): "))
            num_to_take = max(1, min(num_to_take, len(active_pool)))
        except ValueError:
            num_to_take = 3 #default number of questions if user input is invalid.
            print("Invalid input. Defaulting to 3 questions.")

        # Requirement: Chosen randomly without repetition
        test_questions = random.sample(active_pool, num_to_take) 
        
        score = 0
        print(f"\n{'='*30}\nTEST START: {topic_info['pretty']}\n{'='*30}") #header for the test session, showing the topic name and some formatting for emphasis.

        for i, q in enumerate(test_questions, 1):
            print(f"\nQuestion {i}/{num_to_take}:") #i.e display question 1/10
            print(f"[{q['type'].upper()}] {q['question_text']}")

            if q['type'] == "mcq":
                for idx, opt in enumerate(q['options'], 1): #we display the multiple choice options for the user, numbering them starting from 1 for easier selection.
                    print(f"  {idx}. {opt}")
                ans = input("Your choice (number): ").strip()
                try:
                    is_correct = (q['options'][int(ans)-1] == q['correct_answer'])
                except:
                    is_correct = False
            else:
                ans = input("Your answer: ").strip()
                print("Grading...")
                is_correct = self._evaluate_freeform(q['question_text'], q['correct_answer'], ans)

            if is_correct:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Incorrect. Correct answer: {q['correct_answer']}")

        # Requirement: Display final score
        print(f"\n{'='*30}")
        print(f"TEST COMPLETE!")
        print(f"Final Score: {score} out of {num_to_take}")
        print(f"{'='*30}")

        # Requirement: Append to results.txt
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #we create a timestamp for when the test was taken.
        log_entry = f"[{timestamp}] Topic: {topic_info['pretty']} | Score: {score}/{num_to_take}\n" #we format the log entry to include the timestamp, topic name, and score in a clear way.
        
        with open(self.results_file, "a") as f:
            f.write(log_entry)
        print(f"Result saved to {self.results_file}")

    def run(self):
        topics = self._get_available_topics()
        if not topics:
            print("No topics found. Generate some questions first!")
            return
            
        print("\nSelect Topic for Test:")
        for i, t in enumerate(topics, 1):
            print(f"{i}. {t['pretty']}")
        
        choice = input("Choice: ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(topics):
                self.run_test(topics[idx])
        except:
            print("Invalid selection.")

if __name__ == "__main__":
    tester = TestMode()
    tester.run()