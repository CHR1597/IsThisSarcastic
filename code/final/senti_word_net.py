"""Set up functions for WordNet and SentiWordNet.

Classes:
senti_word_net -- The class handling these functions.
"""

import csv, collections, os
import nltk
import numpy as np

folder = os.path.join(os.path.dirname(__file__),"../..")

"""Perform operations for SentiWordNet.

This class handles operations relating to SentiWordNet, a project that assigns a
sentiment score to every word in WordNet.

Methods:
__init__       -- Constructor for the class.
score_word     -- Score a single word.
score_sentence -- Score a sentence.
score          -- Calculate the score for a word.
posvector      -- Tally the parts of speech present in a sentence.
"""
class senti_word_net(object):

    """Constructor for the class.
    
    The class is initialised by reading the SentiWordNet file and setting up a local dictionary
    mapping words to sentiment scores.
    """
    def __init__(self):
        sent_scores = collections.defaultdict(list)
        
        with open(os.path.join(folder,"SentiWordNet_3.0.0.txt"), "r") as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            
            for line in reader:
                if line[0].startswith("#"):
                    continue
                if len(line) == 1:
                    continue
                    
                POS, ID, PosScore, NegScore, SynsetTerms, Gloss = line
                
                if len(POS) == 0 or len(ID) == 0:
                    continue
                
                for term in SynsetTerms.split(" "):
                    term = term.split("#")[0]
                    term = term.replace("-", " ").replace("_", " ")
                    key = "%s/%s"%(POS, term.split("#")[0])
                    sent_scores[key].append((float(PosScore),float(NegScore)))
                    
        for key, value in sent_scores.items():
            sent_scores[key] = np.mean(value,axis=0)
            
        self.sent_scores = sent_scores
        
    """Score a single word.
    
    Arguments:
    word -- The word to be scored.
    
    Returns:
    The sentiment score for that word.
    """
    def score_word(self, word):
        pos = nltk.pos_tag([word])[0][1]
        return self.score(word,pos)
        
    """Score a sentence.
    
    Arguments:
    sentence -- The sentence to be scored.
    
    Returns:
    mean_score -- The average score of the sentence based on each word.
    """
    def score_sentence(self, sentence):
        pos = nltk.pos_tag(sentence)
        mean_score = np.array([0.0,0.0])
        for j in range(len(pos)):
            mean_score += self.score(pos[j][0],pos[j][1])
            
        return mean_score
        
    """Calculate the score for a word.
    
    Arguments:
    word -- The word itself.
    pos  -- The part of speech for that word - for possible ambiguities.
    
    Returns:
    The positive and negative sentiment score for that word in the dictionary, or zeroes if not present.
    """
    def score(self, word, pos):
        if pos[0:2] == "NN":
            pos_type = "n"
        elif pos[0:2] == "JJ":
            pos_type = "a"
        elif pos[0:2] == "VB":
            pos_type = "v"
        elif pos[0:2] == "RB":
            pos_type = "r"
        else:
            pos_type = 0
            
        if pos_type != 0:
            dic_loc = pos_type+"/"+word
            pos_neg_scores = self.sent_scores[dic_loc]
            if len(pos_neg_scores) == 2:
                return pos_neg_scores
            else:
                return np.array([0.0,0.0])
        else:
            return np.array([0.0,0.0])
    
    """Tally the parts of speech present in a sentence.
    
    Arguments:
    sentence -- The sentence in question.
    
    Returns:
    vector -- The count of nouns, adjectives, verbs, and adverbs in the sentence.
    """
    def posvector(self, sentence):
        pos_vector = nltk.pos_tag(sentence)
        vector = np.zeros(4)
        
        for j in range(len(sentence)):
            pos = pos_vector[j][1]
            if pos[0:2] == "NN":
                vector[0] += 1
            elif pos[0:2] == "JJ":
                vector[1] += 1
            elif pos[0:2] == "VB":
                vector[2] += 1
            elif pos[0:2] == "RB":
                vector[3] += 1
                
        return vector