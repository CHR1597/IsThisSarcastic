from enum import Enum
import nltk
import string
import expr_replace
import senti_word_net
import praw
import prawcore
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class PostType(Enum):
    COMMENT = 1
    SUBREDDIT = 2
    PARENT = 3


print("Loading files...")
porter = nltk.PorterStemmer()
sentiments = senti_word_net.senti_word_net()

def extract_features(comment, topic_modeller):
    features = {}
    sentence = comment["text"]
    #print("Comment:",sentence)
    
    extract_ngrams(features, sentence)
    extract_sentiment(features, sentence, PostType.COMMENT)
    extract_pos(features, sentence)
    extract_capital(features, sentence)
    extract_topic(features, sentence, topic_modeller)
    extract_reddit(features, comment)
    
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
        
def extract_sentiment(features, sentence, post_type):
    prefix = post_type.name+" "
    analyser = SentimentIntensityAnalyzer()
    sentence_sentiment = expr_replace.replace_emotion(sentence)
    tokens = nltk.word_tokenize(sentence_sentiment)
    tokens = [(t.lower()) for t in tokens]
    
    mean_sentiment = sentiments.score_sentence(tokens)
    features[prefix+"Sentiment"] = mean_sentiment[0] - mean_sentiment[1]
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()
    score = analyser.polarity_scores(blob)
    features[prefix+"VADER positive"] = score["pos"]
    features[prefix+"VADER negative"] = score["neg"]
    features[prefix+"VADER neutral"] = score["neu"]
    features[prefix+"VADER compound"] = score["compound"]
    
    blob = TextBlob(blob)
    features[prefix+"Subjectivity"] = blob.sentiment.subjectivity
    
    if len(tokens) == 1:
        tokens += ["."]
    first_part = tokens[0:len(tokens)//2]
    second_part = tokens[len(tokens)//2:]
    
    mean_sentiment_f = sentiments.score_sentence(first_part)
    features[prefix+"Sentiment 1/2"] = mean_sentiment_f[0] - mean_sentiment_f[1]
    mean_sentiment_s = sentiments.score_sentence(second_part)
    features[prefix+"Sentiment 2/2"] = mean_sentiment_s[0] - mean_sentiment_s[1]
    
    features[prefix+"Sentiment contrast 2"] = np.abs(features[prefix+"Sentiment 1/2"] - features[prefix+"Sentiment 2/2"])
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in first_part]).strip()
    score = analyser.polarity_scores(blob)
    features[prefix+"VADER positive 1/2"] = score["pos"]
    features[prefix+"VADER negative 1/2"] = score["neg"]
    features[prefix+"VADER neutral 1/2"] = score["neu"]
    features[prefix+"VADER compound 1/2"] = score["compound"]
    
    blob = TextBlob(blob)
    features[prefix+"Subjectivity 1/2"] = blob.sentiment.subjectivity
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in second_part]).strip()
    score = analyser.polarity_scores(blob)
    features[prefix+"VADER positive 2/2"] = score["pos"]
    features[prefix+"VADER negative 2/2"] = score["neg"]
    features[prefix+"VADER neutral 2/2"] = score["neu"]
    features[prefix+"VADER compound 2/2"] = score["compound"]
    
    blob = TextBlob(blob)
    features[prefix+"Subjectivity 2/2"] = blob.sentiment.subjectivity
    
    features[prefix+"VADER Sentiment contrast 2"] = np.abs(features[prefix+"VADER compound 1/2"] - features[prefix+"VADER compound 2/2"])
    
    if len(tokens) == 2:
        tokens += ["."]
    first_part = tokens[0:len(tokens)//3]
    second_part = tokens[len(tokens)//3:2*len(tokens)//3]
    third_part = tokens[2*len(tokens)//3:]
    
    mean_sentiment_f = sentiments.score_sentence(first_part)
    features[prefix+"Sentiment 1/3"] = mean_sentiment_f[0] - mean_sentiment_f[1]
    mean_sentiment_s = sentiments.score_sentence(second_part)
    features[prefix+"Sentiment 2/3"] = mean_sentiment_s[0] - mean_sentiment_s[1]
    mean_sentiment_t = sentiments.score_sentence(third_part)
    features[prefix+"Sentiment 3/3"] = mean_sentiment_t[0] - mean_sentiment_t[1]
    
    features[prefix+"Sentiment contrast 3"] = np.abs(features[prefix+"Sentiment 1/3"] - features[prefix+"Sentiment 2/3"] - features[prefix+"Sentiment 3/3"])
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in first_part]).strip()
    score = analyser.polarity_scores(blob)
    features[prefix+"VADER positive 1/3"] = score["pos"]
    features[prefix+"VADER negative 1/3"] = score["neg"]
    features[prefix+"VADER neutral 1/3"] = score["neu"]
    features[prefix+"VADER compound 1/3"] = score["compound"]
    
    blob = TextBlob(blob)
    features[prefix+"Subjectivity 1/3"] = blob.sentiment.subjectivity
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in second_part]).strip()
    score = analyser.polarity_scores(blob)
    features[prefix+"VADER positive 2/3"] = score["pos"]
    features[prefix+"VADER negative 2/3"] = score["neg"]
    features[prefix+"VADER neutral 2/3"] = score["neu"]
    features[prefix+"VADER compound 2/3"] = score["compound"]
    
    blob = TextBlob(blob)
    features[prefix+"Subjectivity 2/3"] = blob.sentiment.subjectivity
    
    blob = "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in third_part]).strip()
    score = analyser.polarity_scores(blob)
    features[prefix+"VADER positive 3/3"] = score["pos"]
    features[prefix+"VADER negative 3/3"] = score["neg"]
    features[prefix+"VADER neutral 3/3"] = score["neu"]
    features[prefix+"VADER compound 3/3"] = score["compound"]
    
    blob = TextBlob(blob)
    features[prefix+"Subjectivity 3/3"] = blob.sentiment.subjectivity
    
    features[prefix+"VADER Sentiment contrast 3"] = np.abs(features[prefix+"VADER compound 1/3"] 
                                                         - features[prefix+"VADER compound 2/3"] 
                                                         - features[prefix+"VADER compound 3/3"])
    
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
        #print("Topic details:",topic_modeller.get_topic(topics[j][0]))
        features["Topic :" + str(topics[j][0])] = topics[j][1]
        
