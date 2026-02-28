import os
from generate_mode import QuestionGenerator
from stats_mode import StatsManager 
from manage_mode import QuestionManager
from practice_mode import PracticeMode
from test_mode import TestMode
from dis_and_en_mode import DisableEnableManager

def get_existing_topics():
    """Scans the current directory for .json files and returns a list of topics"""
    files = os.listdir('.')
    
    # Filter: Only take .json files, but EXCLUDE system files or disabled question files
    # This prevents 'disabled_questions.json' or 'topic_disabled.json' from appearing
    json_files = [
        f for f in files 
        if f.endswith('.json') 
        and f != 'disabled_questions.json' 
        and not f.endswith('_disabled.json')
    ]
    
    topics = []
    for f in json_files:
        name_no_ext = f.replace('.json', '')
        pretty_name = name_no_ext.replace('_', ' ').title()
        topics.append(pretty_name)
    
    return topics

def main():
    # Initialize all our specialized managers
    generator = QuestionGenerator()
    stats_viewer = StatsManager()
    manager = QuestionManager()
    practice = PracticeMode()
    test = TestMode()
    dis_en_manager = DisableEnableManager()

    while True:
        print("\n" + "="*40)
        print("   AI-POWERED LEARNING COMPANION")
        print("="*40)
        
# --- SHOW EXISTING TOPICS ---
        existing_topics = get_existing_topics()
        
        if existing_topics:
            print(f"📂 Existing Topics Found: {', '.join(existing_topics)}")
        else:
            print("📂 No topics found yet. Start by generating some!")
        
        print("\nMain Menu:")
        print("1. Generate New Questions (LLM)")
        print("2. View Performance Statistics")
        print("3. Manage Questions (Toggle Active/Inactive)")
        print("4. Practice Questions")
        print("5. Take a Test")
        print("6. Disable/Enable Questions")
        print("0. Exit")
        
        choice = input("\nSelect an option: ")

        if choice == "1":
            generator.run()
        elif choice == "2":
            stats_viewer.run()
        elif choice == "3":
            manager.run() 
        elif choice == "4":
            practice.run()
        elif choice == "5":
            test.run()
        elif choice == "6":
            dis_en_manager.run()
        elif choice == "0":
            print("Goodbye! Happy learning.")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()