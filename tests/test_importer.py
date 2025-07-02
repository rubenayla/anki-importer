import pytest
from unittest.mock import MagicMock
import os
import yaml

# Add the root directory to the Python path to allow imports from the main script
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import AnkiMdImporter, AnkiConnect

@pytest.fixture
def mock_anki_connect(mocker):
    """Fixture to mock the AnkiConnect class."""
    mock = MagicMock(spec=AnkiConnect)
    mock.get_model_names.return_value = ["Basic", "MCQ Ultimate V2.1 shuffling default"]
    mock.get_model_field_names.return_value = ["Question", "Correct", "Incorrect1", "Incorrect2", "Incorrect3", "Explanation"]
    mocker.patch('main.AnkiConnect', return_value=mock)
    return mock

@pytest.fixture
def temp_config_file(tmp_path):
    """Fixture to create a temporary config file in YAML format."""
    config_data = {
        "deck_name": "TestDeck",
        "card_model": "MCQ Ultimate V2.1 shuffling default",
        "fields": {
            "question": "Question",
            "correct_answer": "Correct",
            "incorrect_answers": [
                "Incorrect1",
                "Incorrect2",
                "Incorrect3"
            ],
            "explanation": "Explanation"
        },
        "questions_file": "test_questions.md"
    }
    config_file = tmp_path / "config.yml"
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f)
    return str(config_file)

@pytest.fixture
def temp_questions_file(tmp_path):
    """Fixture to create a temporary questions markdown file."""
    markdown_content = """
- What is the capital of France?
    1. Berlin
    2. Madrid
    3. Paris
    4. Rome
    - Answer: 3, Paris is the capital of France.

- Which planet is known as the Red Planet?
    1. Earth
    2. Mars
    3. Jupiter
    - Answer: 2, Mars is often called the Red Planet.
"""
    questions_file = tmp_path / "test_questions.md"
    with open(questions_file, 'w') as f:
        f.write(markdown_content)
    return str(questions_file)

def test_extract_questions(temp_questions_file):
    """Test that questions are extracted correctly from the markdown file."""
    with open(temp_questions_file, 'r') as f:
        content = f.read()
    questions = AnkiMdImporter.extract_questions(content)
    assert len(questions) == 2
    assert questions[0][0].strip() == "What is the capital of France?"
    assert "Paris" in questions[0][1]
    assert questions[0][2].strip().startswith("3, Paris")

def test_process_questions_with_mock(mock_anki_connect, temp_config_file, temp_questions_file):
    """Test the main logic of processing questions and adding notes using a mock."""
    # Change working directory to the temp path so the script can find the files
    os.chdir(os.path.dirname(temp_config_file))

    importer = AnkiMdImporter(os.path.basename(temp_config_file))
    importer.anki = mock_anki_connect # Replace the real AnkiConnect with our mock

    importer.process_file()

    # Verify that add_note was called twice
    assert mock_anki_connect.add_note.call_count == 2

    # Inspect the first call
    first_call_args = mock_anki_connect.add_note.call_args_list[0][0][0]
    assert first_call_args['modelName'] == "MCQ Ultimate V2.1 shuffling default"
    assert first_call_args['fields']['Question'] == "What is the capital of France?"
    assert first_call_args['fields']['Correct'] == "Paris"
    assert first_call_args['fields']['Incorrect1'] == "Berlin"
    assert first_call_args['fields']['Incorrect2'] == "Madrid"
    assert first_call_args['fields']['Incorrect3'] == "Rome"
    assert "Paris is the capital" in first_call_args['fields']['Explanation']

    # Inspect the second call (note the blank incorrect option)
    second_call_args = mock_anki_connect.add_note.call_args_list[1][0][0]
    assert second_call_args['fields']['Question'] == "Which planet is known as the Red Planet?"
    assert second_call_args['fields']['Correct'] == "Mars"
    assert second_call_args['fields']['Incorrect1'] == "Earth"
    assert second_call_args['fields']['Incorrect2'] == "Jupiter"
    assert second_call_args['fields']['Incorrect3'] == "" # Check that padding works
