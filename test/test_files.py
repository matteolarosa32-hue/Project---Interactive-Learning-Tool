import json
import os

def test_json_save_and_load(tmp_path):
    """
    Requirement: Test file loading/saving logic.
    This test creates a temporary file, saves a question, and reads it back.
    """
    # 1. Setup: Define a temporary file path and some dummy data
    d = tmp_path / "test_topic.json"
    test_data = [
        {
            "id": "abc12",
            "question_text": "What is 2+2?",
            "correct_answer": "4",
            "is_active": True
        }
    ]

    # 2. Action: Save the data to the temporary file
    with open(d, "w") as f:
        json.dump(test_data, f)

    # 3. Verification: Does the file actually exist?
    assert os.path.exists(d)

    # 4. Action: Load the data back
    with open(d, "r") as f:
        loaded_data = json.load(f)

    # 5. Final Assertion: Is the data we loaded identical to what we saved?
    assert len(loaded_data) == 1
    assert loaded_data[0]["id"] == "abc12"
    assert loaded_data[0]["question_text"] == "What is 2+2?"
    assert loaded_data[0]["is_active"] is True