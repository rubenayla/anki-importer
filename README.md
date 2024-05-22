# AnkiMdImporter

## Overview
The `AnkiMdImporter` is a Python script designed to automatically import questions formatted in Markdown into Anki, a popular flashcard application used for spaced repetition learning. This script parses a Markdown file containing questions and their respective options, converts these questions into Anki cards, and adds them to a specified deck.

## Requirements
- Python 3.x
- `markdown2` library
- `requests` library
- Anki installed with [AnkiConnect](https://ankiweb.net/shared/info/2055492159) plugin enabled (listening on port 8765)
    - Code: ``2055492159``
- Make sure the deck is created, it has at least 1 card already, and the name of the deck matches with the variable ``deck_name``, at the end of the script

### Questions File Format
The `AnkiCardImporter` script requires that the questions are present in a file called `questions.md`, formatted as follows:
```text
- What is the capital of France?:
    1. Berlin
    2. Madrid
    3. Paris
    4. Rome
    - Answer: 3, because Paris is the capital of France.
```

Note this:
- Question text should start with a dash
- Each option should begin with a number followed by a period
- The correct answer explanation should start with a dash, followed by the word "Answer:", and the explanation should explain why the answer is correct, in the same line (only one)

## Installation

### Set up Python Environment
1. Ensure Python 3 is installed on your system.
2. Install the required Python libraries:
   ```bash
   pip install markdown2 requests
