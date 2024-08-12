# TODO UNDERSTAND THIS FILE AND IMPROVE SO DOESN'T IMPORT TWICE and wheenver load/save code?
from django.apps import AppConfig

class WordInputConfig(AppConfig):
    default = True
    name = 'wordinput'

    def ready(self):
        print("WordInputConfig.ready() is being called")
        from .model_loader import load_wiki_word_embedding_model
        load_wiki_word_embedding_model()