from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

class Vader():
    def __init__(self) -> None:
        self.model = SentimentIntensityAnalyzer()
    
    def get_sentiment_scores(self, df):
        res = []

        for index, row in df.iterrows():
            print(index)
            try:
                res.append(self.model.polarity_scores(row['text']))
            except Exception:
                res.append(
                    {
                        'neg': None,
                        'neu': None,
                        'pos': None,
                        'compound': None
                    }
                )
        
        vader_results = pd.DataFrame.from_records(res).reset_index().rename(columns={'index': 'Unnamed: 0'}).merge(df, how='left')
        vader_results['sentiment'] = vader_results['compound'].apply(calculate_sentiment)
        
        return vader_results
        
def calculate_sentiment(self, sentiment_score):
    if sentiment_score >= 0.05:
        return "Positive"
    elif -0.05 <= sentiment_score <= 0.05:
        return "Neutral"
    else:
        return "Negative"
