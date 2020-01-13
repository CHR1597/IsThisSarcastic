import json
import numpy as np
import re

folder = r"C:\Users\Chris\Documents\Final Year Project"

def preprocess(dict_obj):
    
    #TODO: save preprocessed text as numpy array for topic modeller and apply that text to the json version for feature extraction
    
    return 1,2
    
dict_obj_sarc = json.loads(open(folder+r"\sarc-comments.json","r").read())
sarc_data, sarc_length = preprocess(dict_obj_sarc)

dict_obj_non = json.loads(open(folder+r"\nonsarc-comments.json","r").read())
non_data, non_length = preprocess(dict_obj_non)