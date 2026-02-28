import json
import os

class QuestionManager:
    def __init__(self):
        # The file path is determined when the user selects a topic
        self.file_path = ""

    def _get_available_topics(self):
        """Scans the directory for .json files and returns a list of dictionaries"""
        files = [f for f in os.listdir('.') if f.endswith('.json') and "_disabled" not in f] #important filter to exclude any disabled question files from the management options.
        topic_list = []
        for f in files:
            pretty_name = f.replace('.json', '').replace('_', ' ').title() #returns the list of abvailable topics in a more user-friendly format.
            topic_list.append({"pretty": pretty_name, "filename": f})
        return topic_list

    def toggle_question_status(self, questions: list):
        """Allows user to find a question by ID and flip its active status"""
        target_id = input("\nEnter the 5-character ID of the question to toggle (or 'q' to cancel): ").strip() #the strip function is used to remove any leading or trailing whitespace from the user's input.
        
        if target_id.lower() == 'q':
            return

        # We look through our list to find the matching ID
        found = False #the command False is used to indicate that we haven't found the question yet. If we find it, we will set this variable to True.
        for q in questions:
            if q.get("id") == target_id:
                found = True
                current_status = "ACTIVE" if q.get("is_active") else "INACTIVE" #we check the current status of the question and prepare a string to show to the user.
                
                print(f"\n--- QUESTION FOUND ---")
                print(f"Text: {q.get('question_text')}") 
                print(f"Current Status: {current_status}")
                
                confirm = input(f"\nDo you want to {'DISABLE' if q.get('is_active') else 'ENABLE'} this question? (y/n): ").lower()
                
                if confirm == 'y':
                    # This is the 'Toggle' logic: if it was True, it becomes False; if False, it becomes True.
                    q["is_active"] = not q.get("is_active")
                    print(f"✅ Question {target_id} is now {'ACTIVE' if q['is_active'] else 'INACTIVE'}.")
                    self._save_changes(questions)
                break
        
        if not found:
            print(f"❌ No question found with ID: {target_id}")

    def _save_changes(self, questions):
        """Writes the updated list back to the JSON file to persist the changes"""
        try:
            with open(self.file_path, "w") as f:
                json.dump(questions, f, indent=4) #the indent=4 argument is used to make the JSON file more human-readable by adding indentation and line breaks.
        except Exception as e:
            print(f"❌ Error saving changes: {e}")

    def list_and_manage(self, topic_info):
        """Shows the list of questions for a topic and provides the toggle menu"""
        self.file_path = topic_info['filename']
        
        if not os.path.exists(self.file_path):
            print("❌ File not found.")
            return

        with open(self.file_path, "r") as f:
            questions = json.load(f) # the json.load function reads the content of the file and converts it from JSON format into Python data structures.

        if not questions:
            print("This topic is empty.")
            return

        while True:
            print(f"\n{'='*60}")
            print(f" MANAGING TOPIC: {topic_info['pretty'].upper()}")
            print(f"{'='*60}")
            
            # Simple list for the user to see IDs and Status
            for q in questions:
                status_icon = "🟢" if q.get("is_active") else "🔴"
                print(f"{status_icon} [{q.get('id')}] {q.get('question_text')[:80]}...")

            print(f"\nOptions: (t) Toggle Status | (b) Back to Topics")
            choice = input("Select: ").lower()

            if choice == 't':
                self.toggle_question_status(questions)
            elif choice == 'b':
                break

    def run(self):
        """Main interaction flow for Management Mode"""
        topics = self._get_available_topics()
        if not topics:
            print("\nNo topics found.")
            return

        print("\n--- SELECT TOPIC TO MANAGE ---")
        for i, t in enumerate(topics):
            print(f"{i + 1}. {t['pretty']}") #we display the list of topics to the user, showing the pretty name for each topic along with a number for selection.
        
        choice = input("\nChoice (or '0' to exit): ")
        if choice == '0': return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(topics):
                self.list_and_manage(topics[idx])
        except ValueError:
            print("❌ Invalid input.")