- What is the primary function of the `AnkiCardImporter` script?
    1. To convert PDF files into Anki cards
    2. To automate the import of Markdown-formatted questions into Anki decks
    3. To generate Markdown files from Anki decks
    4. To synchronize Anki decks across multiple devices
    - Answer: 2, because the script is designed to parse Markdown files containing questions and options, then automatically add these as cards into a specified Anki deck.

- Which Python library is used by `AnkiCardImporter` to convert Markdown text into HTML?
    1. BeautifulSoup
    2. Pandas
    3. markdown2
    4. NumPy
    - Answer: 3, because `markdown2` is the library used by the script to handle the conversion of Markdown syntax into HTML format.

- Before running the `AnkiCardImporter` script, what plugin must be installed and active in Anki?
    1. AnkiWeb
    2. AnkiConnect
    3. AnkiFlash
    4. AnkiOverdrive
    - Answer: 2, because AnkiConnect is the required plugin that allows external applications like this script to communicate with Anki via a local network.

- What should be ensured about the Anki application before running the `AnkiCardImporter` script?
    1. Anki must be installed but not running.
    2. Anki must be running and the AnkiConnect plugin active.
    3. Anki must be uninstalled and reinstalled.
    4. Anki must be upgraded to the latest version only.
    - Answer: 2, because for the script to function, Anki needs to be running with the AnkiConnect plugin enabled to facilitate the addition of cards.

- How can a user specify the deck into which the Anki cards should be added?
    1. By editing the `deck_name` variable in the script.
    2. By sending an email to the Anki support team.
    3. By renaming the Markdown file.
    4. By modifying the AnkiConnect plugin settings.
    - Answer: 1, because the `deck_name` variable in the `AnkiCardImporter` script is used to define the name of the Anki deck where the cards will be added.
