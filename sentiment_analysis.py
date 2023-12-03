import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem import WordNetLemmatizer
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import torch

def tokenize(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokenized_text = ' '.join([lemmatizer.lemmatize(word) for word in tokens if word not in stop_words])
    return tokenized_text

# VADER Sentiment Analysis
def gen_vader(text):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)['compound']

def gen_sentiment(text):
    model = pipeline("sentiment-analysis")
    def chunk_text(text, max_chunk_char_length):
        for start in range(0, len(text), max_chunk_char_length):
            end = start + max_chunk_char_length
            yield text[start:end]
    max_chunk_char_length = 1000
    text_chunks = list(chunk_text(text, max_chunk_char_length))
    sentiment_counts = Counter()
    for chunk in text_chunks:
        result = model(chunk)
        sentiment_counts[result[0]['label']] += 1
    most_common_sentiment = sentiment_counts.most_common(1)[0][0]
    return most_common_sentiment


def categorize_vader(score):
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
article_data['vader_discrete'] = article_data['vader'].apply(categorize_vader)
for idx, row in article_data.iterrows():
    article_data.at[idx, 'sentiment'] = gen_sentiment(row['text'])
article_data.to_csv('/Users/ElenaPerego/Desktop/Columbia/Natural Language Processing/qmss-nlp-climate/data/sentiment_article_data_new.csv')
# article_data.to_csv('/Users/ElenaPerego/Desktop/Columbia/Natural Language Processing/qmss-nlp-climate/data/sentiment_article_data.csv')
