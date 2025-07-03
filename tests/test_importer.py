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
    mock.add_note.return_value = None # Simulate successful note addition
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
def temp_config_file_no_explanation(tmp_path):
    """Fixture to create a temporary config file without an explanation field."""
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
            ]
        },
        "questions_file": "test_questions.md"
    }
    config_file = tmp_path / "config.yml"
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f)
    return str(config_file)

@pytest.fixture
def temp_config_file_basic_card(tmp_path):
    """Fixture to create a temporary config file for a basic card type."""
    config_data = {
        "deck_name": "TestDeck",
        "card_model": "Basic",
        "fields": {
            "question": "Front",
            "correct_answer": "Back",
            "incorrect_answers": []
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

@pytest.fixture
def temp_questions_file_empty(tmp_path):
    """Fixture for an empty questions markdown file."""
    questions_file = tmp_path / "empty_questions.md"
    with open(questions_file, 'w') as f:
        f.write("")
    return str(questions_file)

@pytest.fixture
def temp_questions_file_no_answer(tmp_path):
    """Fixture for questions markdown file with a question missing an answer line."""
    markdown_content = """
- What is the capital of France?
    1. Berlin
    2. Madrid
    3. Paris
    4. Rome

- Which planet is known as the Red Planet?
    1. Earth
    2. Mars
    3. Jupiter
    - Answer: 2, Mars is often called the Red Planet.
"""
    questions_file = tmp_path / "no_answer_questions.md"
    with open(questions_file, 'w') as f:
        f.write(markdown_content)
    return str(questions_file)

@pytest.fixture
def temp_questions_file_invalid_answer_index(tmp_path):
    """Fixture for questions markdown file with an invalid answer index."""
    markdown_content = """
- What is the capital of France?
    1. Berlin
    2. Madrid
    3. Paris
    4. Rome
    - Answer: 5, Paris is the capital of France.
"""
    questions_file = tmp_path / "invalid_index_questions.md"
    with open(questions_file, 'w') as f:
        f.write(markdown_content)
    return str(questions_file)


# --- Existing Tests ---

def test_extract_questions(temp_questions_file):
    """Test that questions are extracted correctly from the markdown file."""
    with open(temp_questions_file, 'r') as f:
        content = f.read()
    questions = AnkiMdImporter.extract_questions(content)
    assert len(questions) == 2
    assert questions[0][0].strip() == "What is the capital of France?"
    assert "Berlin" in questions[0][1] # Check if options are present
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


# --- New Tests ---

def test_importer_config_not_found():
    """Test that FileNotFoundError is raised if config file is not found."""
    with pytest.raises(FileNotFoundError, match="Configuration file not found: non_existent_config.yml"):
        AnkiMdImporter("non_existent_config.yml")

def test_importer_malformed_config(tmp_path):
    """Test that YAMLError is raised if config file is malformed."""
    malformed_config = tmp_path / "malformed_config.yml"
    malformed_config.write_text("deck_name: [-") # Invalid YAML
    with pytest.raises(yaml.YAMLError):
        AnkiMdImporter(str(malformed_config))

def test_importer_questions_file_not_found(mock_anki_connect, tmp_path):
    """Test that FileNotFoundError is raised if questions file is not found."""
    config_data = {
        "deck_name": "TestDeck",
        "card_model": "Basic",
        "fields": {"question": "Front", "correct_answer": "Back"},
        "questions_file": "non_existent_questions.md"
    }
    config_file = tmp_path / "config.yml"
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f)
    
    os.chdir(str(tmp_path)) # Change to temp dir so importer looks for file there
    importer = AnkiMdImporter(os.path.basename(config_file))
    importer.anki = mock_anki_connect

    with pytest.raises(FileNotFoundError, match="Questions file not found: non_existent_questions.md"):
        importer.process_file()

def test_extract_questions_empty_content():
    """Test that extracting questions from empty content returns an empty list."""
    questions = AnkiMdImporter.extract_questions("")
    assert len(questions) == 0

def test_extract_questions_no_answer_line(temp_questions_file_no_answer):
    """Test that questions without an answer line are not extracted."""
    with open(temp_questions_file_no_answer, 'r') as f:
        content = f.read()
    questions = AnkiMdImporter.extract_questions(content)
    # The regex should now only extract questions that have a complete answer line.
    # The first question in temp_questions_file_no_answer does NOT have a complete answer line.
    assert len(questions) == 1 
    assert questions[0][0].strip() == "Which planet is known as the Red Planet?"

def test_extract_questions_invalid_answer_index(mock_anki_connect, temp_config_file, temp_questions_file_invalid_answer_index, capsys):
    """Test that an invalid answer index prints a warning and skips the card."""
    os.chdir(os.path.dirname(temp_config_file))
    importer = AnkiMdImporter(os.path.basename(temp_config_file))
    importer.anki = mock_anki_connect
    importer.config['questions_file'] = os.path.basename(temp_questions_file_invalid_answer_index)

    importer.process_file()

    captured = capsys.readouterr()
    assert "Invalid correct answer index for question: What is the capital of France?" in captured.out
    mock_anki_connect.add_note.assert_not_called() # No card should be added

def test_list_models_connection_error(mocker, capsys):
    """Test that --list-models handles ConnectionError gracefully."""
    mocker.patch('main.AnkiConnect', side_effect=ConnectionError("Mock connection error"))
    
    # Mock argparse to simulate command line arguments
    mocker.patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(list_models=True, list_fields=None, config='config.yml'))
    
    from main import main # Re-import main to run the main function
    main()
    captured = capsys.readouterr()
    assert "Mock connection error" in captured.out # Removed "Error: " prefix

