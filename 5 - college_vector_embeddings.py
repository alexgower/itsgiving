import numpy as np
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json


college_posts_compilation_filename = 'data/camfess_data_college_compilation.json'

# Load pre-trained word vectors
# TODO try with bigger model too
# TODO try without limits
word_vectors = KeyedVectors.load_word2vec_format('data/wiki-news-300d-1M.vec', binary=False, limit=200000)


def create_name_vector_with_sentiment(text, model):
    sia = SentimentIntensityAnalyzer()
    
    words = text.lower().split()
    word_vectors = [model[word] for word in words if word in model]
    if not word_vectors:
        return None
    
    # Calculate average word vector
    # TODO make this better than an average eventually
    avg_vector = np.mean(word_vectors, axis=0)
    
    # Get sentiment scores
    sentiment_scores = sia.polarity_scores(text)
    sentiment_vector = np.array([
        sentiment_scores['pos'],
        sentiment_scores['neg'],
        sentiment_scores['neu'],
        sentiment_scores['compound']
    ])

    print("Sentiment vector: ", sentiment_vector)
    
    # Combine average word vector with sentiment vector
    return np.concatenate([avg_vector, sentiment_vector])


def find_closest_college(word, name_vectors, model):
    sia = SentimentIntensityAnalyzer()
    
    if word not in model:
        return "Word not found in the model"
    
    # Get word vector
    word_vector = model[word]
    
    # Get sentiment scores for the word
    sentiment_scores = sia.polarity_scores(word)
    sentiment_vector = np.array([
        sentiment_scores['pos'],
        sentiment_scores['neg'],
        sentiment_scores['neu'],
        sentiment_scores['compound']
    ])
    
    # Combine word vector with sentiment vector
    word_vector_with_sentiment = np.concatenate([word_vector, sentiment_vector])
    
    # Calculate similarities
    similarities = {name: cosine_similarity([word_vector_with_sentiment], [vec])[0][0] 
                    for name, vec in name_vectors.items() if vec is not None}
    
    # TODO maybe show top 3 or something
    # Sort similarities in descending order
    sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    # Get top 3 most similar colleges
    # with angles
    top_3_colleges = [college for college, _ in sorted_similarities[:3]]
    return top_3_colleges

    # top_3_colleges = [college for college, _ in sorted_similarities[:3]]
    # return top_3_colleges

    # return max(similarities, key=similarities.get)



# Gather text data for each college
with open(college_posts_compilation_filename, 'r') as f:
    data = json.load(f)

# Dictionary to store the concatenated text for each college
college_texts = {}

# Process each college and its posts
for college, posts in data.items():
    print(f"Processing college: {college}")
    # Join all texts for this college into one long string
    college_texts[college] = " ".join(post['text'] for post in posts)

    print(f"Text length: {len(college_texts[college])}")

# Create name vectors
name_vectors = {college: create_name_vector_with_sentiment(text, word_vectors) 
                for college, text in college_texts.items()}

# Example usage
closest_name = find_closest_college("happy", name_vectors, word_vectors)
print(f"The college most associated with 'happy' is: {closest_name}")

closest_name = find_closest_college("sad", name_vectors, word_vectors)
print(f"The college most associated with 'sad' is: {closest_name}")

closest_name = find_closest_college("party", name_vectors, word_vectors)
print(f"The college most associated with 'party' is: {closest_name}")

closest_name = find_closest_college("study", name_vectors, word_vectors)
print(f"The college most associated with 'study' is: {closest_name}")

closest_name = find_closest_college("essay", name_vectors, word_vectors)
print(f"The college most associated with 'essay' is: {closest_name}")

closest_name = find_closest_college("queer", name_vectors, word_vectors)
print(f"The college most associated with 'queer' is: {closest_name}")

closest_name = find_closest_college("racist", name_vectors, word_vectors)
print(f"The college most associated with 'racist' is: {closest_name}")

closest_name = find_closest_college("racism", name_vectors, word_vectors)
print(f"The college most associated with 'racism' is: {closest_name}")

closest_name = find_closest_college("sporty", name_vectors, word_vectors)
print(f"The college most associated with 'sporty' is: {closest_name}")

closest_name = find_closest_college("jewish", name_vectors, word_vectors)
print(f"The college most associated with 'jewish' is: {closest_name}")