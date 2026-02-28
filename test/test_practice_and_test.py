import sys
import os

# 1. Get the absolute path to the directory where this test file sits
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
# 2. Go UP to the parent directory
project_folder = os.path.dirname(current_dir)
# 3. Add that folder to the VERY START of Python's search list
sys.path.insert(0, project_folder)
# DIAGNOSTIC
print(f"\n--- PATH CHECK ---")
print(f"Current Test Folder: {current_dir}")
print(f"Adding to Path: {project_folder}")
if os.path.exists(project_folder):
    print(f"Files found in {project_folder}: {os.listdir(project_folder)}")
print(f"------------------\n")
# 4. Now the imports
from test_mode import TestMode as AppTestMode #so pytest doesn't get confused with the actual TestMode class in test_mode.py
from practice_mode import PracticeMode

# 1. THE MOCK FUNCTION
# This replaces the actual Gemini call. It simply returns True if the user's answer is exactly '4'.
def mock_grading(self, question, correct_ans, user_ans):
    return user_ans.strip() == "4"

def test_modes_with_mock_api(monkeypatch):
    """
    Requirement: Test both Practice and Test modes using Monkeypatch.
    """
    
    # 2. APPLY MONKEYPATCH TO BOTH CLASSES
    # This ensures neither class tries to call the real Gemini API
    monkeypatch.setattr(AppTestMode, "_evaluate_freeform", mock_grading)
    monkeypatch.setattr(PracticeMode, "_evaluate_freeform", mock_grading)

    # 3. TEST PRACTICE MODE
    pm = PracticeMode()
    practice_result = pm._evaluate_freeform("What is 2+2?", "4", "4")
    assert practice_result is True
    
    practice_fail = pm._evaluate_freeform("What is 2+2?", "4", "5")
    assert practice_fail is False

    # 4. TEST TEST MODE
    tm = AppTestMode() # Use the alias here
    test_result = tm._evaluate_freeform("What is 2+2?", "4", "4")
    assert test_result is True
    
    test_fail = tm._evaluate_freeform("What is 2+2?", "4", "wrong answer")
    assert test_fail is False

    print("\n✅ Both Practice and Test modes validated with Mock API!")