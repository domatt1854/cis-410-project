import joblib

class KNN():
    def __init__(self):
        self.KNN = joblib.load('joblib-KNN-Model.pkl')
    
    def get_sentiment_scores(self, df):
        return None
        # TODO: FILL THIS OUT
        