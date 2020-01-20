import nltk
import string
import expr_replace
import senti_word_net
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

print("Loading files...")
porter = nltk.PorterStemmer()
sentiments = senti_word_net.senti_word_net()

def extract_features(comment, topic_modeller):
    features = {}
    sentence = comment["text"]
    
    extract_ngrams(features, sentence)
    extract_sentiment(features, sentence)
    #extract_pos(features, sentence)
    #extract_capital(features, sentence)
    #extract_topic(features, sentence, topic_modeller)
    #extract_reddit(features, comment)
    
    return features
    
def extract_ngrams(features, sentence):
    sentence_reg = expr_replace.replace_general(sentence)
    
    tokens = nltk.word_tokenize(sentence_reg)
    tokens = [porter.stem(t.lower()) for t in tokens]
    bigrams = nltk.bigrams(tokens)
    bigrams = [tup[0]+" "+tup[1] for tup in bigrams]
    grams = tokens + bigrams
    
    for t in grams:
        features["contains(%s)" % t] = 1.0
        
def extract_sentiment(features, sentence):
    analyser = SentimentIntensityAnalyzer()
    sentence_sentiment = expr_replace.replace_emotion(sentence)
    tokens = nltk.word_tokenize(sentence_sentiment)
    tokens = [(t.lower()) for t in tokens]
    
    mean_sentiment = sentiments.score_sentence(tokens)
    features["Sentiment"] = mean_sentiment[0] - mean_sentiment[1]
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()
    score = analyser.polarity_scores(blob)
    features["VADER positive"] = score["pos"]
    features["VADER negative"] = score["neg"]
    features["VADER neutral"] = score["neu"]
    features["VADER compound"] = score["compound"]
    
    blob = TextBlob(blob)
    features["Subjectivity"] = blob.sentiment.subjectivity
    