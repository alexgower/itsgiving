import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.linalg import svd


### FIND CLOSEST COLLEGE FUNCTIONS
def find_closest_college(word, college_vectors, model):
    
    if word not in model:
        return "Word not found in the model"
    
    # Get word vector
    word_vector = model[word]
    
    # Calculate similarities
    similarities = {name: cosine_similarity([word_vector], [vec])[0][0] 
                    for name, vec in college_vectors.items() if vec is not None}
    
    # Sort similarities in descending order
    sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)


    # Get top 3 most similar colleges with similarity scores
    top_3_colleges_and_scores = [(college, score) for college, score in sorted_similarities[:3]]

    return top_3_colleges_and_scores




### CREATE COLLEGE VECTOR FUNCTIONS

# Uses simple mean over word vectors
def create_college_vector_avg(text, model):

    words = text.lower().split()
    word_vectors = [model[word] for word in words if word in model]
    if not word_vectors:
        return None

    # Calculate average word vector
    avg_vector = np.mean(word_vectors, axis=0)
        
    # Combine average word vector with sentiment vector
    return avg_vector


# Uses tfidf to weight word vectors by importance
def create_college_vector_tfid(text, model, college_texts):
    tfidf = TfidfVectorizer()
    tfidf.fit(college_texts.values())  # Fit on all texts

    words = text.lower().split()
    tfidf_scores = tfidf.transform([text]).toarray()[0]
    word_vectors = []
    weights = []

    for word, score in zip(tfidf.get_feature_names_out(), tfidf_scores):
        if word in model and score > 0:
            word_vectors.append(model[word])
            weights.append(score)

    if not word_vectors:
        return None

    weighted_avg = np.average(word_vectors, axis=0, weights=weights)
    return weighted_avg



# TODO fix SIF
# Uses SIF to weight word vectors by importance 
# (and remove first principal component)
def create_college_vector_sif(text, model, a=1e-3):
    words = text.lower().split()
    word_vectors = [model[word] for word in words if word in model]
    if not word_vectors:
        return None

    word_freqs = {word: model.get_vecattr(word, 'count') for word in words if word in model}
    total_freq = sum(word_freqs.values())

    weighted_vectors = [model[word] * a / (a + word_freqs[word]/total_freq) for word in words if word in model]
    weighted_avg = np.mean(weighted_vectors, axis=0)

    # Skip PCA for a single vector
    if len(weighted_vectors) == 1:
        return weighted_avg

    # Perform PCA
    matrix = np.array(weighted_vectors)
    matrix = matrix - np.mean(matrix, axis=0)
    u, _, _ = svd(matrix, full_matrices=False)
    pc = u[:, 0]

    return weighted_avg - pc.dot(pc.T).dot(weighted_avg)


