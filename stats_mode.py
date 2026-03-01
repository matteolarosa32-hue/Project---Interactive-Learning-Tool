import json
import os

class StatsManager:
    def __init__(self):
        # We initialize with no path; it gets set when the user picks a topic
        self.file_path = ""

    def _get_available_topics(self): 
        files = [f for f in os.listdir('.') if f.endswith('.json') and "_disabled" not in f] # the listdir function gets all the files in the current directory, it is part of the os module.
        return [{"pretty": f.replace('.json', '').replace('_', ' ').title(), "filename": f} for f in files] #the function returns a list of dictionaries, where each one has a user friendly name.

    def display_topic_report(self, topic_info):
        """Reads the specific file and prints the detailed statistics table"""
        self.file_path = topic_info['filename'] # Set the file path based on the user's topic selection. 
        
        if not os.path.exists(self.file_path): # If the file doesn't exist, we print an error message and return early.
            print(f"❌ Error: {self.file_path} not found.")
            return

        with open(self.file_path, "r") as f:
            try:
                questions = json.load(f) # The json library takes the text in the file and converts it into Python data structures (like lists and dictionaries) that we can work with.
            except json.JSONDecodeError:
                print(f"❌ Error: Could not parse {self.file_path}.") # If the file is not a valid JSON, we catch the error and inform the user.
                return

        if not questions:
            print(f"--- The topic '{topic_info['pretty']}' has no questions yet. ---")
            return

        print(f"\n" + "="*80)
        print(f"FULL REPORT: {topic_info['pretty'].upper()}") #header for the report, showing the topic name in uppercase for emphasis.
        print("="*80)

        for q in questions: #here we unpack the JSON data for each questions.
            # 1. Prepare Data
            qid = q.get("id", "N/A") #.get is a built-in method for dictionaries that allows us to safely access a key. 
            status = "ACTIVE" if q.get("is_active") else "INACTIVE"
            source = q.get("source", "User")
            qtype = q.get("type", "MCQ").upper()
            full_text = q.get("question_text", "")
            
            # 2. Stats Calculation
            stats = q.get("stats", {"shown": 0, "correct": 0})
            shown = stats.get("shown", 0)
            correct = stats.get("correct", 0)
            acc_str = f"{(correct/shown)*100:.1f}%" if shown > 0 else "0.0%"

            # 3. PRINTING THE BLOCK
            # Top line shows metadata
            print(f"ID: {qid} | {qtype} | Source: {source} | {status}")
            # Middle line shows the FULL text
            print(f"Q: {full_text}")
            # Bottom line shows the performance
            print(f"📊 Stats: Shown {shown} times | Accuracy: {acc_str}")
            print("-" * 80) # Separator between questions

        print(f"TOTAL QUESTIONS: {len(questions)}")
        print("="*80 + "\n")

    # --- RESTORED RUN METHOD ---
    def run(self):
        """Main interaction flow for viewing statistics"""
        topics = self._get_available_topics()

        if not topics:
            print("\n📂 No question files found. Please generate some questions first!")
            return

        print("\n--- SELECT A TOPIC TO VIEW STATS ---")
        for i, t in enumerate(topics):
            print(f"{i + 1}. {t['pretty']}")
        print("0. Back to Main Menu")

        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            return
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(topics):
                self.display_topic_report(topics[index])
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a number.")