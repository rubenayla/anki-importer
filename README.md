# Anki Markdown Importer

This script imports multiple-choice questions from a Markdown file into Anki, allowing you to use custom note types with shuffling options.

## Features

- Imports questions from a simple Markdown format.
- Highly configurable via `config.yml` files.
- Automatically detects available Anki card models (note types).
- Lets you inspect the fields of any card model to configure the importer easily.
- Supports mapping to any custom note type, including those with shuffling options like "MCQ Ultimate V2.1 shuffling default".

## Prerequisites

1.  **[Anki](https://apps.ankiweb.net/)**: Make sure Anki is installed on your system.
2.  **[AnkiConnect](https://ankiweb.net/shared/info/2055492159)**: You need to install the AnkiConnect add-on in Anki. This allows the script to communicate with Anki.
3.  **[Python](https://www.python.org/downloads/)**: You need Python 3 installed.

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

**How the Markdown is interpreted for Anki Cards:**

This Markdown format is specifically designed for multiple-choice questions. Here's how the script interprets each part to populate your Anki card fields:

*   The line starting with `-` or `N.` (e.g., `- What is...` or `1. What is...`) is extracted as the **Question** text.
*   The numbered lines (e.g., `1. Berlin`, `2. Madrid`) are treated as the **Options**.
*   The `- Answer: N, [Explanation]` line is crucial:
    *   `N` (the number) indicates the **correct option** among the numbered lines.
    *   `[Explanation]` (the text after the comma) is the **Explanation** for the answer.

This information is then mapped to the fields of your chosen Anki card model, as configured in your selected `config.yml`.

**Note on Basic Card Types:** If you configure a basic card model (e.g., 'Basic') in your `config.yml` (by setting `card_model: Basic` and `incorrect_answers: []`), the script will automatically combine the question and options into the 'Front' field, and the correct answer along with the explanation into the 'Back' field.

### 2. Installation

Choose your preferred method to install the project dependencies:

#### Automated Installation (Recommended)

To get started quickly, simply run the appropriate installation script for your operating system. This will install Poetry (if you don't have it) and all project dependencies.

**Linux / macOS:**

```bash
bash install.sh
```

**Windows (PowerShell):**

```powershell
.\install.ps1
```

#### Manual Installation

If you prefer to install dependencies manually, follow these steps:

1.  **Install Poetry**: If you don't have Poetry installed, follow the official instructions:
    *   **Linux / macOS / Windows (WSL):**
        ```bash
        curl -sSL https://install.python-poetry.org | python3 -
        ```
    *   **Windows (PowerShell):**
        ```powershell
        (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
        ```
    *   For other installation methods or troubleshooting, refer to the [Poetry documentation](https://python-poetry.org/docs/#installation).

2.  **Install Project Dependencies**: Navigate to the project root directory in your terminal and run:
    ```bash
    poetry install
    ```

### 3. Configure the Importer

Configuration is done through YAML files. The project provides a default `config.yml` for basic cards and a `configs/` directory with presets for more complex card types.

**Default Configuration (for Basic Anki Cards):**

The `config.yml` file in the root directory is pre-configured to import questions as basic Anki cards (Front/Back). If you intend to use basic cards, you can proceed directly to [Step 4. Run the Importer](#4-run-the-importer) after preparing your questions and installing the dependencies. No changes to `config.yml` are needed.

**Using Presets or Custom Configurations:**

If you want to use a custom multiple-choice Anki card model (like "MCQ Ultimate V2.1 shuffling default") or any other specific setup, you can use one of the provided presets or create your own. Presets are located in the `configs/` directory.

**Step 3.1: Find Your Card Model (if using a custom model)**

First, make sure Anki is running. Then, run the following command in your terminal to see all the card models you have installed:

```bash
poetry run python main.py --list-models
```

This will output a list of names. Find the one you want to use (e.g., `MCQ Ultimate V2.1 shuffling default`) and copy it.

**Step 3.2: Find the Fields for Your Card Model (if using a custom model)**

Now, use the name you just copied to find out which fields the card model uses:

```bash
bash poetry run python main.py --list-fields "MCQ Ultimate V2.1 shuffling default"
```

This will show you the exact names of the fields, for example:
- Question
- Correct
- Incorrect1
- Incorrect2
- Incorrect3
- Explanation

**Step 3.3: Select or Edit Your Configuration File**

*   **To use a preset:** Choose a file from the `configs/` directory (e.g., `configs/mcq_ultimate_v2.yml`). You can use it directly or copy it to your project root and modify it.
*   **To create a custom configuration:** You can start by copying an existing preset or the default `config.yml` and modifying it to suit your needs.

Your configuration file (whether `config.yml` or a preset) will define the `card_model`, `fields` mapping, and `questions_file`.

Here is an example `configs/mcq_ultimate_v2.yml` for the "MCQ Ultimate V2.1 shuffling default" template:

```yaml
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

### 4. Run the Importer

Once your configuration file is ready and Anki is running, run the script. You can specify the configuration file and the target Anki deck:

```bash
poetry run python main.py --config config.yml --deck-name "My Custom Deck"
```

*   Use `--config config.yml` to use the default configuration, or `--config configs/your_preset.yml` to use a preset.
*   Use `--deck-name "Your Anki Deck"` to specify the target deck. If omitted, cards will be added to the "Default" deck in Anki.

The script will read your Markdown file, connect to Anki, and create the new cards in the specified deck with the correct card model.
