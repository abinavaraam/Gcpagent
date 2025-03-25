import csv
import nltk
import spacy
from nltk.corpus import stopwords
import json

# Download necessary NLTK data (if you haven't already)
try:
    stopwords.words('english')
    except LookupError:
        nltk.download('stopwords')

        try:
            spacy.load("en_core_web_sm")
            except OSError:
                spacy.cli.download("en_core_web_sm")

                nlp = spacy.load("en_core_web_sm")
                stop_words = set(stopwords.words('english'))

                def extract_keywords(question):
                    """Extracts keywords from a question by removing stop words and punctuation."""
                        words = nltk.word_tokenize(question.lower())
                            keywords = [word for word in words if word.isalnum() and word not in stop_words]
                                return keywords

                                def identify_question_type(question):
                                    """Identifies a basic question type based on the starting word."""
                                        question = question.lower().strip()
                                            if question.startswith("what"):
                                                    return "what"
                                                        elif question.startswith("when"):
                                                                return "when"
                                                                    elif question.startswith("where"):
                                                                            return "where"
                                                                                elif question.startswith("how"):
                                                                                        return "how"
                                                                                            elif question.startswith("is") or question.startswith("are") or question.startswith("do") or question.startswith("can"):
                                                                                                    return "is_are_do_can"
                                                                                                        else:
                                                                                                                return "other"

                                                                                                                def check_availability(answer):
                                                                                                                    """Checks if the answer suggests availability (basic check)."""
                                                                                                                        answer = answer.lower()
                                                                                                                            availability_keywords = ["available", "in stock", "can be purchased", "yes", "we have"]
                                                                                                                                unavailability_keywords = ["not available", "out of stock", "sold out", "no"]
                                                                                                                                    if any(keyword in answer for keyword in availability_keywords) and not any(keyword in answer for keyword in unavailability_keywords):
                                                                                                                                            return True
                                                                                                                                                elif any(keyword in answer for keyword in unavailability_keywords):
                                                                                                                                                        return False
                                                                                                                                                            return None  # Could not determine

                                                                                                                                                            def extract_entities(question):
                                                                                                                                                                """Extracts named entities from the question using spaCy."""
                                                                                                                                                                    doc = nlp(question)
                                                                                                                                                                        entities = [ent.text for ent in doc.ents]
                                                                                                                                                                            return entities

                                                                                                                                                                            def generate_metadata(question, answer):
                                                                                                                                                                                """Generates metadata for a given question and answer."""
                                                                                                                                                                                    metadata = {
                                                                                                                                                                                            "original_question": question,
                                                                                                                                                                                                    "intent": "unknown",  # You might need more sophisticated logic for intent
                                                                                                                                                                                                            "entities": extract_entities(question),
                                                                                                                                                                                                                    "question_type": identify_question_type(question),
                                                                                                                                                                                                                            "keywords": extract_keywords(question),
                                                                                                                                                                                                                                    "answer_type": "unknown",  # You might need logic to determine answer type
                                                                                                                                                                                                                                            "is_available": check_availability(answer)
                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                    return metadata

                                                                                                                                                                                                                                                    def process_csv(csv_filepath, output_filepath):
                                                                                                                                                                                                                                                        """Reads a CSV file, generates metadata for each row, and saves it to a JSONL file."""
                                                                                                                                                                                                                                                            data_with_metadata =
                                                                                                                                                                                                                                                                with open(csv_filepath, 'r', encoding='utf-8') as csvfile:
                                                                                                                                                                                                                                                                        reader = csv.DictReader(csvfile)
                                                                                                                                                                                                                                                                                for row in reader:
                                                                                                                                                                                                                                                                                            question = row.get("Question")
                                                                                                                                                                                                                                                                                                        answer = row.get("Answer")
                                                                                                                                                                                                                                                                                                                    if question and answer:
                                                                                                                                                                                                                                                                                                                                    metadata = generate_metadata(question, answer)
                                                                                                                                                                                                                                                                                                                                                    data_with_metadata.append({
                                                                                                                                                                                                                                                                                                                                                                        "content": answer,  # Using the answer as the content for the data store
                                                                                                                                                                                                                                                                                                                                                                                            "metadata": metadata
                                                                                                                                                                                                                                                                                                                                                                                                            })

                                                                                                                                                                                                                                                                                                                                                                                                                with open(output_filepath, 'w', encoding='utf-8') as outfile:
                                                                                                                                                                                                                                                                                                                                                                                                                        for item in data_with_metadata:
                                                                                                                                                                                                                                                                                                                                                                                                                                    json.dump(item, outfile)
                                                                                                                                                                                                                                                                                                                                                                                                                                                outfile.write('\n')

                                                                                                                                                                                                                                                                                                                                                                                                                                                if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                                                                                                                                                                    csv_file = "your_qa_data.csv"  # Replace with the path to your CSV file
                                                                                                                                                                                                                                                                                                                                                                                                                                                        output_jsonl_file = "qa_data_with_metadata.jsonl"
                                                                                                                                                                                                                                                                                                                                                                                                                                                            process_csv(csv_file, output_jsonl_file)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                print(f"Processed '{csv_file}' and saved data with metadata to '{output_jsonl_file}'")