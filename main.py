from generate_mode import QuestionGenerator
from stats_mode import StatsManager 
from manage_mode import QuestionManager
from practice_mode import PracticeMode
from test_mode import TestMode
from dis_and_en_mode import DisableEnableManager
from utils import get_available_topics

def main():
    # Initialize all our classes 
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
        topics_data = get_available_topics()
        # We extract just the 'pretty' names for the print statement
        pretty_names = [t['pretty'] for t in topics_data]
        
        if pretty_names:
            print(f"📂 Existing Topics Found: {', '.join(pretty_names)}")
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