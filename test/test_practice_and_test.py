import sys
import os

# 1. Get the directory of the test file
current_test_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go UP one level to reach the folder where your logic files live
project_root = os.path.abspath(os.path.join(current_test_dir, '..'))

# DIAGNOSTIC PRINT (To confirm we found the right place)
print(f"\n--- RE-DEBUGGING PATHS ---")
print(f"Now looking in: {project_root}")
if os.path.exists(project_root):
    print(f"Files found here: {os.listdir(project_root)}")
print(f"--------------------------\n")

# 3. Add that root to the path
sys.path.insert(0, project_root)

# 4. Now the imports should work
from practice_mode import PracticeMode
from test_mode import TestMode as AppTestMode  # Renaming to avoid confusion with the test function


def mock_grading(self, question, correct_ans, user_ans):
    return user_ans.strip() == "4"


def test_modes_with_mock_api(monkeypatch):
    """
    Requirement:
    Test both PracticeMode and TestMode
    while mocking the Gemini API evaluation method.
    """

    # Apply monkeypatch to BOTH classes
    monkeypatch.setattr(AppTestMode, "_evaluate_freeform", mock_grading)
    monkeypatch.setattr(PracticeMode, "_evaluate_freeform", mock_grading)

    # -----------------------------
    # TEST PRACTICE MODE
    # -----------------------------
    pm = PracticeMode()

    practice_success = pm._evaluate_freeform("What is 2+2?", "4", "4")
    assert practice_success is True

    practice_fail = pm._evaluate_freeform("What is 2+2?", "4", "5")
    assert practice_fail is False

    # -----------------------------
    # TEST TEST MODE
    # -----------------------------
    tm = AppTestMode()

    test_success = tm._evaluate_freeform("What is 2+2?", "4", "4")
    assert test_success is True

    test_fail = tm._evaluate_freeform("What is 2+2?", "4", "wrong answer")
    assert test_fail is False

    print("\n✅ Both Practice and Test modes validated with Mock API!")