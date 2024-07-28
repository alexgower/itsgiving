import numpy as np
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load pre-trained word vectors
word_vectors = KeyedVectors.load_word2vec_format('path/to/word2vec.bin', binary=True)

# Sample data
name_texts = {
    "Alice": "Alice loves reading books and solving puzzles. She's always cheerful.",
    "Bob": "Bob enjoys playing football but gets frustrated when he loses.",
    # Add more names and associated texts
}

def create_name_vector_with_sentiment(text, model):
    sia = SentimentIntensityAnalyzer()
    
    words = text.lower().split()
    word_vectors = [model[word] for word in words if word in model]
    if not word_vectors:
        return None
    
    # Calculate average word vector
    avg_vector = np.mean(word_vectors, axis=0)
    
    # Get sentiment scores
    sentiment_scores = sia.polarity_scores(text)
    sentiment_vector = np.array([
        sentiment_scores['pos'],
        sentiment_scores['neg'],
        sentiment_scores['neu'],
        sentiment_scores['compound']
    ])
    
    # Combine average word vector with sentiment vector
    return np.concatenate([avg_vector, sentiment_vector])

# Create name vectors
name_vectors = {name: create_name_vector_with_sentiment(text, word_vectors) 
                for name, text in name_texts.items()}

def find_closest_name(word, name_vectors, model):
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
    
    return max(similarities, key=similarities.get)

# Example usage
closest_name = find_closest_name("happy", name_vectors, word_vectors)
print(f"The name most associated with 'happy' is: {closest_name}")