from gensim.models import KeyedVectors
from django.contrib.staticfiles import finders

wiki_word_embedding_model = None

def load_wiki_word_embedding_model():
    global wiki_word_embedding_model
    print("Starting to load wiki_word_embedding_model")
    model_filepath = finders.find('wordinput/data/wiki-news-300d-1M.vec')
    wiki_word_embedding_model = KeyedVectors.load_word2vec_format(model_filepath, binary=False, limit=200000)
    print("Finished loading wiki_word_embedding_model")
