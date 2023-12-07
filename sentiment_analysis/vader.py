# TESTING MODULE AS AN EXAMPLE OF WHAT EACH MODEL COULD BE

from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

class Vader():
    def __init__(self) -> None:
        self.model = SentimentIntensityAnalyzer()
    
    def get_sentiment_scores(self, df):
        res = []

        for index, row in df.iterrows():
            # print(index)
            try:
                scores = self.model.polarity_scores(row['text'])
                # print(scores)
                scores['id'] = row['id']
                res.append(scores)
                
            except Exception:
                continue
        
        vader_results = pd.DataFrame.from_records(res).dropna()    
        vader_results['sentiment'] = vader_results['compound'].apply(calculate_sentiment)
        return vader_results.merge(df, how='left', on='id', validate="1:1")

def calculate_sentiment(sentiment_score):
    if sentiment_score >= 0.05:
        return "Positive"
    elif -0.05 <= sentiment_score <= 0.05:
        return "Neutral"
    else:
        return "Negative"