# TODO think of way to make this generate less boring words
import json

from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

university = "cambridge"
undergrad_colleges_only = True

# Import model
print("Starting to load wiki_word_embedding_model")
model_filepath = './itsgiving/wordinput/static/wordinput/data/wiki-news-300d-1M.vec'
wiki_word_embedding_model = KeyedVectors.load_word2vec_format(model_filepath, binary=False, limit=200000)
print("Finished loading wiki_word_embedding_model")

# Load college vectors from relevant file
print("Loading college vectors...")
averaging_algorithm = "tfid"
college_vectors_filepath = (f'./data/{university}_undergrad_only_{undergrad_colleges_only}_college_vectors_{averaging_algorithm}.json')
with open(college_vectors_filepath, 'r') as f:
    college_vectors = json.load(f)


# Convert loaded vectors back to numpy arrays
college_vectors = {college: np.array(vector) for college, vector in college_vectors.items()}
print("College vectors loaded and processed.")

print(f"Number of colleges loaded: {len(college_vectors)}")
print(f"Shape of first college vector: {next(iter(college_vectors.values())).shape}")

print("Finding closest words to each college...")
college_closest_words = {
    college: wiki_word_embedding_model.similar_by_vector(vector, topn=3)
    for college, vector in college_vectors.items()
}
print("Closest words found.")

# Print all out
for college, closest_words in college_closest_words.items():
    print(f"Closest words to {college}: {closest_words}")