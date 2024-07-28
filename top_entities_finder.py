import json
import spacy
from collections import Counter

file_path = 'data/oxfess_data_text_only.json'  # Replace with your actual file path

# Load the English language model for spaCy
# "en_core_web_md" - Medium-sized English model * "en_core_web_lg" - Large English model * "en_core_web_trf" - Transformer-based English model
nlp = spacy.load("en_core_web_sm")
# nlp = spacy.load("en_core_web_trf")
nlp.max_length = 5355908

def extract_text_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Assuming the JSON is a list of dictionaries 
    return " ".join([item['text'] for item in data])

def perform_ner(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    return entities

def get_top_entities(entities, n=100):
    entity_counts = Counter(entities)
    return entity_counts.most_common(n)

# Main execution
combined_text = extract_text_from_json(file_path)
entities = perform_ner(combined_text)
top_100_entities = get_top_entities(entities)

# Print results
for entity, count in top_100_entities:
    print(f"{entity}: {count}")