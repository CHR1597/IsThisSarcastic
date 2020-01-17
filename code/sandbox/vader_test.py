from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print(score)
    
mystr = ""
while mystr != "exit":
    mystr = input("Enter sentence: ")
    sentiment_analyzer_scores(mystr)