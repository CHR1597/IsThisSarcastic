import os
import random
import json
import numpy as np
import feature_extract
import topic

folder = os.path.join(os.path.dirname(__file__),"../..")

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
    print(i, "sarcastic comments processed...", end="\r")
    featuresets.append((feature_extract.extract_features(v, topic_mod), labels[0]))
    i += 1
    
print()
i = 1
for k,v in nonsarcs.items():
    print(i, "non-sarcastic comments processed...", end="\r")
    featuresets.append((feature_extract.extract_features(v, topic_mod), labels[1]))
    i += 1