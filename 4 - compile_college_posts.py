import json
from collections import defaultdict

# TODO repeat this once openai extraction is complete
input_filename = 'data/camfess_by_colleges_openai.json'
output_filename = 'data/camfess_data_college_compilation.json'

# Read the input JSON file
with open(input_filename, 'r') as f:
    data = json.load(f)

# Create a defaultdict to store posts by college
# (defaultdict automatically initializes new keys with an empty list)
college_posts = defaultdict(list)

# Process each post
for post in data:
    post_id = post['postId']
    colleges = post['colleges']
    
    # Add the post to each mentioned college, ignoring 'None'
    # Also remove any colons from strings in text
    for college, text in colleges.items():
        if college != 'None':
            college_posts[college].append({
                'postId': post_id,
                'text': text.replace(':', '')
            })

# Convert defaultdict to regular dict for JSON serialization
output_data = dict(college_posts)

# Write the output JSON file
with open(output_filename, 'w') as f:
    json.dump(output_data, f, indent=2)

print("Output JSON file has been created successfully.")