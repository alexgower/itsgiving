import anthropic
import json
import os
import time
import random

input_filename = 'data/camfess_data_text_only.json'
output_filename = 'data/camfess_by_colleges_anthropic.json'

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key='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')

# Comprehensive list of Cambridge colleges
cambridge_colleges = [
    "Christ's", "Churchill", "Clare", "Clare Hall", "Corpus Christi",
    "Darwin", "Downing", "Emmanuel", "Fitzwilliam", "Girton",
    "Gonville and Caius", "Homerton", "Hughes Hall", "Jesus", "King's",
    "Lucy Cavendish", "Magdalene", "Murray Edwards", "Newnham", "Pembroke",
    "Peterhouse", "Queens'", "Robinson", "Selwyn", "Sidney Sussex",
    "St Catharine's", "St Edmund's", "St John's", "Trinity", "Trinity Hall", "Wolfson", "None"
]


def process_text_block(text_block, max_retries=5):
    system_prompt = f"""
    You are an AI assistant specialized in extracting information about Cambridge colleges from text. 
    Given a text block, create a JSON where each key is a college name and the value is the associated text for that college. 
    The JSON should only have college names and 'associated_text' as the fields and nothing else. 

    Here's the list of Cambridge colleges to consider:
    {', '.join(cambridge_colleges)}

    Only include colleges from this list in your JSON output. If a college from this list is not mentioned in the text block, do not include it in the JSON output. 
    
    When matching college names, please be flexible with capitalization, common abbreviations, and minor typos.

    Also, if text is not associated with any college in this list, please include it under the key 'None'.

    Extra notes: 
    - 'sidge' is not a college
    
    Provide only the JSON output, with no additional explanation.
    """

    user_prompt = f"Here's the text block to process:\n\n{text_block}"

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Extract the JSON from the response
            response_content = response.content[0].text
            json_start = response_content.index('{')
            json_end = response_content.rindex('}') + 1
            json_str = response_content[json_start:json_end]

            # Parse the JSON string into a Python dictionary
            return json.loads(json_str)

        except Exception as e:
            print(f"An error occurred: {e}")
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.random()
                print(f"Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts.")
                raise

def append_to_json_file(file_path, data):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r+') as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, indent=2)
            file.truncate()
    else:
        with open(file_path, 'w') as file:
            json.dump([data], file, indent=2)

# Read the input JSON file
with open(input_filename, 'r') as file:
    input_data = json.load(file)

# Process each item in the input data
for item_index, item in enumerate(input_data):
    post_id = item['postId']
    text = item['text']
    
    print("")
    print(f"Processing item {item_index + 1} of {len(input_data)}")
    print(f"Processing post ID: {post_id}")
    print("Text:", text)
    
    try:
        result = process_text_block(text)
        
        output_item = {
            "postId": post_id,
            "colleges": result
        }

        print("")
        print("Result:", result)
        
        # Append the processed item to the output file
        append_to_json_file(output_filename, output_item)
        
        print(f"Successfully processed and saved item {item_index + 1}")
    except Exception as e:
        print(f"Failed to process item {item_index + 1}: {e}")
    
    # Add a small delay between requests to help avoid rate limiting
    # time.sleep(1.2)  # This ensures we don't exceed 50 requests per minute

print(f"Processed all items. Results saved to {output_filename}")