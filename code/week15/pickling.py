import pickle
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__ == "__main__":
    vectorizer = TfidfVectorizer()
    lsvc = LinearSVC()
    pickle.dump(vectorizer, open("vect.p","wb"))
    pickle.dump(lsvc, open("classifier.p","wb"))