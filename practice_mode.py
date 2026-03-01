import json
import os
import random
from generate_mode import LLMClient

class PracticeMode:
    def __init__(self): # We initialize the LLM client and set up a placeholder for the file path that will be determined when the user selects a topic.
        self.llm = LLMClient()
        self.file_path = ""

    def _get_available_topics(self): 
        files = [f for f in os.listdir('.') if f.endswith('.json') and "_disabled" not in f] # the listdir function gets all the files in the current directory, it is part of the os module.
        return [{"pretty": f.replace('.json', '').replace('_', ' ').title(), "filename": f} for f in files] #the function returns a list of dictionaries, where each one has a user friendly name.

    def _calculate_weight(self, q):
        """Strategic Weight: Higher weight = higher chance of being picked"""
        stats = q.get("stats", {"shown": 0, "correct": 0}) #get method used to safely access the stats dictionary, for each question.
        shown = stats.get("shown", 0) #get method used to safely access the number of times the question has been shown, defaulting to 0 if not present.
        correct = stats.get("correct", 0) #get method used to safely access the number of times the question has been answered correctly, defaulting to 0 if not present.

        if shown == 0:
            return 10.0 # if a question has never been shown, we give it a high weight to ensure it gets picked at least once.
        
        accuracy = correct / shown
        # Weight formula: 10 - (Accuracy * 9). 
        # 0% accuracy = 10.0 weight | 100% accuracy = 1.0 weight.
        return max(1.0, 10.0 - (accuracy * 9)) #1 is a floor, making sure that weight never goes below 1.

    def _evaluate_freeform(self, question, correct_ref, user_ans):
        """Asks the LLM to judge a freeform answer"""
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
                result = response.text.strip().upper()
                
                # Check for INCORRECT first because 'CORRECT' is a substring of 'INCORRECT'
                if result.startswith("INCORRECT"):
                    is_correct = False
                elif result.startswith("CORRECT"):
                    is_correct = True
                else:
                    # Fallback: look for the word specifically using split
                    words = result.split()
                    first_word = words[0].strip(',.:') if words else ""
                    is_correct = (first_word == "CORRECT")
                
                return is_correct, response.text.strip() #we return a tuple with the boolean indicating correctness and the full response from the LLM for feedback.
            
            # Fallback if response.text is empty to prevent "None is not iterable" error
            return False, "No response from LLM."

        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return False, "Evaluation failed."

    def _save_stats(self, questions):
        with open(self.file_path, "w") as f:
            json.dump(questions, f, indent=4) #the json.dump function is used to write the updated list of questions back to the JSON file.

    def run_session(self, topic_info): #core function that runs the practice session for a given topic.
        self.file_path = topic_info['filename'] 
        with open(self.file_path, "r") as f:
            all_questions = json.load(f)

        active_questions = [q for q in all_questions if q.get("is_active", True)]

        if not active_questions:
            print("❌ No active questions in this topic!")
            return

        print(f"\n--- PRACTICE SESSION: {topic_info['pretty']} ---")
        print("(Type 'q' or 'exit' at any time to stop)")

        while True:
            # 1. Selection Strategy
            weights = [self._calculate_weight(q) for q in active_questions] #recalls the _calculate_weight method for each active question to determine how likely it is to be selected.
            q = random.choices(active_questions, weights=weights, k=1)[0] #cumulative distribution function, the largest weight has the hiighest chance to be selected.

            print(f"\n[{q['type'].upper()}] {q['question_text']}") #we print the question type and the question text for the user to see before they answer.
            
            # 2. Get User Input
            if q['type'] == "mcq":
                for i, opt in enumerate(q['options']):
                    print(f"  {i+1}. {opt}")
                user_input = input("Your choice (number) or 'q' to quit: ").strip().lower() #strip and lower are used to clean up user input (no spaces and uppercase letters)
            else:
                user_input = input("Your answer (or 'q' to quit): ").strip().lower()

            if user_input in ['q', 'exit']:
                print(f"\nEnding session for {topic_info['pretty']}. Great work!")
                break 

            # 3. Evaluation Logic
            if q['type'] == "mcq":
                try:
                    idx = int(user_input) - 1 #-1 because we displayed options starting from 1, but list indices start from 0.
                    is_correct = (q['options'][idx] == q['correct_answer']) #correct answer is stored in the json file for mcqs, so we can directly compare with user's answer.
                except (ValueError, IndexError):
                    print("⚠️ Invalid choice. Skipping question.")
                    continue # Restarts the loop for a new question
            else:
                print("Evaluating...")
                is_correct, feedback = self._evaluate_freeform(q['question_text'], q['correct_answer'], user_input)
                print(f"Result: {feedback}")

            # 4. Update Statistics
            q['stats']['shown'] += 1 #this were initiated with a default of 0 in get_questions.py.
            if is_correct:
                print("✅ Correct!")
                q['stats']['correct'] += 1 #increment the correct count if the user's answer is correct.
            else:
                print(f"❌ Incorrect. The right answer was: {q['correct_answer']}")

            # 5. Persist changes
            self._save_stats(all_questions)

    def run(self): #set the stage for the run session.
        topics = self._get_available_topics() 
        if not topics: return
        print("\n--- SELECT TOPIC TO PRACTICE ---")
        for i, t in enumerate(topics):
            print(f"{i+1}. {t['pretty']}")
    
        choice = input("\nChoice (or '0' to exit): ")
        if choice == '0': return

        try:
            idx = int(choice) - 1 #we convert the user's choice to an index to access the corresponding topic from the list.
            if 0 <= idx < len(topics):
                self.run_session(topics[idx]) #we call the run_session method with the selected topic's information to start the practice session.
        except:
            pass