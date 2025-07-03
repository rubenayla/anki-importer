import markdown2
import requests
import os
import re
import yaml
import argparse

class AnkiConnect:
    def __init__(self, url="http://localhost:8765"):
        self.url = url

    def _invoke(self, action, **params):
        payload = {"action": action, "version": 6, "params": params}
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            result = response.json()
            if result.get('error') is not None:
                raise Exception(result['error'])
            return result.get('result')
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Could not connect to AnkiConnect at {self.url}. Please ensure Anki is running and AnkiConnect is installed.") from e

    def get_model_names(self):
        return self._invoke('modelNames')

    def get_model_field_names(self, model_name):
        return self._invoke('modelFieldNames', modelName=model_name)

    def add_note(self, note):
        return self._invoke('addNote', note=note)

class AnkiMdImporter:
    def __init__(self, config_path='config.yml'):
        self.config = self._load_config(config_path)
        self.anki = AnkiConnect()

    def _load_config(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def extract_questions(markdown_content):
        # Refined regex to capture full question blocks more reliably.
        # It explicitly looks for a question line, followed by options, and then the mandatory answer line.
        # Using [^\n]* instead of .*? with re.DOTALL to avoid greedy matching issues across lines.
        pattern = re.compile(
            r'^(?:- |\d+\.\s)([^\n]*)\n'  # Question line (group 1) - matches until newline
            r'((?:^\s*\d+\.\s[^\n]*\n)+?)'     # Options (non-greedy, group 2) - matches lines starting with spaces and numbers
            r'^\s*- Answer: ([^\n]*)(?:$|\n)', # Answer line (group 3) - matches the answer line
            re.MULTILINE
        )
        return pattern.findall(markdown_content)

    def process_file(self):
        questions_file = self.config['questions_file']
        if not os.path.exists(questions_file):
            raise FileNotFoundError(f"Questions file not found: {questions_file}")
        
        with open(questions_file, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        
        questions = AnkiMdImporter.extract_questions(markdown_content)
        self.process_questions(questions)

    def process_questions(self, questions):
        field_map = self.config['fields']
        is_basic_card = not field_map.get('incorrect_answers')

        for question_text, options_str, answer_text in questions:
            options = re.findall(r'\d+\.\s(.*?)(?:\n|$)', options_str)
            answer_match = re.match(r'\s*(\d+),?\s*(.*)', answer_text.strip())

            if not answer_match:
                print(f"Could not parse answer for question: {question_text.strip()}")
                continue

            correct_index = int(answer_match.group(1)) - 1
            explanation = answer_match.group(2).strip()

            if not (0 <= correct_index < len(options)):
                print(f"Invalid correct answer index for question: {question_text.strip()}")
                continue

            correct_option = options[correct_index]
            
            fields = {}
            if is_basic_card:
                front_html = f"<p>{question_text.strip()}</p><ol>"
                for option in options:
                    front_html += f"<li>{option.strip()}</li>"
                front_html += "</ol>"
                
                # For basic cards, combine correct answer and explanation in the back field
                # markdown2.markdown will convert this to HTML, typically wrapping in <p> tags
                back_html = markdown2.markdown(f"{correct_option.strip()}\n\n{explanation}")
                
                fields[field_map['question']] = front_html
                fields[field_map['correct_answer']] = back_html
            else:
                incorrect_options = [opt for i, opt in enumerate(options) if i != correct_index]
                fields[field_map['question']] = question_text.strip()
                fields[field_map['correct_answer']] = correct_option.strip()
                
                if field_map.get('explanation'):
                    fields[field_map['explanation']] = markdown2.markdown(explanation)

                incorrect_fields = field_map.get('incorrect_answers', [])
                for i, field_name in enumerate(incorrect_fields):
                    if i < len(incorrect_options):
                        fields[field_name] = incorrect_options[i].strip()
                    else:
                        fields[field_name] = ""

            note = {
                "deckName": self.config['deck_name'],
                "modelName": self.config['card_model'],
                "fields": fields,
                "tags": self.config.get('tags', [])
            }

            try:
                self.anki.add_note(note)
                print(f"Card added for question: {question_text.strip()}")
            except Exception as e:
                print(f"Error adding card for question: {question_text.strip()}. Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Import questions from a Markdown file to Anki.")
    parser.add_argument('--list-models', action='store_true', help='List available Anki note types (card models).')
    parser.add_argument('--list-fields', metavar='MODEL_NAME', help='List fields for a specific Anki note type.')
    parser.add_argument('--config', default='config.yml', help='Path to the configuration file.')

    args = parser.parse_args()

    if args.list_models:
        try:
            anki = AnkiConnect()
            models = anki.get_model_names()
            print(f"Available Anki Card Models:")
            for model in models:
                print(f"- {model}")
        except ConnectionError as e:
            print(f"{e}") # Print only the error message, not the "Error: " prefix
        return

    if args.list_fields:
        try:
            anki = AnkiConnect()
            fields = anki.get_model_field_names(args.list_fields)
            print(f"Fields for model '{args.list_fields}':")
            for field in fields:
                print(f"- {field}")
        except ConnectionError as e:
            print(f"{e}") # Print only the error message, not the "Error: " prefix
        except Exception as e:
            print(f"Error: {e}")
        return

    try:
        importer = AnkiMdImporter(args.config)
        importer.process_file()
    except (FileNotFoundError, ConnectionError, Exception) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()