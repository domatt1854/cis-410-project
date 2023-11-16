import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('vader_lexicon')

# Define some functions that can take the DataFrame generated in reddit_scraper.py
# and then returns a dataframe with the polarity scores attached