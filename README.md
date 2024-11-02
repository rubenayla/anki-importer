# AnkiMdImporter

## Overview
The `AnkiMdImporter` is a Python script designed to automatically import questions formatted in Markdown into Anki, a popular flashcard application used for spaced repetition learning. This script parses a Markdown file containing questions and their respective options, converts these questions into Anki cards, and adds them to a specified deck.

## Steps to use
1. Install [Anki](https://apps.ankiweb.net/)
2. In Anki, install the plugin [AnkiConnect](https://ankiweb.net/shared/info/2055492159)
    - To do this you can go to Tools -> Add-ons -> Get Add-ons, and paste the code ``2055492159`` in the box
3. Restart the Anki program so the plugin is loaded (It's listening on port 8765 by default. That's how the script communicates with Anki)
4. Create your deck, and put at least 1 card already
5. Install [Python 3.x](https://www.python.org/downloads/) (any version of Python3 should work)
6. Python usually comes with pip, but in case you have problems you can install pip with:
    - `python -m ensurepip --upgrade`
7. Then install the pip packages `markdown2` and `requests` with:
    - `pip install markdown2 requests`
    - If you have problems, you can use conda, uv, or virtual environments
8. Clone the GitHub repository, or just download `main.py`, or copy the contents of `main.py` into a new text file, and name it `main.py` (anything with the `.py` extension)
9. Modify the `deck_name` variable at the end of the script to match the name of the deck you created in Anki
    - It's probably a good idea to use a simple name without spaces or strange characters
10. Figure out your source of information. Maybe it's a PDF, some text notes, maybe it's common knowledge to the AI so you don't need anything, maybe it's so incredibly long to the AI that you have to split it in pieces... it depends. Once you have it, save the text in a file called `questions.md` (for example) in the same directory as the script.
11. Modify the `file_path` variable at the end of the script to match the file with questions. If the Python script (`main.py`) and the file with questions (`questions.md`) are in the same folder, you can just put the name of the file, INCLUDING the extension (`"questions.md"`).
12. Run the script and wait for the cards to be imported into Anki. You should be able to see them appear one by one.

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


## Prompt to generate the questions
```text
Create multiple-choice test questions with 4 possible answers for me to practice on the attached document. Try to make them difficult, aiming to be tricky like a university exam. After the questions, include explanations with their answers. You can start with 40 questions.

Follow this format, EXACTLY, with the dash to indicate the start of the question, no numbers indicating the different questions. Put everything in a codeblock:
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
