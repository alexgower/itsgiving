import numpy as np
from gensim.models import KeyedVectors

import json

from college_embeddings_utils import *


### COLLEGES CONFIGURATION ###

univeristies = ["oxford", "cambridge"]
undergrad_colleges_only_options = [True, False]

for university in univeristies:
    for undergrad_colleges_only in undergrad_colleges_only_options:

        print(f"Processing {university} {'undergrad colleges only' if undergrad_colleges_only else 'all colleges'}")

        college_posts_compilation_filename = 'data/oxfess_data_college_compilation.json' if university == "oxford" else 'data/camfess_data_college_compilation.json'


        # Define college lists
        oxford_colleges = [
            "All Souls", "Balliol", "Blackfriars", "Brasenose", "Campion Hall",
            "Christ Church", "Corpus Christi", "Exeter", "Green Templeton",
            "Harris Manchester", "Hertford", "Jesus", "Keble", "Kellogg",
            "Lady Margaret Hall", "Linacre", "Lincoln", "Magdalen", "Mansfield",
            "Merton", "New", "Nuffield", "Oriel", "Pembroke", "Queen's",
            "Regent's Park", "Reuben", "Somerville", "St Anne's", "St Anthony's",
            "St Catherine's", "St Cross", "St Edmund Hall", "St Hilda's", "St Hugh's",
            "St John's", "St Peter's", "St Stephen's House", "Trinity", "University",
            "Wadham", "Wolfson", "Worcester", "Wycliffe Hall", "OUCA", "Union",
        ]
        oxford_undergraduate_colleges  = [
            "All Souls", "Balliol", "Brasenose",
            "Christ Church", "Corpus Christi", "Exeter",
            "Harris Manchester", "Hertford", "Jesus", "Keble",
            "Lady Margaret Hall", "Lincoln", "Magdalen", "Mansfield",
            "Merton", "New", "Oriel", "Pembroke", "Queen's",
            "Reuben", "Somerville", "St Anne's", 
            "St Catherine's", "St Edmund Hall", "St Hilda's", "St Hugh's",
            "St John's", "St Peter's", "Trinity", "University",
            "Wadham",  "Worcester", "OUCA", "Union",
        ]

        cambridge_colleges = [
            "Christ's", "Churchill", "Clare", "Clare Hall", "Corpus Christi",
            "Darwin", "Downing", "Emmanuel", "Fitzwilliam", "Girton",
            "Gonville and Caius", "Homerton", "Hughes Hall", "Jesus", "King's",
            "Lucy Cavendish", "Magdalene", "Murray Edwards", "Newnham", "Pembroke",
            "Peterhouse", "Queens'", "Robinson", "Selwyn", "Sidney Sussex",
            "St Catharine's", "St Edmund's", "St John's", "Trinity", "Trinity Hall", "Wolfson"
        ]
        cambridge_undergraduate_colleges = [
            "Christ's", "Churchill", "Clare", "Corpus Christi",
            "Downing", "Emmanuel", "Fitzwilliam", "Girton",
            "Gonville and Caius", "Homerton", "Jesus", "King's",
            "Magdalene", "Murray Edwards", "Newnham", "Pembroke",
            "Peterhouse", "Queens'", "Robinson", "Selwyn", "Sidney Sussex",
            "St Catharine's", "St John's", "Trinity", "Trinity Hall",
        ]

        # Select college list
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
        word_vectors = KeyedVectors.load_word2vec_format('itsgiving/wordinput/static/wordinput/data/wiki-news-300d-1M.vec', binary=False, limit=200000)






        ### CREATE COLLEGE WORD STRINGS ###

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


        print("Colleges ordered by most text length: ", sorted(college_texts, key=lambda x: len(college_texts[x]), reverse=True))





        ### CREATE COLLEGE VECTORS ###


        # Create all college vectors vectors
        all_college_vectors_avg = {college: create_college_vector_avg(text, word_vectors)
                        for college, text in college_texts.items()}

        all_college_vectors_tfid = {college: create_college_vector_tfid(text, word_vectors, college_texts) 
                        for college, text in college_texts.items()}

        # all_college_vectors_sif = {college: create_college_vector_sif(text, word_vectors)
                        # for college, text in college_texts.items()}


        permitted_college_vectors_avg = {college: vec for college, vec in all_college_vectors_avg.items() if college in colleges_list}
        permitted_college_vectors_tfid = {college: vec for college, vec in all_college_vectors_tfid.items() if college in colleges_list}

        # permitted_college_vectors_sif = {college: vec for college, vec in all_college_vectors_sif.items() if college in colleges_list}





        ### EXPORT COLLEGE VECTORS TO FILES ###

        # Convert NumPy arrays to lists
        def convert_np_to_list(data):
            return {college: vec.tolist() if isinstance(vec, np.ndarray) else vec for college, vec in data.items()}

        permitted_college_vectors_avg_list = convert_np_to_list(permitted_college_vectors_avg)
        permitted_college_vectors_tfid_list = convert_np_to_list(permitted_college_vectors_tfid)
        # permitted_college_vectors_sif_list = convert_np_to_list(permitted_college_vectors_sif)

        # Save average vectors
        with open(f'data/{university}_undergrad_only_{undergrad_colleges_only}_college_vectors_avg.json', 'w') as f:
            json.dump(permitted_college_vectors_avg_list, f)

        # Save TF-IDF vectors
        with open(f'data/{university}_undergrad_only_{undergrad_colleges_only}_college_vectors_tfid.json', 'w') as f:
            json.dump(permitted_college_vectors_tfid_list, f)

        # Uncomment if you need to save SIF vectors as well
        # with open(f'data/{university}_undergrad_only_{undergrad_colleges_only}_college_vectors_sif.json', 'w') as f:
        #     json.dump(permitted_college_vectors_sif_list, f)


        print("College vectors exported successfully.")











