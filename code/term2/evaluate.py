import numpy as np
import pickle
import os
import feature_extract
import topic

vecpath = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "vecdict_9192_reddit.p"), "rb")
classifpath = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "lr_9192_reddit.p"), "rb")

vec = pickle.load(vecpath)
classifier = pickle.load(classifpath)

vecpath.close()
classifpath.close()

topic_mod = topic.topic(model = os.path.join(os.path.dirname(os.path.realpath(__file__)), "topics.tp"),\
                        dicttp = os.path.join(os.path.dirname(os.path.realpath(__file__)), "topics_dict.tp"))
                        
def score(comment):
    features = feature_extract.extract_features(comment, topic_mod, True)
    features_vec = vec.transform(features)
    print("Prediction: ",classifier.predict(features_vec))
    score = classifier.decision_function(features_vec)[0]
    percentage = int(round(2.0*(2.0/(1.0+np.exp(-score))-0.5)*100.0))
    
    return percentage