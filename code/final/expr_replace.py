"""Replace emoticons with textual representations and extend abbreviations."""

import nltk
import re

# Dictionary for sentiment analysis replacement
emotion_replace = {
    "<3" : " good ",
    ":d" : " good ",
    ":p" : " good ",
    "8)" : " good ",
    ":)" : " good ",
    ":-)" : " good ",
    "(:" : " good ",
    "(-:" : " good ",
    ";)" : " good ",
    
    ":/" : " bad ",
    ":(" : " bad ",
    ":-(" : " bad ",
    ":s" : " bad ",
    ":@" : " bad "
}

# Dictionary for general replacements
emotion_replace2 = {
    "<3" : " heart ",
    ":d" : " smile ",
    ":p" : " smile ",
    "8)" : " smile ",
    ":)" : " smile ",
    ":-)" : " smile ",
    "(:" : " smile ",
    "(-:" : " smile ",
    ";)" : " smile ",
    
    ":/" : " worry ",
    ":(" : " sad ",
    ":-(" : " sad ",
    ":s" : " sad ",
    ":@" : " angry "
}

# General replacements (e.g. abbreviations)
abbr_replace = {
    r"\br\b" : "are",
    r"\bu\b" : "you",
    r"\bha(ha)+\b" : "ha",
    r"\bdon't\b" : "do not",
    r"\bdoesn't\b" : "does not",
    r"\bdidn't\b" : "did not",
    r"\bhasn't\b" : "has not",
    r"\bhaven't\b" : "have not",
    r"\bhadn't\b" : "had not",
    r"\bwon't\b" : "will not",
    r"\bwouldn't\b" : "would not",
    r"\bcan't\b" : "can not",
    r"\bcannot\b" : "can not",
    r"\bcouldn't\b" : "could not",
    r"\bshouldn't\b" : "should not"
}

order_repl = [k for (k_len,k) in reversed(sorted([(len(k),k) for k in emotion_replace.keys()]))]
order_repl2 = [k for (k_len,k) in reversed(sorted([(len(k),k) for k in emotion_replace2.keys()]))]

def replace_emotion(sentence):
    sentence2 = sentence
    for k in order_repl:
        sentence2 = sentence2.replace(k,emotion_replace[k])
    for r, repl in abbr_replace.items():
        sentence2 = re.sub(r,repl,sentence2)
    return sentence2
    
def replace_general(sentence):
    sentence2 = sentence
    for k in order_repl2:
        sentence2 = sentence2.replace(k, emotion_replace2[k])
    for r, repl in abbr_replace.items():
        sentence2 = re.sub(r,repl,sentence2)
    return sentence2