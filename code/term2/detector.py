import praw
import numpy as np
import evaluate

reddit = praw.Reddit("project2")
dict_obj = {}
footer = """\
---
*^I'm ^a ^bot ^for ^detecting ^sarcasm ^in ^Reddit ^comments ^using ^[SARC](https://arxiv.org/abs/1704.05579). ^Created ^by ^/u/CHR1597.*

*^Your ^feedback ^may ^improve ^my ^decision-making ^in ^the ^future. ^Please ^feel ^free ^to ^leave ^your ^comments [^on ^this ^form.](https://forms.gle/R56c1t65ETWp4vMS6)*
"""

mentions = reddit.inbox.mentions
stream = praw.models.util.stream_generator(mentions)
print("Ready.")

try:
    for mention in stream:
        reply = ""
        if mention.new:
            will_reply = True
            try:
                comm = None
                if len(mention.body.split(" ")) == 1 and isinstance(mention.parent(), praw.models.Comment):
                    comm = reddit.comment(mention.parent())
                else:
                    link = mention.body.split(" ")[1]
                    comm = reddit.comment(url=link)
                dict_obj["text"] = comm.body
                dict_obj["score"] = comm.score
                dict_obj["description"] = comm.subreddit.public_description
                dict_obj["parent_title"] = comm.submission.title
                score = evaluate.score(dict_obj)
                abs_score = np.absolute(score)
                abs_score *= 100
                if abs_score > 100:
                    abs_score = 100
                
                if abs_score <= 10:
                    reply += "It's too close to call! My guess is that this comment is "
                    if score < 0:
                        reply += "**not** "
                    reply += "sarcastic."
                elif abs_score > 10 and abs_score <= 25:
                    reply += "It's a very difficult decision, but I think this comment is "
                    if score < 0:
                        reply += "**not** "
                    reply += "sarcastic."
                elif abs_score > 25 and abs_score <= 50:
                    reply += "It's quite a difficult decision, but I think this comment is "
                    if score < 0:
                        reply += "**not** "
                    reply += "sarcastic."
                elif abs_score > 50 and abs_score <= 75:
                    reply += "I'm fairly sure this comment is "
                    if score < 0:
                        reply += "**not** "
                    reply += "sarcastic."
                elif abs_score > 75 and abs_score <= 90:
                    reply += "I'm sure this comment is "
                    if score < 0:
                        reply += "**not** "
                    reply += "sarcastic."
                else:
                    reply += "I'm certain this comment is "
                    if score < 0:
                        reply += "**not** "
                    reply += "sarcastic."
                
                reply += "\n\n(Confidence score: " + "{0:.2f}".format(abs_score) + "%)"
                print("Mention:", mention.body, "\nby:", mention.author)

            
            except (ValueError, praw.exceptions.ClientException):
                will_reply = False
                reddit.redditor("chr1597").message("Comment parse error", mention.body)
                continue
                
            finally:
                reply += "\n\n" + footer
                if will_reply:
                    mention.reply(reply)
                mention.mark_read()
except KeyboardInterrupt:
    print("\nExiting.")