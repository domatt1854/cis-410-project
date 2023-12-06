import re
import nltk
import json
import string
import pandas as pd
import random
import numpy as np
import joblib
import nltk.classify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.neighbors import KNeighborsClassifier
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('movie_reviews')
nltk.download('stopwords')
nltk.download('wordnet')

class Sentiment_Scorer:
    def __init__(self, data, model):
        # Remove Nan
        data = data.dropna(subset=['text'])
        self.data = data
        if model == None:
            raise Exception("Model has not been selected")
        if model == 'K Nearest Neighbors':
            self.model = joblib.load('joblib-KNN-Model.pkl')
        elif model == 'Decision Tree':
            self.model = joblib.load('joblib-DT-Model.pkl')
        elif model == 'Random Forest':
            self.model = joblib.load('joblib-RF-Model.pkl')
        elif model == 'Logistic Regression':
            self.model = joblib.load('joblib-LR-Model.pkl')
        elif model == 'SGD Classifier':
            self.model = joblib.load('joblib-SC-Model.pkl')
        elif model == 'Hard Voting Classifier':
            self.model = joblib.load('joblib-vh-Model.pkl')
        elif model == 'Soft Voting Classifier':
            self.model = joblib.load('joblib-vs-Model.pkl')
        else:
            raise Exception("The selected model is not currently supported by our API")
            
        self.tfidf_vectorizer = joblib.load('tfidf-vector.pkl')

        with open("negative.json", "r") as fp: 
            self.positive_words = json.load(fp)
        with open("positive.json", "r") as fp: 
            self.negative_words = json.load(fp)

        self.analyzer = SentimentIntensityAnalyzer()
        self.ps = PorterStemmer()

    
    def clean_text(self,text):
        def preprocess_text(text):
            text = text.lower()
            #eliminate the punctuation, URL, and @
            text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text) 
            text = re.sub(r'\d+', '', text) # Remove digits
            text = re.sub(r'[^\w\s]', '', text) # Remove special characters
            tokens = nltk.word_tokenize(text) # Tokenize the text
            return tokens
        
        def remove_stopwords(tokens):
            stop_words = set(stopwords.words('english'))
            filtered_words = [word for word in tokens if word not in stop_words]
            return filtered_words
        
        def perform_lemmatization(tokens):
            lemmatizer = nltk.WordNetLemmatizer()
            lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
            return lemmatized_tokens
        
        tokens = preprocess_text(text)
        filtered_tokens = remove_stopwords(tokens)
        lemmatized_tokens = perform_lemmatization(filtered_tokens)
        clean_text = ' '.join(lemmatized_tokens)
        return clean_text
    

    def get_features(self, text):
        def intersection(list1,list2):
            x = set(list1)
            y = set(list2)
            z = x.intersection(y)
            return len(z)
    
        
        features = {}
        
        # Feature #1 - verbosity
        features['verbosity'] = len(text)
        
        # Feature #2 - lexical word choice
        scores = self.analyzer.polarity_scores(text)
        features['vader(pos)'] = scores['pos']
        features['vader(neg)'] = scores['neg']
        features['vader(neu)'] = scores['neu']
        features['vader(compound)'] = scores['compound']
        
        # Feature #3 - Positive and Negative Words Frequency
        words = text.split()
        words = [self.ps.stem(word) for word in words]
        pos = intersection(words,self.positive_words)
        neg = intersection(words,self.negative_words)
        features['num_pos'] = pos
        features['num_neg'] = neg
        try:
            features['tone'] = (pos-neg) / (pos+neg)
        except:
            features['tone'] = 0
    
        # Feature #4 - TFIDF
        vectors = self.tfidf_vectorizer.transform([text]).toarray()
    
        for column in range(vectors.shape[1]):
            feature_name = 'tfidf_' + str(column)
            features[feature_name] = vectors[0][column]    

        return features

        
    def label_dataset(self):
        ## 0 Indicating it is a Neutral Tweet/Comment
        ## 1 Indicating a Postive Sentiment
        ## -1 Indicating a Negative Tweet/Comment
        res = []
        for index, row in self.data.iterrows():
            try:
                res.append(self.model.classify(self.get_features(self.clean_text(row['text']))))
            except:
                res.append(None)
        result_df = self.data
        result_df['sentiment'] = res
        result_df['sentiment'] = result_df['sentiment'].apply(lambda x: calculate_sentiment(x))
    
        return result_df
        
        
def calculate_sentiment(sentiment_score):
    if sentiment_score >= 1:
        return "Positive"
    elif sentiment_score == 0:
        return "Negative"
    else:
        return "Neutral"
    