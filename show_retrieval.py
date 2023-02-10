# THIS PYTHON FILE WILL HANDLE The show retrieval

import random
from pipeline import pre_processing
import pandas as pd
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer

#values
THRESHOLD_RETRIEVAL = 0.15
botname = "Axel"
CANT_FIND_SHOW = "no_show"


# reading in small talk dataset
path = "./datasets/dataanime.csv"
df = pd.read_csv(path)
df_copy = df['Description'].copy()


# create the vectorizers
vectorizer = TfidfVectorizer(analyzer='word')

# pre-process the description part of the dataset so that a match can be found between the processed query and the dataset
num=0
for d in df['Description']:
    processed_d = pre_processing(d, True)
    df_copy[num] = processed_d
    num +=1

# create a list of bag of words model for each document in the dataset where all the values are weighted according to tf-idf
list_of_vectors = vectorizer.fit_transform(df_copy).toarray()


# create matrix corresponding to the vectors above
df_idf_matrix = pd.DataFrame(list_of_vectors, columns = vectorizer.get_feature_names())


# list of potential responses for show recommendation
responses = ["You should watch: ", "Have you considered watching: ", "I think you would really like: "]

# Function to retrieve the rating of a particular show
def get_rating(show_index):

    if(show_index == -1):
        return False
    
    response = df['Score'][show_index]
    return response

# Function to return more infor regarding a particular show
def further_info(show_index):

    if(show_index == -1):
        return False
    description = df['Description'][show_index]
    response = "Alright here you go!: \n" + description
    return response
    

# Checking for show retrieval function
def is_show_retrieval(query):
    response = False

    query = pre_processing(query, False)

    #vectorize query with tfidf
    input_tfidf1 = vectorizer.transform([query.lower()]).toarray()
    cos = 1 - pairwise_distances(df_idf_matrix, input_tfidf1, metric = 'cosine')
    cos_list = cos.tolist()
    if cos.max() > THRESHOLD_RETRIEVAL:
            show_index = cos_list.index(cos.max())
            show_name = df['Title'][show_index]
            response = random.choice(responses) + show_name
            return response, show_index
    return response, -1






