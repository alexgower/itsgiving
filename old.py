###### SENTIMENT ANALYSIS COLLEGE VECTOR EMBEDDING STUFF #####
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


def find_closest_college_with_sentiment(word, name_vectors, model):
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
    top_3_colleges = [college for college, _ in sorted_similarities[:3]]
    return top_3_colleges
