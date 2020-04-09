"""Preprocess the comment data in preparation for training.

This file removes comments from the final dataset if they are empty or contain web links or non-Unicode
characters. It also removes subreddits, usernames, hashtags, sarcasm tags, and mentions of sarcasm from
all comments.
"""

import os
import json
import numpy as np
import re
from textblob import TextBlob

folder = os.path.join(os.path.dirname(__file__),"../..")

"""Process full comment data.

Arguments:
dict_obj -- The dictionary object of full comment data.

Returns:
newdict -- The dictionary made of only valid comments with text that would confuse the classifier removed.
data    -- A numpy array of comment text for use with the topic modeller.
length  -- The number of words in the final set of comment data.
"""
def preprocess(dict_obj):
    
    
    newdict = {}    # Dictionary will be altered during preprocessing and saved here - required for feature extraction
    data = []       # Array will be converted to numpy array for topic modeller
    length = []
    remove_subreddit = re.compile(r"/?r/\w+\s?")
    remove_user_mention = re.compile(r"/?u/\w+\s?")
    remove_hashtags = re.compile(r"#\w+\s?")  # Hashtags have no purpose on Reddit but some users use them anyway to ironically invoke a Twitter-style comment
    remove_sarctag = re.compile(r"\s+/s\b")
    remove_sarcasm = re.compile(re.escape("sarcasm"),re.IGNORECASE)
    remove_sarcastic = re.compile(re.escape("sarcastic"),re.IGNORECASE)
    
    for k,v in dict_obj.items():
        temp = v.get("text")
        temp = remove_sarctag.sub("",temp)
        if len(temp) > 0 and "http" not in temp and "\\u" not in temp and len(v.get("parent").split()) == 1:
            temp = remove_subreddit.sub("",temp)
            temp = remove_user_mention.sub("",temp)
            temp = remove_hashtags.sub("",temp)
            temp = remove_sarcasm.sub("",temp)
            temp = remove_sarcastic.sub("",temp)
            temp = " ".join(temp.split())
            if len(temp.split()) > 2:
                data.append(temp)
                newdict[k] = v
                newdict[k]["text"] = temp
                length.append(len(temp.split()))
             
            
    
    data = list(set(data))
    data = np.array(data)
    
    return newdict,data,length
    
dict_obj_sarc = json.loads(open(os.path.join(folder,"sarc-comments.json"),"r").read())
sarc_dict, sarc_data, sarc_length = preprocess(dict_obj_sarc)

dict_obj_non = json.loads(open(os.path.join(folder,"nonsarc-comments.json"),"r").read())
non_dict, non_data, non_length = preprocess(dict_obj_non)

print("Number of sarcastic comments:",len(sarc_data))
print("Average length of sarcastic comments:",np.mean(sarc_length))
print("Number of non-sarcastic comments:",len(non_data))
print("Average length of non-sarcastic comments:",np.mean(non_length))

sarc_json = json.dumps(sarc_dict)
non_json = json.dumps(non_dict)
f = open(os.path.join(folder,"sarc-comments.json"),"w")
f.write(sarc_json)
f.close()
g = open(os.path.join(folder,"nonsarc-comments.json"),"w")
g.write(non_json)
g.close()

np.save("sarc-processed",sarc_data)
np.save("nonsarc-processed",non_data)