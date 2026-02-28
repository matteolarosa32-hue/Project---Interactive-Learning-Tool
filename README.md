# Project - Interactive Learning Tool

A comprehensive Python study assistant powered by the Google Gemini API. This project serves as a personalized tutor, helping users master new subjects through AI-generated content and intelligent feedback.

---

## Overview
The Interactive Learning Tool allows users to explore any topic of their choice. By leveraging Large Language Models (LLM), the tool dynamically generates study material, providing a custom learning path that evolves with the user's progress. The primary purpose of the project is to assist in learning about a new subject or topic from scratch.

---

## Functional Modes
### Generate Mode
The Generate Mode is the starting point of the learning process. It interfaces with the Google Gemini API to dynamically create new question sets based on a user-provided topic. This mode handles the logic of prompting the AI, parsing the response into structured data, and saving the results into a JSON file for future use in the Practice and Test modes.

### Practice Mode
Designed for low-pressure learning, this mode allows users to practice on a topic of their choice. Users receive immediate feedback on their answers, allowing them to learn and correct mistakes in real-time.

### Test Mode
Simulates a formal exam environment. Users are graded on their performance through simulated tests, helping them gauge their readiness on a specific topic.

### Stats Mode
Tracks the learning journey by displaying statistics regarding progress on a specific topic. It specifically shows the accuracy percentage for all active questions to help visualize improvement.

### Management and Control
- **Manage Mode**: Allows for the organization of question banks, including the ability to mark questions as active or inactive.
- **Disable and Enable Mode**: Provides the specific feature to enable or disable questions from appearing in the Practice and Test modes, allowing for focused study sessions.

---

## Intelligent Grading
This tool supports both:
1. Multiple Choice Questions (MCQ): Automated validation for quick assessment.
2. Freeform Answers: Uses intelligent AI grading to evaluate the conceptual accuracy of text responses, moving beyond simple keyword matching.

---

## Project Structure
project/
├── .env                    # Environment variables (Private API Key)
├── .gitignore              # Defines files to be ignored by Git (e.g., .env, pycache)
├── main.py                 # Application entry point
├── generate_mode.py        # AI question generation logic
├── stats_mode.py           # Performance tracking and math
├── test_mode.py            # Assessment session logic
├── practice_mode.py        # Interactive learning logic
├── manage_mode.py          # Question bank organization
├── dis_and_en_mode.py      # Feature toggling logic
├── results.txt             # Record of user performance (logged automatically)
└── test/                   # Automated test suite
    ├── test_files.py       # Validates file loading and saving
    ├── test_mcq.py         # Tests multiple-choice logic
    ├── test_stats.py       # Verifies accuracy formula calculations
    └── test_practice_and_test_mode.py  # Mocked LLM evaluation tests

---

## Automated Testing
The project maintains code quality through a robust pytest suite. To ensure reliability and cost-efficiency, the suite uses Monkeypatching to simulate LLM interactions and API responses.
To run the full test suite:
Bash
python -m pytest test/

---

## Getting Started

### Requirements
Install the necessary Python libraries:
Bash
pip install google-genai pytest python-dotenv

### API Configuration
To protect sensitive credentials, this project uses an environment file.
Create a file named .env in the root directory.
Add your Google Gemini API key:
Plaintext
GEMINI_API_KEY=your_actual_key_here
Note: The .env file is excluded from version control via .gitignore to ensure security.

### Running the Application
Once the API key is configured, start the tool:
Bash
python main.py
Deliverables
Included in this repository are the generated output files, including question banks (.json) and the performance history (results.txt), as required by the project specifications.
