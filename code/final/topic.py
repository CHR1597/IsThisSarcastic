"""A wrapper for the Gensim topic modeller.

Classes:
topic -- Generates and saves topic modeller and provides operations on it.
"""

from gensim import corpora, models, similarities
import numpy as np
import nltk
import expr_replace
from nltk.corpus import stopwords

"""Perform operations relating to topics of text.

Methods:
__init__  -- Constructor for the class.
fit       -- Save an LDA topic modeller for the dataset.
get_topic -- Get details of a topic by number.
transform -- Get topics present in a sentence.
"""
class topic(object):

    """Constructor for the class.
    
    Arguments:
    nbtopic -- Number of topics to be represented in the modeller.
    alpha   -- The alpha parameter for the LDA representation.
    model   -- A saved representation of a previous model.
    dicttp  -- A saved representation of a previous dictionary.
    """
    def __init__(self, nbtopic=100, alpha=1, model=None, dicttp=None):
        self.nbtopic = nbtopic
        self.porter = nltk.PorterStemmer()
        self.alpha = alpha
        self.stop = stopwords.words("english")+[".","!","?",'"',"...","\\","''","[","]","~","'m","'s",";",":","..","$"]
        if model != None and dicttp != None:
            self.lda = models.ldamodel.LdaModel.load(model)
            self.dictionary = corpora.Dictionary.load(dicttp)
    
    """Save an LDA topic modeller for the dataset.
    
    Arguments:
    documents -- Data to be used for generating the topic modeller.
    """
    def fit(self, documents):
        documents_mod = [expr_replace.replace_general(sentence) for sentence in documents]
        tokens = [nltk.word_tokenize(sentence) for sentence in documents_mod]
        tokens = [[self.porter.stem(t.lower()) for t in sentence if t.lower() not in self.stop] for sentence in tokens]
        
        self.dictionary = corpora.Dictionary(tokens)
        corpus = [self.dictionary.doc2bow(text) for text in tokens]
        self.lda = models.ldamodel.LdaModel(corpus, id2word=self.dictionary, num_topics = self.nbtopic, alpha = self.alpha)
        
        self.lda.save("topics.tp")
        self.dictionary.save("topics_dict.tp")
    
    """Get details of a topic by number.
    
    Arguments:
    topic_number -- The number of the topic to be retrieved.
    
    Returns:
    The information about that topic in the saved model.
    """
    def get_topic(self, topic_number):
        return self.lda.print_topic(topic_number)
    
    """Get topics present in a sentence.
    
    Arguments:
    sentence -- The sentence to be analysed.
    
    Returns:
    The topics present in the given sentence.
    """
    def transform(self, sentence):
        sentence_mod = expr_replace.replace_general(sentence)
        tokens = nltk.word_tokenize(sentence_mod)
        tokens = [self.porter.stem(t.lower()) for t in sentence if t.lower() not in self.stop]
        corpus_sentence = self.dictionary.doc2bow(tokens)
        return self.lda[corpus_sentence]