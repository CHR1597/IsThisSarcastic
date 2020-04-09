###
This information can also be viewed in Appendix A of the report.
###

This project was developed using Python 3.8.1, and requires the following optional packages (run `pip install <name>`):
• gensim
• nltk
• numpy
• praw
• textblob
• vaderSentiment
Generating new classifiers also requires the libraries scipy and sklearn.

A file titled praw.ini is required for the PRAW library to log into Reddit as a specific user. As mentioned in section 3.5, the Reddit API requires any application that uses it to register with Reddit using OAuth2. As such, running this program requires a Reddit account to which any comments will
be posted. When the application has been registered with Reddit, you will be given a client ID and client secret. Once you have this information, the praw.ini file should be made to this specification:

[project2]
client_id = <Client ID>
client_secret = <Client Secret>
user_agent = <User agent string>
username = <Account username>
password = <Account password>

With praw.ini in the code/final directory, run detector.py from the same directory. When the console reads "Ready.", replying to a Reddit comment with the username of the connected account will prompt the bot to reply. Adding a link to another Reddit comment will prompt it to analyse the linked comment instead.

To generate a new classifier, run:
`train.py <include reddit> <classifier type>`
where <include reddit> is 0 or 1 to indicate whether Reddit context should be included, and <classifier type> is 1 or 2, indicating a LinearSVC or Logistic Regression model respectively.