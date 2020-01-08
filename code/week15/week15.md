# Christmas Holidays Log
## Results of first marker meeting
- After meeting with Alan at the end of term, focus was on combining ideas into a realistic product
- Problems brought up included a lack of familiarity with machine learning concepts and sklearn implementations.
- After returning to the research stage I discovered http://www.thesarcasmdetector.com/ - an open-source Twitter-based sarcasm detector. This project provided great insight into how I should realistically structure my product.
- Inspired by this project, mine will now work as follows:
    - Use `gensim` library to model topics
    - Use custom feature-extraction code using `nltk` and `VADER` to generate a dictionary of features using n-grams, sentiment analysis, parts of speech, topics, etc.
    - One part of this will use the Reddit API to access the details of the comment in question (subreddit, score, etc.) to add details to the dictionary e.g. agrees with consensus, controversial
    - Use this dictionary to create a TF-IDF vector which can be passed into an `sklearn` classifier (linear support vector, naive Bayes, logistic regression)
- This will generate a model that can be used on any new Reddit comment (or sentence only, in the appropriate mode)

## Stretch goals
If this proves to be doable within a reasonable timeframe, I will also design a web application to use this model to predict the sarcasm of any given sentence. The site will allow a user to provide a Reddit link (thereby providing the model with comment metadata), or simply type a phrase.