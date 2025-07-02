# Anki Markdown Importer

This script imports multiple-choice questions from a Markdown file into Anki, allowing you to use custom note types with shuffling options.

## Features

- Imports questions from a simple Markdown format.
- Highly configurable via a `config.yml` file.
- Automatically detects available Anki card models (note types).
- Lets you inspect the fields of any card model to configure the importer easily.
- Supports mapping to any custom note type, including those with shuffling options like "MCQ Ultimate V2.1 shuffling default".

## Prerequisites

1.  **Anki**: Make sure Anki is installed on your system.
2.  **AnkiConnect**: You need to install the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on in Anki. This allows the script to communicate with Anki.
3.  **Python**: You need Python 3 installed.
4.  **Python Libraries**: Install the required libraries by running:
    ```bash
    pip install requests markdown2 PyYAML
    ```

## How to Use

### 1. Prepare Your Questions

Create a Markdown file (e.g., `questions.md`) with your questions. Use the following format for each question:

```markdown
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
    4. Venus
    - Answer: 2, Mars is often called the Red Planet due to its reddish appearance.
```

**Important**: Each question must end with an `- Answer:` line, followed by the number of the correct option and an optional explanation.

### 2. Configure the Importer

Configuration is done through the `config.yml` file. This is where you tell the script which Anki deck to use, which card model (note type) to apply, and how to map your data to its fields.

**Step 2.1: Find Your Card Model**

First, make sure Anki is running. Then, run the following command in your terminal to see all the card models you have installed:

```bash
python main.py --list-models
```

This will output a list of names. Find the one you want to use (e.g., `MCQ Ultimate V2.1 shuffling default`) and copy it.

**Step 2.2: Find the Fields for Your Card Model**

Now, use the name you just copied to find out which fields the card model uses:

```bash
python main.py --list-fields "MCQ Ultimate V2.1 shuffling default"
```

This will show you the exact names of the fields, for example:
- Question
- Correct
- Incorrect1
- Incorrect2
- Incorrect3
- Explanation

**Step 2.3: Edit `config.yml`**

Open the `config.yml` file and fill it out using the information you just gathered.

- `deck_name`: The Anki deck you want to add cards to.
- `card_model`: The name of the card model you chose.
- `fields`: This is the most important part. You need to map the script's internal names (`question`, `correct_answer`, etc.) to the actual field names of your card model.
    - `question`: The field for the question text.
    - `correct_answer`: The field for the correct option.
    - `incorrect_answers`: A list of fields for the wrong options.
    - `explanation`: The field for the answer explanation.
- `questions_file`: The path to your Markdown file.

Here is an example `config.yml` for the "MCQ Ultimate V2.1 shuffling default" template:

```yaml
deck_name: My Deck
card_model: MCQ Ultimate V2.1 shuffling default
fields:
  question: Question
  correct_answer: Correct
  incorrect_answers:
    - Incorrect1
    - Incorrect2
    - Incorrect3
  explanation: Explanation
questions_file: questions.md
```

### 3. Run the Importer

Once your `config.yml` is set up and Anki is running, simply run the script:

```bash
python main.py
```

The script will read your Markdown file, connect to Anki, and create the new cards in the specified deck with the correct card model.
