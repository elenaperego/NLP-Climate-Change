import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
# from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def tokenize(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokenized_text = ' '.join([lemmatizer.lemmatize(word) for word in tokens if word not in stop_words])
    return tokenized_text

# simple sentiment
def gen_vader(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)['compound']

def categorize_sentiment(score):
    if score > 0.05:
        return 'POSITIVE'
    elif score < -0.05:
        return 'NEGATIVE'
    else:
        return 'NEUTRAL'


article_data = pd.read_csv('data/article_data.csv')
article_data = article_data.dropna(subset=['text'])
article_data['tokenized_text'] = article_data['text'].apply(tokenize)
article_data['vader'] = article_data['tokenized_text'].apply(gen_vader)
article_data['vader_discrete'] = article_data['vader'].apply(categorize_sentiment)
article_data.to_csv('/Users/ElenaPerego/Desktop/Columbia/Natural Language Processing/qmss-nlp-climate/data/sentiment_article_data.csv')
