import json

input_file = 'data/oxfess_data.json'
output_file = 'data/oxfess_data_text_only.json'

# Read the input JSON file
with open(input_file, 'r') as file:
    data = json.load(file)

# Extract postId and text
extracted_data = []
for item in data:
    extracted_data.append({
        'postId': item['postId'],
        'text': item['text']
    })

# Save the extracted data to a new JSON file
with open(output_file, 'w') as file:
    json.dump(extracted_data, file, indent=2)

print("Extraction complete. Data saved to file:", output_file)