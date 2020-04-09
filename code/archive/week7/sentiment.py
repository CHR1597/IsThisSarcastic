import json
import nltk
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

folder = r"C:\Users\Chris\Documents\Final Year Project"

if __name__ == "__main__":

    train_comments = {}
    test_comments = {}
    
    all_words = ""
    
    with open(folder+r"\train-comments.json") as f:
        train_comments = json.loads(f.read())
       
    with open(folder+r"\test-comments.json") as f:
        test_comments = json.loads(f.read())
        
    for k,v in train_comments.items():
        if v.get("marker") == "1" and len(v.get("parent").split(" ")) == 1:
            all_words += v.get("text") + " "
            
            
           
    print("Comments read...")
    
    i = 0
    print("20 random comments:")
    while i < 20:
        key = random.choice(list(test_comments.keys()))
        if "text" not in test_comments[key] or test_comments[key]["parent"] == "" or len(test_comments[key]["parent"].split(" ")) != 1:
            continue
        print("key:",key)
        print("text:",test_comments[key]["text"])
        print("subreddit:",test_comments[key]["subreddit"])
        print("score:",test_comments[key]["score"])
        print("sarcasm:",test_comments[key]["marker"])
        parent = test_comments[key]["parent"]
        print("parent:",test_comments[parent]["text"])
        i += 1
        print()
        
    input("Press enter to continue.")
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(all_words)
    
    print("Comments tokenized...")
    
    filtered = [t.lower() for t in tokens if not t.lower() in stop_words]
    filtered = [t.lower() for t in filtered if t.isalpha()]
    
    print("Comments filtered...")
    
    wordcount = {}
    for word in filtered:
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
            
    for word in wordcount:
        if wordcount[word] >= 1000:
            print("'",word,"' appears ",wordcount[word]," times",sep="")