def test_mcq_scoring():
    """Checks if the matching logic handles extra spaces"""
    correct_answer = "Paris"
    user_choice = " Paris  "
    assert user_choice.strip() == correct_answer

def test_mcq_validation_logic():
    """
    Test Requirement: User's answer must match the 'correct_answer' string.
    """
    # Simulate a question object from your JSON
    mock_question = {
        "id": "q123",
        "type": "mcq",
        "question_text": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct_answer": "Paris"
    }

    # Scenario A: User selects the correct option (Success)
    user_selection_index = 2  # User chose "Paris" (index 2)
    user_answer_text = mock_question["options"][user_selection_index]
    
    # Logic: The validation check
    is_valid = (user_answer_text == mock_question["correct_answer"])
    assert is_valid is True, f"Expected {mock_question['correct_answer']}, but got {user_answer_text}"

    # Scenario B: User selects the wrong option (Failure)
    wrong_selection_index = 0  # User chose "London"
    wrong_answer_text = mock_question["options"][wrong_selection_index]
    
    is_valid_wrong = (wrong_answer_text == mock_question["correct_answer"])
    assert is_valid_wrong is False
