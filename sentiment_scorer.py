# sentiment_scorer.py will take a dataframe created from reddit_scraper and attach sentiment scores to the dataframe

# Exploration will be done on notebooks for different models, but when we learn how to score the data, we can move that logic here

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd


# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('vader_lexicon')
nltk.download('stopwords')


# Define a function that can take the DataFrame generated in reddit_scraper.py
# and then returns a dataframe with the polarity scores attached

# We can specify different models using the `model` Kwarg
def get_polarity_scores(df: pd.DataFrame, model='VADER') -> pd.DataFrame:
    # merge the following columns onto the dataframe and return it
        # pos: positive score
        # neg: negative score
        # neu: neutral score
        # compound: compound

    if model == 'VADER':
        ## Return VADER results
        return
    elif model == 'huggingface':
        ## Return huggingface results
        return