# AnkiMdImporter

## Overview
The `AnkiMdImporter` is a Python script designed to automatically import questions formatted in Markdown into Anki, a popular flashcard application used for spaced repetition learning. This script parses a Markdown file containing questions and their respective options, converts these questions into Anki cards, and adds them to a specified deck.

## Steps to use
1. Install the [requirements](#requirements)
2. Figure out your source of information. Maybe it's a PDF, some text notes, maybe it's common knowledge to the AI so you don't need anything, maybe it's so incredibly long to the AI that you have to split it in pieces... it depends. Once you have it, save the text in a file called `questions.md` in the same directory as the script.
3. Then make sure your deck is created, has 1 card already (dummy or anything), and the variable `deck_name` matches with the name of the deck, at the end of the script.
4. Run the script and wait for the cards to be imported into Anki. You should be able to see them appear one by one.

## Requirements
- Python 3.x
- `markdown2` library
- `requests` library
- Anki installed with [AnkiConnect](https://ankiweb.net/shared/info/2055492159) plugin enabled (listening on port 8765 by default)
    - Code: ``2055492159``
- Make sure the deck is created, it has at least 1 card already, and the variable ``deck_name`` matches with the name of the deck, at the end of the script

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

### Prompt to generate the questions
```text
Create multiple-choice test questions with 4 possible answers for me to practice on the attached document. Try to make them difficult, aiming to be tricky like a university exam. After the questions, include explanations with their answers. You can start with 10 questions.

Follow this format:
- Is this thing correct or the other, etc.?:
    1. blablabla
    2. blablabla
    3. blablabla
    4. blablabla
    - Answer: Correct answer 1, because blablabla
- Next question...
```
In spanish:
```text
Hazme preguntas tipo test con 4 respuestas posibles, para practicar sobre el documento adjunto (en un codeblock, de ahora en adelante todo así). Intenta que sean dificiles, intenta ir a pillar, como en un examen de universidad. Tras las preguntas, pon las explicaciones con sus respuestas. Puedes empezar con 10 preguntas.

Sigue el siguiente formato (en codeblock):
- Tal cosa es correcta o la otra etc?:
    1. blablabla
    2. blablabla
    3. blablabla
    4. blablabla
    - Answer: Respuesta correcta 1, porque blablabla
- Siguiente pregunta...
```