def extract_reddit(features, comment):
    opted_in = False
    reddit = praw.Reddit("project1")
    
    subreddit = reddit.subreddit(comment["subreddit"])
    while True:
        try:
            #print("Subreddit:",subreddit.display_name)
            #print("Description:",subreddit.public_description)
            extract_sentiment(features,subreddit.public_description,PostType.SUBREDDIT)
            parent = reddit.submission(id=comment["parent"])
            #print("Parent title:",parent.title)
            extract_sentiment(features,parent.title,PostType.PARENT)
            features["Comment/Subreddit contrast"] = np.abs(features["COMMENT Sentiment"] - features["SUBREDDIT Sentiment"])
            features["Comment/Subreddit VADER contrast"] = np.abs(features["COMMENT VADER compound"] - features["SUBREDDIT VADER compound"])
            features["Comment/Parent contrast"] = np.abs(features["COMMENT Sentiment"] - features["PARENT Sentiment"])
            features["Comment/Parent VADER contrast"] = np.abs(features["COMMENT VADER compound"] - features["PARENT VADER compound"])
            break
        except prawcore.exceptions.Forbidden:
            if opted_in:
                #print(comment["subreddit"],": Subreddit no longer exists.",sep="")
                break
            subreddit.quaran.opt_in()   # Opt into quarantined subreddit
            opted_in = True
            continue
        