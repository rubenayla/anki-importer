# AnkiMdImporter

## Overview
The `AnkiMdImporter` is a Python script designed to automatically import questions formatted in Markdown into Anki, a popular flashcard application used for spaced repetition learning. This script parses a Markdown file containing questions and their respective options, converts these questions into Anki cards, and adds them to a specified deck.

## Features
- **Markdown Parsing**: Converts questions written in Markdown format to HTML.
- **Deck Customization**: Allows users to specify the deck name where the cards will be added.
- **Flexible Card Models**: Supports basic Anki card models with customizable front and back formats.

## Requirements
- Python 3.x
- `markdown2` library
- `requests` library
- Anki installed with AnkiConnect plugin enabled (listening on port 8765)

## Installation

### Set up Python Environment
1. Ensure Python 3 is installed on your system.
2. Install the required Python libraries:
   ```bash
   pip install markdown2 requests
