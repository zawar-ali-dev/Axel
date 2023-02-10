#THIS PYTHON FILE WILL HANDLE THE TEXT-PREPROCESSING UP TO THE STEMMING PROCESS


import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


# First we define the main function, which, when given an input will go through
# all the steps in the pre-processing pipeline
def pre_processing(input, removeStopWords):

    # Tokenising the input
    tokenizer = nltk.RegexpTokenizer(r"\w+")  #only keep words
    tokenised = tokenizer.tokenize(input)

    # Lower-casing
    lowercased = [word.lower() for word in tokenised]
    
    # Filtering Stopwords (NOTE: we don't always want to filter stop words, so we have a boolean input to this function
    # which determines whether we will or won't filter)
    if removeStopWords:
        # Remove stopwords and lower casing
        personalised_stopwords = ["show", "anime", "want", "wanna", "watch", "about"]
        english_stopwords = stopwords.words('english')
        filtered = [word for word in lowercased
                        if word not in english_stopwords and word not in personalised_stopwords]
    else:
        filtered = lowercased

    # Stemming
    sb_stemmer = SnowballStemmer('english')
    stemmed = [sb_stemmer.stem(word) for word in filtered]

    # Returning the processed input
    return " ".join(stemmed)


