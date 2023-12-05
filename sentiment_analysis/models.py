from nltk.sentiment import SentimentIntensityAnalyzer
from vader import Vader
import joblib

class Model:
    def __init__(self):
        self.model_name = None

        # Load in All Models Pickle Files Here
        
        self.vader = Vader()
        self.decisionTree = joblib.load('joblib-DT-Model.pkl')
        self.kNN = joblib.load('joblib-KNN-Model.pkl')
        self.logisticRegression = joblib.load('joblib-LR-Model.pkl')
        self.randomForest = joblib.load('joblib-RF-Model.pkl')
        self.sgd = joblib.load('joblib-SC-Model.pkl')
        self.votingSoft = joblib.load('joblib-vh-Model.pkl')
        self.votingHard =  joblib.load('joblib-vs-model.pkl')
        
        ## Load in Logistic Regression, K nearest Neighbors, etc.
        
    
    def select_model(self, model):
        self.model_name = model
    
    def get_polarity_scores(self, df):
        if not self.model_name:
            raise Exception("Model has not been selected")
        
        if self.model_name == "VADER":
            return self.vader.get_sentiment_scores(df)
        elif self.model_name == "K-Nearest-Neighbors":
            # Run code to return KNN Here
            return None
        
        
        
    