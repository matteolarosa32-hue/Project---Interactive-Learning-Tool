import json
import os

class DisableEnableManager:
    def __init__(self):
        # We don't need the LLM for this mode, just file management
        pass

    def _get_available_topics(self):
        """Finds all topic files. We ignore the '_disabled' files in the main list."""
        files = [f for f in os.listdir('.') if f.endswith('.json') and "_disabled" not in f]
        return [{"pretty": f.replace('.json', '').replace('_', ' ').title(), "filename": f} for f in files]

    def _load_json(self, filename):
        if not os.path.exists(filename): # If the file doesn't exist, we return an empty list to avoid errors.
            return []
        with open(filename, "r") as f: # We open the file in read mode and attempt to load the JSON data. If the file is empty or not valid JSON, we catch the error and return an empty list.
            try:
                return json.load(f)
            except:
                return []

    def _save_json(self, filename, data):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def run(self):
        topics = self._get_available_topics()
        if not topics:
            print("No topics found.")
            return

        print("\n--- Disable/Enable Questions ---")
        for i, t in enumerate(topics, 1):
            print(f"{i}. {t['pretty']}")
        
        choice = input("\nChoice (or '0' to exit): ")
        if choice == '0': return
        
        try:
            topic = topics[int(choice)-1] 
            active_file = topic['filename']
            disabled_file = active_file.replace(".json", "_disabled.json") # We determine the corresponding disabled file name by adding "_disabled" before the .json extension.
            
            action = input("Do you want to (d)isable an active question or (e)nable a disabled one? Type d or e:").lower()
            
            if action == 'd':
                self.handle_toggle(active_file, disabled_file, "disable") 
            elif action == 'e':
                self.handle_toggle(disabled_file, active_file, "enable")
            else:
                print("Invalid action.")
        except (ValueError, IndexError):
            print("Invalid selection.")

    def handle_toggle(self, source_file, dest_file, mode):
        questions = self._load_json(source_file)
        if not questions:
            print(f"No questions found to {mode}.") #mode is either "e" or "d", so this message will be either "No questions found to enable." or "No questions found to disable."
            return

        print(f"\n--- Available IDs to {mode} ---") #available IDs to disable or enable
        for q in questions:
            # We show the ID and the start of the question text
            print(f"ID: {q['id']} | {q['question_text'][:50]}...") #we display the question text truncated to 50 characters for easier reading in the list.

        target_id = input(f"\nEnter the ID to {mode}: ").strip()
        
        # Find the question in the list

        found_q = None
        for q in questions:
            if str(q['id']) == target_id: #check if the ID matches the user's input.
                found_q = q
                break

        if found_q: #check if we found a question with the given ID before proceeding with the toggle action.
            print(f"\nFound Question: {found_q['question_text']}")
            print(f"Correct Answer: {found_q['correct_answer']}")
            confirm = input(f"Are you sure you want to {mode} this question? (y/n): ").lower()

            if confirm == 'y':
                # 1. Update the internal status
                found_q['is_active'] = (mode == "enable")
                
                # 2. Add to destination
                dest_data = self._load_json(dest_file)
                dest_data.append(found_q)
                self._save_json(dest_file, dest_data)

                # 3. Remove from source
                new_source_data = [q for q in questions if q['id'] != target_id] #we create a new list of questions for the source file that excludes the question we just moved, effectively removing it from the source.
                self._save_json(source_file, new_source_data)

                print(f"✅ Question {target_id} has been {mode}d and moved.")
        else:
            print("❌ ID not found.")

if __name__ == "__main__":
    manager = DisableEnableManager()
    manager.run()