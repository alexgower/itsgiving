import numpy as np
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.linalg import svd
import json


### COLLEGES CONFIGURATION ###

university = "oxford"
undergrad_colleges_only = True

college_posts_compilation_filename = 'data/oxfess_data_college_compilation.json' if university == "oxford" else 'data/camfess_data_college_compilation.json'

oxford_undergraduate_colleges  = [
    "All Souls", "Balliol", "Brasenose",
    "Christ Church", "Corpus Christi", "Exeter",
    "Harris Manchester", "Hertford", "Jesus", "Keble",
    "Lady Margaret Hall", "Lincoln", "Magdalen", "Mansfield",
    "Merton", "New College", "Oriel", "Pembroke", "Queen's",
    "Reuben", "Somerville", "St Anne's", 
    "St Catherine's", "St Edmund Hall", "St Hilda's", "St Hugh's",
    "St John's", "St Peter's", "Trinity", "University",
    "Wadham",  "Worcester", "OUCA", "Union",
]

oxford_colleges = [
    "All Souls", "Balliol", "Blackfriars", "Brasenose", "Campion Hall",
    "Christ Church", "Corpus Christi", "Exeter", "Green Templeton",
    "Harris Manchester", "Hertford", "Jesus", "Keble", "Kellogg",
    "Lady Margaret Hall", "Linacre", "Lincoln", "Magdalen", "Mansfield",
    "Merton", "New College", "Nuffield", "Oriel", "Pembroke", "Queen's",
    "Regent's Park", "Reuben", "Somerville", "St Anne's", "St Antony's",
    "St Catherine's", "St Cross", "St Edmund Hall", "St Hilda's", "St Hugh's",
    "St John's", "St Peter's", "St Stephen's House", "Trinity", "University",
    "Wadham", "Wolfson", "Worcester", "Wycliffe Hall", "OUCA", "Union", "None"
]

cambridge_undergraduate_colleges = cambridge_colleges = [
    "Christ's", "Churchill", "Clare", "Corpus Christi",
    "Downing", "Emmanuel", "Fitzwilliam", "Girton",
    "Gonville and Caius", "Homerton", "Jesus", "King's",
    "Magdalene", "Murray Edwards", "Newnham", "Pembroke",
    "Peterhouse", "Queens'", "Robinson", "Selwyn", "Sidney Sussex",
    "St Catharine's", "St John's", "Trinity", "Trinity Hall",
]


cambridge_colleges = [
    "Christ's", "Churchill", "Clare", "Clare Hall", "Corpus Christi",
    "Darwin", "Downing", "Emmanuel", "Fitzwilliam", "Girton",
    "Gonville and Caius", "Homerton", "Hughes Hall", "Jesus", "King's",
    "Lucy Cavendish", "Magdalene", "Murray Edwards", "Newnham", "Pembroke",
    "Peterhouse", "Queens'", "Robinson", "Selwyn", "Sidney Sussex",
    "St Catharine's", "St Edmund's", "St John's", "Trinity", "Trinity Hall", "Wolfson"
]

if university == "oxford":
    if undergrad_colleges_only:
        colleges_list = oxford_undergraduate_colleges
    else:
        colleges_list = oxford_colleges
else:
    if undergrad_colleges_only:
        colleges_list = cambridge_undergraduate_colleges
    else:
        colleges_list = cambridge_colleges
    





### WORD VECTORS CONFIGURATION ###

# Load pre-trained word vectors
# TODO try with bigger model too
# TODO try without limits - would this be obvious as give errors if not though?
word_vectors = KeyedVectors.load_word2vec_format('words/wiki-news-300d-1M.vec', binary=False, limit=200000)







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

    # Get top 3 most similar colleges
    # top_3_colleges = [college for college, _ in sorted_similarities[:3]]

    # Get top 3 most similar colleges with similarity scores
    top_3_colleges = [(college, score) for college, score in sorted_similarities[:3]]

    return top_3_colleges







### CREATE COLLEGE VECTORS ###

# Gather text data for each college
with open(college_posts_compilation_filename, 'r') as f:
    data = json.load(f)

# Dictionary to store the concatenated text for each college
college_texts = {}

# Process each college and its posts
for college, posts in data.items():
    print(f"Processing college: {college}")
    # Join all texts for this college into one long string
    try: 
        college_texts[college] = " ".join(post['text'] for post in posts if isinstance(post['text'], str))
    except:
        print(f"Error processing college: {college}")
        for i, post in enumerate(posts):
            print(i)
            print(post)

    print(f"Text length: {len(college_texts[college])}")


print("")
print("College vectors created successfully.")
print("Colleges ordered by most text length: ", sorted(college_texts, key=lambda x: len(college_texts[x]), reverse=True))




# Create all college vectors vectors
all_college_vectors_avg = {college: create_college_vector_avg(text, word_vectors)
                for college, text in college_texts.items()}

all_college_vectors_tfid = {college: create_college_vector_tfid(text, word_vectors, college_texts) 
                for college, text in college_texts.items()}

all_college_vectors_sif = {college: create_college_vector_sif(text, word_vectors)
                for college, text in college_texts.items()}


permitted_college_vectors_avg = {college: vec for college, vec in all_college_vectors_avg.items() if college in colleges_list}
permitted_college_vectors_tfid = {college: vec for college, vec in all_college_vectors_tfid.items() if college in colleges_list}
permitted_college_vectors_sif = {college: vec for college, vec in all_college_vectors_sif.items() if college in colleges_list}








### EXAMPLE USAGE ###
# TODO slider for all colleges or (default) undergrad colleges only
# TODO slider for Avg or SIF or (default) Tfid
words_to_test = ["happy", "sad", "party", "study", "essay", "queer", "racist", "sporty", "jewish", "christian", "muslim", "atheist",
                 "conservative", "gay", "boring", "exciting", "stressful", "easy", "hard", "expensive", "cheap", "beautiful", "ugly", "far", 
                 "girls", "women", "boys", "men", "football", "rugby", "rowing", "swimming", "pool", "gym", "library"]

for word in words_to_test:
    closest_colleges = find_closest_college(word, permitted_college_vectors_avg, word_vectors)
    print(f"Avg: The colleges most associated with '{word}' are: {closest_colleges}")

    closest_colleges = find_closest_college(word, permitted_college_vectors_tfid, word_vectors)
    print(f"Tfid: The colleges most associated with '{word}' are: {closest_colleges}")

    closest_colleges = find_closest_college(word, permitted_college_vectors_sif, word_vectors)
    print(f"Sif: The colleges most associated with '{word}' are: {closest_colleges}")

    print("")





