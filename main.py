import markdown2
import requests
import os
import re

class AnkiMdImporter:
    def __init__(self, file_path, deck_name="Default", card_model="Basic"):
        self.file_path = file_path
        self.deck_name = deck_name
        self.card_model = card_model
        self.url = "http://localhost:8765"

    def markdown_to_html(self, markdown_text):
        return markdown2.markdown(markdown_text)

    def add_card(self, front, back):
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": self.deck_name,
                    "modelName": self.card_model,
                    "fields": {
                        "Front": front,
                        "Back": back
                    },
                    "tags": []
                }
            }
        }
        response = requests.post(self.url, json=payload)
        return response.json()

    def extract_questions(self, markdown_content):
        """
        Returns a list of tuples containing the question, options and answer.
        
        Args:
            markdown_content (str): The markdown content containing the questions.
        
        Returns:
            list[tuple(str, str, str)]: A list of tuples containing the question, options and answer.
        """
        pattern = re.compile(r'(?<=\n)(?:- |\d+\.\s)([\s\S]*?)$\s*((?:\d+\.\s.*?$\s*)+)- Answer: (.*?)$', re.DOTALL | re.MULTILINE)
        return pattern.findall(markdown_content)

    def process_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        questions = self.extract_questions(markdown_content)
        self.process_questions(questions)

    def process_questions(self, questions):
        for question, options_str, answer in questions:
            options = re.findall(r'\d+\.\s(.*?$)', options_str, re.MULTILINE)

            # Create HTML for the front with the question and options as a list
            front_html = f"<p>{question.strip()}</p><ol>"
            for option in options:
                front_html += f"<li>{option.strip()}</li>"
            front_html += "</ol>"
            
            # Convert the explanation to HTML
            back_html = self.markdown_to_html("Answer: " + answer.strip())
            
            # Add the card to Anki
            self.add_card(front_html, back_html)

if __name__ == "__main__":
    # Set folder to parent of file and define the deck name
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    file_path = 'questions.md'
    deck_name = 'ALA_FIJA' # Specify your Anki deck name

    importer = AnkiMdImporter(file_path, deck_name)
    importer.process_file()
