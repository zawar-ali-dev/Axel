# MAIN CHATBOT FILE

import os
import numpy as np
import pandas as pd
from name_management import is_name_management, find_name, get_name
from pipeline import pre_processing
from small_talk import is_small_talk
from sklearn.model_selection import train_test_split
from show_retrieval import is_show_retrieval, further_info, get_rating
from nltk.corpus import stopwords
from nltk.stem.snowball import PorterStemmer
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score , f1_score , confusion_matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sn


# Values
END = "end"
state = "normal"
flag = True
generalIntent = ""
preciseIntent = ""
CANT_FIND_SHOW = "no_show"
CHANGE = "change"
botname = "Axel"
THRESHOLD = 0.65
user = "user"
show_index = -1
query_index = -1

# Printing initial greeting
print(f">> {botname}: Hi there! I am {botname}, your personal chatbot!")
print(f">> {botname}: My main purpose is to help you with finding new shows to watch!")
print(f">> {botname}: But before any of that, what should i call you!?")
#Prompting user to get their name
user = get_name()

quit()

#Create dataframe for intent dataset
path = "./datasets/Intent.csv"
df = pd.read_csv(path)

# create the Vectorizer
vectorizer = TfidfVectorizer(analyzer='word')

# create a list of bag of words model for each document in the dataset where all the values are weighted according to tf-idf
list_of_vectors = vectorizer.fit_transform(df["Utterances"]).toarray()

# create matrix corresponding to the vectors above
df_idf_matrix = pd.DataFrame(list_of_vectors, columns = vectorizer.get_feature_names())

#********************* CODE FOR THE CLASSIFIER IMPLEMENTATION *****************************
# #create lists of the data ans the corresponding intent labels
# data = df["Utterances"].values.tolist()
# labels = df["General Intent"].values.tolist()
# labelss = df["Precise Intent"].values.tolist()


# #Creating and training classifier for general intent
# x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size = 0.25, random_state = 1)
# count_vect = CountVectorizer(lowercase=True, stop_words=stopwords.words('english'), analyzer='word')
# X_train_counts = count_vect.fit_transform(x_train)
# tfidf_transformer = TfidfTransformer(use_idf=True, sublinear_tf=True).fit(X_train_counts)
# X_train_tf = tfidf_transformer.transform(X_train_counts)
# clf = LogisticRegression(random_state=0).fit(X_train_tf, y_train)

# #Creating and training classifier for precise intent
# x_train, x_test, y_train, y_test = train_test_split(data, labelss, test_size = 0.25, random_state = 1)
# count_vect = CountVectorizer(lowercase=True, stop_words=stopwords.words('english'), analyzer='word')
# X_train_counts = count_vect.fit_transform(x_train)
# tfidf_transformer = TfidfTransformer(use_idf=True, sublinear_tf=True).fit(X_train_counts)
# X_train_tf = tfidf_transformer.transform(X_train_counts)
# clf2 = LogisticRegression(random_state=0).fit(X_train_tf, y_train)

# X_new_counts = count_vect.transform ( x_test )
# X_new_tfidf = tfidf_transformer.transform ( X_new_counts )
# predicted = clf.predict( X_new_tfidf )
#********************* CODE FOR THE CLASSIFIER IMPLEMENTATION *****************************


## MAIN CHATBOT LOOP
while flag:

    # Getting user input and preprocessing it
    query = input(f">> {user}: ")

#********************* CODE FOR THE CLASSIFIER IMPLEMENTATION *****************************
    # queryDoc = [query]
    # processed_newdata = count_vect.transform(queryDoc)
    # processed_newdata = tfidf_transformer.transform(processed_newdata )
    # generalIntent = clf.predict(processed_newdata)
    # preciseIntent = clf2.predict(processed_newdata)
#********************* CODE FOR THE CLASSIFIER IMPLEMENTATION *****************************


    # pre_process user query
    proccessed_query = pre_processing(query, False)

    # process query with tfidf vec
    input_tfidf = vectorizer.transform([proccessed_query.lower()]).toarray()
    cos = 1 - pairwise_distances(df_idf_matrix, input_tfidf, metric = 'cosine')
    cos_list = cos.tolist()

    # retrieve general and precise intent if a match is found that exceeds established threshold
    if cos.max() > THRESHOLD:
        query_index = cos_list.index(cos.max())
        generalIntent = df["General Intent"][query_index]
        preciseIntent = df["Precise Intent"][query_index]
    else:
        print(f">> {botname}: I'm sorry i don't quite understand, could you rephrase your query?")
        continue


    #Functions to check if genereal intent is show retrieval
    if generalIntent == "show":

        if preciseIntent == "discover":
            splits = re.split("about", query, flags = re.IGNORECASE)

            if (len(splits) != 2):
                #it means 'about' was not in the query
                print(f">> {botname}: I'm sorry i don't quite understand, could you rephrase your query?")
                continue           
            #get second split of the query as it contains all the useful information     
            split2 = splits[1]

            #check to see if any of the shows in our datasets match the users descriptions
            response, show_index = is_show_retrieval(split2)
            if response:
                print(f">> {botname}: {response}")
            else:
                print(f">> {botname}: I'm sorry I couldn't find a show that quite matches your description")    
            continue
        
        if preciseIntent == "further_info":
            response = further_info(show_index)
            if response:
                print(f">> {botname}: {response}")
            else:
                print(f">> {botname}: I am sorry, you haven't asked me to recommend a show yet!")
            continue

        if preciseIntent == "rating":
            response = get_rating(show_index)
            if response:
                print(f">> {botname}: This show is rated {response} out of 10")
            else:
                print(f">> {botname}: I am sorry, you haven't asked me to recommend a show yet!")
            continue

    #Functions to check if genereal intent is small talk
    if generalIntent == "small_talk":
        response = is_small_talk(preciseIntent)
        if response == END:
            print(f">> {botname}: It was great chatting with you {user}!")
            quit()
        elif response:
            print(f">> {botname}: {response}")
        else:
            print(f">> {botname}: I'm sorry i couldn't quite understand, could you be a bit more clear?")

    #Functions to check if genereal intent is name management
    if generalIntent == "name":
        response = is_name_management(preciseIntent, user)
        if response == CHANGE:
            print(f">> {botname}: Sure, what would you like me to call you?")
            user = get_name()
        elif response:
            print(f">> {botname}: {response}")
        else:
            print(f">> {botname}: I'm sorry i couldn't quite understand, could you be a bit more clear?")