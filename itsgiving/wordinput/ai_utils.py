from gensim.models import KeyedVectors
import json
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.staticfiles import finders
from .model_loader import wiki_word_embedding_model  # Import the pre-loaded model



def get_closest_colleges_and_image_paths(word, university="cambridge", undergrad_colleges_only=True):

    # Load college vectors from relevant file
    # TODO see if finders is best use in production
    averaging_algorithm = "tfid"
    college_vectors_filepath = finders.find(f'wordinput/data/{university}_undergrad_only_{undergrad_colleges_only}_college_vectors_{averaging_algorithm}.json')
    with open(college_vectors_filepath, 'r') as f:
        college_vectors = json.load(f)

        
    # Access pre-loaded model from memory
    model = wiki_word_embedding_model
    if model is None:
        raise ValueError("Word embedding model is not loaded")
    if word not in model:
        return None
    
    # Get word as a vector
    word_vector = model[word]
    
    # Calculate similarities
    similarities = {name: cosine_similarity([word_vector], [vec])[0][0] 
                    for name, vec in college_vectors.items() if vec is not None}
    
    # Sort similarities in descending order
    sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    # Get top 3 most similar colleges with similarity scores
    top_3_colleges_and_scores = [(college, score) for college, score in sorted_similarities[:3]]

    print(top_3_colleges_and_scores)

    # Get college names, image paths and scores for output
    college_1, college_image_path_1, college_score_1 = top_3_colleges_and_scores[0][0], f'wordinput/images/{university}_{top_3_colleges_and_scores[0][0]}.svg' if university == "oxford" else f'wordinput/images/{university}_{top_3_colleges_and_scores[0][0]}.png', top_3_colleges_and_scores[0][1]
    college_2, college_image_path_2, college_score_2 = top_3_colleges_and_scores[1][0], f'wordinput/images/{university}_{top_3_colleges_and_scores[1][0]}.svg' if university == "oxford" else f'wordinput/images/{university}_{top_3_colleges_and_scores[1][0]}.png', top_3_colleges_and_scores[1][1]
    college_3, college_image_path_3, college_score_3 = top_3_colleges_and_scores[2][0], f'wordinput/images/{university}_{top_3_colleges_and_scores[2][0]}.svg' if university == "oxford" else f'wordinput/images/{university}_{top_3_colleges_and_scores[2][0]}.png', top_3_colleges_and_scores[2][1]

    return college_1, college_image_path_1, college_score_1, college_2, college_image_path_2, college_score_2, college_3, college_image_path_3, college_score_3