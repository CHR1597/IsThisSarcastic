"""Evaluate whether an arbitrary Reddit comment is sarcastic using the saved classifier and feature vector.

Functions:
score -- Classify a comment as sarcastic or not.
"""

import numpy as np
import pickle
import os
import feature_extract
import topic

vecpath = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "vecdict_45652_reddit.p"), "rb")
classifpath = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "lr_45652_reddit.p"), "rb")

vec = pickle.load(vecpath)
classifier = pickle.load(classifpath)

vecpath.close()
classifpath.close()

topic_mod = topic.topic(model = os.path.join(os.path.dirname(os.path.realpath(__file__)), "topics.tp"),\
                        dicttp = os.path.join(os.path.dirname(os.path.realpath(__file__)), "topics_dict.tp"))

"""Classify a comment as sarcastic or not.

Arguments:
comment -- The dictionary format for the comment to be scored.
"""                        
def score(comment):
    features = feature_extract.extract_features(comment, topic_mod, True)
    features_vec = vec.transform(features)
    print("Prediction: ",classifier.predict(features_vec))
    score = classifier.decision_function(features_vec)[0]
    
    return score