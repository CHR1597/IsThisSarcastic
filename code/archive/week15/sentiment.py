import json
import nltk
import random
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

folder = r"C:\Users\Chris\Documents\Final Year Project"

if __name__ == "__main__":

    train_comments = {}
    test_comments = {}
    
    all_words = ""
    
    with open(folder+r"\train-comments.json") as f:
        train_comments = json.loads(f.read())
       
    with open(folder+r"\test-comments.json") as f:
        test_comments = json.loads(f.read())
        
        
    train_features = []
    train_labels = []
    test_features = []
    test_labels = []
    
    for k,v in train_comments.items():
        if "text" in v:
            train_features.append(v.get("text"))
            train_labels.append(v.get("marker"))
    
    for k,v in test_comments.items():
        if "text" in v:
            test_features.append(v.get("text"))
            test_labels.append(v.get("marker"))

    
    train_features = map(lambda s: re.sub('[^a-zA-Z]', '', s), train_features)
    test_features = map(lambda s: re.sub('[^a-zA-Z]', '', s), test_features)
    print("Comments read...")
    
    ps = PorterStemmer()
    
    train_features = map(lambda s: s.split(), train_features)
    train_features = map(lambda s: ' '.join([ps.stem(word) for word in s]), train_features)
    
    test_features = map(lambda s: s.split(), test_features)
    test_features = map(lambda s: ' '.join([ps.stem(word) for word in s]), test_features)
    print("Comments stemmed...")
    
    tv = TfidfVectorizer(max_features = 5000)
    train_features = tv.fit_transform(train_features)
    test_features = tv.fit_transform(test_features)
    print("tf-idf vectors created...")
    
    # i = 0
    # print("20 random comments:")
    # while i < 20:
        # key = random.choice(list(test_comments.keys()))
        # if "text" not in test_comments[key] or test_comments[key]["parent"] == "" or len(test_comments[key]["parent"].split(" ")) != 1:
            # continue
        # print("key:",key)
        # print("text:",test_comments[key]["text"])
        # print("subreddit:",test_comments[key]["subreddit"])
        # print("score:",test_comments[key]["score"])
        # print("sarcasm:",test_comments[key]["marker"])
        # parent = test_comments[key]["parent"]
        # print("parent:",test_comments[parent]["text"])
        # i += 1
        # print()
        
    input("Press enter to continue.")
    print()
    
    # All models return accuracy
    print("Model 1: Linear support vector classifier")
    lsvc = LinearSVC()
    lsvc.fit(train_features, train_labels)
    print("LSVC training:",lsvc.score(train_features, train_labels))
    print("LSVC test:",lsvc.score(test_features, test_labels))
    print()
    
    ## Model 2 does not work as it requires a dense matrix which requires too much memory to construct.
    # print("Model 2: Gaussian Naive Bayes")
    # gnb = GaussianNB()
    # gnb.fit(train_features, train_labels)
    # print("GNB training:",gnb.score(train_features, train_labels))
    # print("GNB test:",gnb.score(test_features, test_labels))
    # print()
    
    print("Model 2: Logistic Regression")
    lr = LogisticRegression(solver="lbfgs", multi_class="auto")
    lr.fit(train_features, train_labels)
    print("LR training:",lr.score(train_features,train_labels))
    print("LR test:",lr.score(test_features,test_labels))
    print()
    
    print("Model 3: Random Forest Classifier")
    rfc = RandomForestClassifier(n_estimators = 10, random_state = 0)
    rfc.fit(train_features,train_labels)
    print("RFC training:",rfc.score(train_features,train_labels))
    print("RFC test:",rfc.score(test_features,test_labels))
    print()
    
    # stop_words = set(stopwords.words("english"))
    # tokens = word_tokenize(all_words)
    
    # print("Comments tokenized...")
    
    # filtered = [t.lower() for t in tokens if not t.lower() in stop_words]
    # filtered = [t.lower() for t in filtered if t.isalpha()]
    
    # print("Comments filtered...")
    
    # wordcount = {}
    # for word in filtered:
        # if word not in wordcount:
            # wordcount[word] = 1
        # else:
            # wordcount[word] += 1
            
    # for word in wordcount:
        # if wordcount[word] >= 1000:
            # print("'",word,"' appears ",wordcount[word]," times",sep="")