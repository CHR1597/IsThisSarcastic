import senti_test
import nltk

sentiment = senti_test.senti_word_net()

mystr = ""
while True:
    mystr = input("Enter sentence: ")
    if mystr == "exit":
        break
    mystr = nltk.word_tokenize(mystr)
    mystr = [(w.lower()) for w in mystr]
    
    mean_sentiment = sentiment.score_sentence(mystr)
    print("Positive sentiment:",mean_sentiment[0])
    print("Negative sentiment:",mean_sentiment[1])
    print("Overall sentiment:",mean_sentiment[0]-mean_sentiment[1])