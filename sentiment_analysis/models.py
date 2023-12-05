import nltk
import pandas as pd
import random
import numpy as np
import joblib
import nltk.classify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.neighbors import KNeighborsClassifier
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
nltk.download('movie_reviews')

class Sentiment_Scorer:
    def __init__(self, data, model):
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

        unwanted = nltk.corpus.stopwords.words("english")
        unwanted.extend([w.lower() for w in nltk.corpus.names.words()])
        def skip_unwanted(pos_tuple):
            word, tag = pos_tuple
            if not word.isalpha() or word in unwanted:
                return False
            if tag.startswith("NN"):
                return False
            return True
        self.positive_words = [word for word, tag in filter(
                          skip_unwanted,
                          nltk.pos_tag(nltk.corpus.movie_reviews.words(categories=["pos"]))
                        )]
        self.negative_words = [word for word, tag in filter(
                          skip_unwanted,
                          nltk.pos_tag(nltk.corpus.movie_reviews.words(categories=["neg"]))
                        )]

        self.analyzer = SentimentIntensityAnalyzer()
        self.ps = PorterStemmer()

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
        words = word_tokenize(text)
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
                res.append(self.model.classify(self.get_features(row['text'])))
            except:
                res.append(None)
        result_df = self.data
        result_df['sentiment'] = res
    
        return result_df
        
        
        
    