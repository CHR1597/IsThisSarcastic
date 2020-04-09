"""Train a new classifier on the processed comment data.

This script creates a topic modeller, extracts features from the dataset, and
uses those features to train a new classifier. A report is printed after training.

Usage:
train.py <include_reddit> <classif_type>
where:
include_reddit -- 0 to skip Reddit context, 1 to include.
classif_type   -- 1 for a Linear SVC classifier, 2 for a Logistic Regression classifier.
"""

import os
import sys
import random
import json
import pickle
import heapq
import numpy as np
import scipy as sp
from sklearn.feature_extraction import DictVectorizer
from sklearn.utils import shuffle
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import feature_extract
import topic

folder = os.path.join(os.path.dirname(__file__),"../..")

include_reddit = int(sys.argv[1])
classif_type = int(sys.argv[2])

print ("Preparing...")
sarc_data = np.load("sarc-processed.npy")
non_data = np.load("nonsarc-processed.npy")

print("Training topics...\n")
topic_mod = topic.topic(nbtopic=200, alpha = "symmetric")
topic_mod.fit(np.concatenate((sarc_data,non_data)))

print("Extracting features...")
sarcs = json.loads(open(os.path.join(folder,"sarc-comments.json"),"r").read())
nonsarcs = json.loads(open(os.path.join(folder,"nonsarc-comments.json"),"r").read())

labels = ["Sarcastic", "Non-Sarcastic"]
featuresets = []

i = 1
for k,v in sarcs.items():
    print(i, "sarcastic comments processed of", len(sarcs), end="\r")
    featuresets.append((feature_extract.extract_features(v, topic_mod, include_reddit), labels[0]))
    i += 1
    
print()
i = 1
for k,v in nonsarcs.items():
    print(i, "non-sarcastic comments processed of", len(nonsarcs), end="\r")
    featuresets.append((feature_extract.extract_features(v, topic_mod, include_reddit), labels[1]))
    i += 1

print()    
featuresets = np.array(featuresets)
targets = (featuresets[0::,1]=="Sarcastic").astype(int)

print("Generating vectorizer...")
vec = DictVectorizer()
featurevec = vec.fit_transform(featuresets[0::,0])

file_name = "vecdict_" + str(len(featuresets))
if include_reddit:
    file_name += "_reddit"
file_name += ".p"
file_object = open(file_name,"wb")
pickle.dump(vec,file_object)
file_object.close()

print("Splitting features...")
order = shuffle(range(len(featuresets)))
targets = targets[order]
featurevec = featurevec[order,0::]

size = int(len(featuresets) * 0.3)  # Train/test split

trainvec = featurevec[size:,0::]
train_targets = targets[size:]
testvec = featurevec[:size,0::]
test_targets = targets[:size]

print("Training...")
c = 0.1
pos_p = (train_targets == 1)
neg_p = (train_targets == 0)
ratio = np.sum(neg_p.astype(float))/np.sum(pos_p.astype(float))
new_trainvec = trainvec
new_train_targets = train_targets
for j in range(int(ratio-1.0)):
    new_trainvec = sp.sparse.vstack([new_trainvec,trainvec[pos_p,0::]])
    new_train_targets = np.concatenate((new_train_targets, train_targets[pos_p]))


classifier = None
if classif_type == 1:
    classifier = LinearSVC(C=c, max_iter = 10000)
else:
    classifier = LogisticRegression(C=c,solver="lbfgs", multi_class="auto", max_iter = 2000)

    
classifier.fit(new_trainvec,new_train_targets)

print("Trained. Saving...")
file_name = ""
if isinstance(classifier, LinearSVC):
    file_name += "svc"
elif isinstance(classifier, LogisticRegression):
    file_name += "lr"
else:
    file_name += "rfc"
    
file_name += "_" + str(len(featuresets))
if include_reddit:
    file_name += "_reddit"
file_name += ".p"
file_object = open(file_name,"wb")
pickle.dump(classifier,file_object)
file_object.close()

