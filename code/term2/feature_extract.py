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
    extract_pos(features, sentence)
    extract_capital(features, sentence)
    extract_topic(features, sentence, topic_modeller)
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
    
    if len(tokens) == 1:
        tokens += ["."]
    first_part = tokens[0:len(tokens)//2]
    second_part = tokens[len(tokens)//2:]
    
    mean_sentiment_f = sentiments.score_sentence(first_part)
    features["Sentiment 1/2"] = mean_sentiment_f[0] - mean_sentiment_f[1]
    mean_sentiment_s = sentiments.score_sentence(second_part)
    features["Sentiment 2/2"] = mean_sentiment_s[0] - mean_sentiment_s[1]
    
    features["Sentiment contrast 2"] = np.abs(features["Sentiment 1/2"] - features["Sentiment 2/2"])
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in first_part]).strip()
    score = analyser.polarity_scores(blob)
    features["VADER positive 1/2"] = score["pos"]
    features["VADER negative 1/2"] = score["neg"]
    features["VADER neutral 1/2"] = score["neu"]
    features["VADER compound 1/2"] = score["compound"]
    
    blob = TextBlob(blob)
    features["Subjectivity 1/2"] = blob.sentiment.subjectivity
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in second_part]).strip()
    score = analyser.polarity_scores(blob)
    features["VADER positive 2/2"] = score["pos"]
    features["VADER negative 2/2"] = score["neg"]
    features["VADER neutral 2/2"] = score["neu"]
    features["VADER compound 2/2"] = score["compound"]
    
    blob = TextBlob(blob)
    features["Subjectivity 2/2"] = blob.sentiment.subjectivity
    
    features["VADER Sentiment contrast 2"] = np.abs(features["VADER compound 1/2"] - features["VADER compound 2/2"])
    
    if len(tokens) == 2:
        tokens += ["."]
    first_part = tokens[0:len(tokens)//3]
    second_part = tokens[len(tokens)//3:2*len(tokens)//3]
    third_part = tokens[2*len(tokens)//3:]
    
    mean_sentiment_f = sentiments.score_sentence(first_part)
    features["Sentiment 1/3"] = mean_sentiment_f[0] - mean_sentiment_f[1]
    mean_sentiment_s = sentiments.score_sentence(second_part)
    features["Sentiment 2/3"] = mean_sentiment_s[0] - mean_sentiment_s[1]
    mean_sentiment_t = sentiments.score_sentence(third_part)
    features["Sentiment 3/3"] = mean_sentiment_t[0] - mean_sentiment_t[1]
    
    features["Sentiment contrast 3"] = np.abs(features["Sentiment 1/3"] - features["Sentiment 2/3"] - features["Sentiment 3/3"])
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in first_part]).strip()
    score = analyser.polarity_scores(blob)
    features["VADER positive 1/3"] = score["pos"]
    features["VADER negative 1/3"] = score["neg"]
    features["VADER neutral 1/3"] = score["neu"]
    features["VADER compound 1/3"] = score["compound"]
    
    blob = TextBlob(blob)
    features["Subjectivity 1/3"] = blob.sentiment.subjectivity
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in second_part]).strip()
    score = analyser.polarity_scores(blob)
    features["VADER positive 2/3"] = score["pos"]
    features["VADER negative 2/3"] = score["neg"]
    features["VADER neutral 2/3"] = score["neu"]
    features["VADER compound 2/3"] = score["compound"]
    
    blob = TextBlob(blob)
    features["Subjectivity 2/3"] = blob.sentiment.subjectivity
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in third_part]).strip()
    score = analyser.polarity_scores(blob)
    features["VADER positive 3/3"] = score["pos"]
    features["VADER negative 3/3"] = score["neg"]
    features["VADER neutral 3/3"] = score["neu"]
    features["VADER compound 3/3"] = score["compound"]
    
    blob = TextBlob(blob)
    features["Subjectivity 3/3"] = blob.sentiment.subjectivity
    
    features["VADER Sentiment contrast 3"] = np.abs(features["VADER compound 1/3"] - features["VADER compound 2/3"] - features["VADER compound 3/3"])
    
def extract_pos(features, sentence):
    sentence_pos = expr_replace.replace_emotion(sentence)
    tokens = nltk.word_tokenize(sentence_pos)
    tokens = [(t.lower()) for t in tokens]
    pos_vector = sentiments.posvector(tokens)
    for j in range(len(pos_vector)):
        features["POS" + str(j+1)] = pos_vector[j]
        
def extract_capital(features, sentence):
    counter = 0
    threshold = 4
    for j in range(len(sentence)):
        counter += int(sentence[j].isupper())
    features["Capitalisation"] = int(counter >= threshold)
    
def extract_topic(features, sentence, topic_modeller):
    topics = topic_modeller.transform(sentence)
    
    for j in range(len(topics)):
        features["Topic :" + str(topics[j][0])] = topics[j][1]