import praw

reddit = praw.Reddit("project1")
                     
# subreddit = reddit.subreddit("formula1")
comment = reddit.comment("fen1xjn")

print(comment.body)
print(comment.author.name)
print(comment.submission.title)
# print(subreddit.title)
# print(subreddit.description)