print()
choice = input("View test info? [y/n] ")
if choice == "n":
    sys.exit(0)
    
print("Most important features")

print("grams:")
coeff = vec.inverse_transform(classifier.coef_)[0]
largest = heapq.nlargest(50, coeff, key=coeff.get)
smallest = heapq.nsmallest(50, coeff, key=coeff.get)
for j in range(50):
    print(largest[j], coeff[largest[j]])
for j in range(50):
    print(smallest[j], coeff[smallest[j]])
    
print()

print("Sentiment:")
print("VADER positive", coeff["COMMENT VADER positive"])
print("VADER positive 1/2", coeff["COMMENT VADER positive 1/2"])
print("VADER positive 2/2", coeff["COMMENT VADER positive 2/2"])
print("VADER positive 1/3", coeff["COMMENT VADER positive 1/3"])
print("VADER positive 2/3", coeff["COMMENT VADER positive 2/3"])
print("VADER positive 3/3", coeff["COMMENT VADER positive 3/3"])
print("VADER negative", coeff["COMMENT VADER negative"])
print("VADER negative 1/2", coeff["COMMENT VADER negative 1/2"])
print("VADER negative 2/2", coeff["COMMENT VADER negative 2/2"])
print("VADER negative 1/3", coeff["COMMENT VADER negative 1/3"])
print("VADER negative 2/3", coeff["COMMENT VADER negative 2/3"])
print("VADER negative 3/3", coeff["COMMENT VADER negative 3/3"])

print("SentiWordNet sentiment", coeff["COMMENT Sentiment"])
print("Subjectivity", coeff["COMMENT Subjectivity"])
print("SentiWordNet sentiment 1/2", coeff["COMMENT Sentiment 1/2"])
print("SentiWordNet sentiment 2/2", coeff["COMMENT Sentiment 2/2"])
print("Subjectivity 1/2", coeff["COMMENT Subjectivity 1/2"])
print("Subjectivity 2/2", coeff["COMMENT Subjectivity 2/2"])
print("SentiWordNet sentiment 1/3", coeff["COMMENT Sentiment 1/3"])
print("SentiWordNet sentiment 2/3", coeff["COMMENT Sentiment 2/3"])
print("SentiWordNet sentiment 3/3", coeff["COMMENT Sentiment 3/3"])
print("Subjectivity 1/3", coeff["COMMENT Subjectivity 1/3"])
print("Subjectivity 2/3", coeff["COMMENT Subjectivity 2/3"])
print("Subjectivity 3/3", coeff["COMMENT Subjectivity 3/3"])

if include_reddit:
    print("Comment/subreddit contrast", coeff["Comment/Subreddit contrast"])
    print("Comment/subreddit VADER contrast", coeff["Comment/Subreddit VADER contrast"])
    print("Comment/parent contrast", coeff["Comment/Parent contrast"])
    print("Comment/parent VADER contrast", coeff["Comment/Parent VADER contrast"])

print()

print("topics:")
topics_tag = []
topics_coeff = []
topics_num = []
for j in range(200):
    try:
        topics_tag.append("Topic :" + str(j))
        topics_coeff.append(coeff[topics_tag[j]])
        topics_num.append(j)
    except (KeyError, IndexError):
        continue
topics_tag = np.array(topics_tag)
topics_num = np.array(topics_num)
topics_coeff = np.array(topics_coeff)

topics_num = topics_num[topics_coeff.argsort()]
topics_tag = topics_tag[topics_coeff.argsort()]
topics_coeff = topics_coeff[topics_coeff.argsort()]
for j in range(10):
    try:
        print(topics_coeff[j], topic_mod.get_topic(topics_num[j]))
    except (KeyError, IndexError):
        continue
for j in range(190,200):
    try:
        print(topics_coeff[j], topic_mod.get_topic(topics_num[j]))
    except (KeyError, IndexError):
        continue
        
print("Validating")
output = classifier.predict(testvec)
print(classification_report(test_targets, output, target_names=labels))
        
        
        

