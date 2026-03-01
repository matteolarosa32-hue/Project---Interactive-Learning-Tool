import json
import random
from datetime import datetime
from generate_mode import LLMClient
from utils import get_available_topics 

class TestMode: 
    def __init__(self): 
        self.llm = LLMClient() #this initializes the LLM client, allowing us to use it for evaluating freeform answers during the test.
        self.file_path = "" 
        self.results_file = "results.txt" #This is the file where we will append the test results, including the topic and score.

    def _evaluate_freeform(self, question, correct_ref, user_ans):
        """Asks the LLM to judge a freeform answer"""
        # If the user input is empty, don't even bother calling the API
        if not user_ans.strip():
            return False, "No answer provided."

        prompt = (
            f"Question: {question}\n"
            f"Reference Correct Answer: {correct_ref}\n"
            f"User's Answer: {user_ans}\n\n"
            "Is the user's answer conceptually correct? "
            "Respond ONLY with 'CORRECT' or 'INCORRECT' followed by a one-sentence explanation."
        )
        try:
            # We use the existing generate_content method from your LLMClient
            response = self.llm.client.models.generate_content(
                model=self.llm.model_name,
                contents=prompt
            ) #the generate_content method is used to send the prompt to the LLM and get a response back.
            
            if response and response.text: #we check if we got a response and if it has text content.
                result = response.text.strip()
               # Extract first word only
                first_word = result.split()[0].strip(",.:!").upper()

                if first_word == "CORRECT":
                    is_correct = True
                elif first_word == "INCORRECT":
                    is_correct = False
                else:
                # If format is unexpected, default to incorrect
                    is_correct = False
                
                return is_correct, response.text.strip() #we return a tuple with the boolean indicating correctness and the full response
            
            # Fallback if response.text is empty to prevent unpacking errors
            return False, "No response from LLM."

        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return False, "Evaluation failed."
                
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
        
        # Initialize the score counter to keep track of how many questions the user answers correctly during the test session.
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
                # FIXED: Unpacking the tuple (boolean, string) to prevent the "always True" tuple bug
                is_correct, feedback = self._evaluate_freeform(q['question_text'], q['correct_answer'], ans)
                print(f"Result: {feedback}")

            if is_correct:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Incorrect. Correct answer: {q['correct_answer']}")

        # Display final score
        print(f"\n{'='*30}")
        print(f"TEST COMPLETE!")
        print(f"Final Score: {score} out of {num_to_take}")
        print(f"{'='*30}")

        # Append to results.txt
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #we create a timestamp for when the test was taken.
        log_entry = f"[{timestamp}] Topic: {topic_info['pretty']} | Score: {score}/{num_to_take}\n" #we format the log entry to include the timestamp, topic name, and score in a clear way.
        
        with open(self.results_file, "a") as f: 
            f.write(log_entry)
        print(f"Result saved to {self.results_file}")

    def run(self):
        topics = get_available_topics()
        if not topics:
            print("No topics found. Generate some questions first!")
            return
            
        print("\nSelect Topic for Test:")
        for i, t in enumerate(topics, 1):
            print(f"{i}. {t['pretty']}")
        
        choice = input("\nChoice (or '0' to exit): ")
        if choice == '0': return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(topics):
                self.run_test(topics[idx])
        except:
            print("Invalid selection.")

if __name__ == "__main__":
    tester = TestMode() #this creates an instance of the TestMode class, which will allow us to call the run method to start the test mode functionality when this script is executed directly.
    tester.run()