def test_list_fields_connection_error(mocker, capsys):
    """Test that --list-fields handles ConnectionError gracefully."""
    mocker.patch('main.AnkiConnect', side_effect=ConnectionError("Mock connection error"))
    
    # Mock argparse to simulate command line arguments
    mocker.patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(list_models=False, list_fields='Basic', config='config.yml'))
    
    from main import main # Re-import main to run the main function
    main()
    captured = capsys.readouterr()
    assert "Mock connection error" in captured.out # Removed "Error: " prefix

def test_add_note_connection_error(mock_anki_connect, temp_config_file, temp_questions_file, capsys):
    """Test that add_note errors are caught and reported."""
    mock_anki_connect.add_note.side_effect = Exception("AnkiConnect add_note failed")
    
    os.chdir(os.path.dirname(temp_config_file))
    importer = AnkiMdImporter(os.path.basename(temp_config_file))
    importer.anki = mock_anki_connect
    importer.config['questions_file'] = os.path.basename(temp_questions_file)

    importer.process_file()

    captured = capsys.readouterr()
    assert "Error adding card for question: What is the capital of France?. Error: AnkiConnect add_note failed" in captured.out
    assert "Error adding card for question: Which planet is known as the Red Planet?. Error: AnkiConnect add_note failed" in captured.out

def test_process_questions_no_explanation_field(mock_anki_connect, temp_config_file_no_explanation, temp_questions_file):
    """Test that cards are added correctly when no explanation field is specified."""
    os.chdir(os.path.dirname(temp_config_file_no_explanation))
    importer = AnkiMdImporter(os.path.basename(temp_config_file_no_explanation))
    importer.anki = mock_anki_connect
    importer.config['questions_file'] = os.path.basename(temp_questions_file)

    importer.process_file()

    mock_anki_connect.add_note.assert_called() # Ensure notes were attempted to be added
    first_call_args = mock_anki_connect.add_note.call_args_list[0][0][0]
    assert 'Explanation' not in first_call_args['fields'] # Ensure no explanation field was set

def test_process_questions_basic_card_type(mock_anki_connect, temp_config_file_basic_card, temp_questions_file):
    """Test that basic card types are formatted correctly."""
    os.chdir(os.path.dirname(temp_config_file_basic_card))
    importer = AnkiMdImporter(os.path.basename(temp_config_file_basic_card))
    importer.anki = mock_anki_connect
    importer.config['questions_file'] = os.path.basename(temp_questions_file)

    importer.process_file()

    mock_anki_connect.add_note.assert_called() # Ensure notes were attempted to be added
    first_call_args = mock_anki_connect.add_note.call_args_list[0][0][0]
    assert first_call_args['modelName'] == "Basic"
    assert "<p>What is the capital of France?</p><ol>" in first_call_args['fields']['Front']
    assert "<li>Berlin</li>" in first_call_args['fields']['Front']
    # Check for the combined content in the 'Back' field, allowing for markdown2's paragraph wrapping
    assert "<p>Paris</p>" in first_call_args['fields']['Back']
    assert "<p>Paris is the capital of France.</p>" in first_call_args['fields']['Back']