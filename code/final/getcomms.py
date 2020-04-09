import json
import socket
import os
import praw
import prawcore

folder = os.path.join(os.path.dirname(__file__),"../..")


if __name__ == "__main__":
    new_train = {}
    new_test = {}
    parents = {}
    orig_train = {}
    orig_test = {}
    log = []
    
    reddit = praw.Reddit("project1")
    
    with open(os.path.join(folder,"train-comments.json")) as f:
        orig_train = json.loads(f.read())
        
    with open(os.path.join(folder,"test-comments.json")) as f:
        orig_test = json.loads(f.read())
        
    with open(os.path.join(folder,"train-comments-new.json")) as f:
        new_train = json.loads(f.read())
        
    with open(os.path.join(folder,"test-comments-new.json")) as f:
        new_test = json.loads(f.read())
        
    i = 1
    try:
        for k,v in orig_train.items():
            print(i, "comments read...",end="\r")
            if k in new_train:
                i += 1
                continue
                
            if "text" in v and v.get("parent") != "" and len(v.get("parent").split(" ")) == 1:
                
                try:
                    sub = reddit.subreddit(v.get("subreddit"))
                    parent = reddit.submission(id=v.get("parent"))
                    
                    v["description"] = sub.public_description
                    v["parent_title"] = parent.title
                    
                    new_train[k] = v
                    i += 1
                    
                except prawcore.exceptions.NotFound:
                    log.append("Comment " + str(i) + " returned not found")
                    i += 1
                    continue
                    
                except prawcore.exceptions.Forbidden:
                    log.append("Comment " + str(i) + " returned forbidden")
                    try:
                        sub.quaran.opt_in()
                    
                        v["description"] = sub.public_description
                        v["parent_title"] = parent.title
                        
                        new_train[k] = v
                        i += 1
                        
                    except prawcore.exceptions.Forbidden:
                        log.append("Comment " + str(i) + " remains forbidden. Skipping.")
                        i += 1
                        continue
                    
                    
        for k,v in orig_test.items():
            print(i, "comments read...",end="\r")
            if k in new_test:
                i += 1
                continue
                
            if "text" in v and v.get("parent") != "" and len(v.get("parent").split(" ")) == 1:
                
                try:
                    sub = reddit.subreddit(v.get("subreddit"))
                    parent = reddit.submission(id=v.get("parent"))
                    
                    v["description"] = sub.public_description
                    v["parent_title"] = parent.title
                    
                    new_test[k] = v
                    i += 1
                    
                except prawcore.exceptions.NotFound:
                    log.append("Comment " + str(i) + " returned not found")
                    i += 1
                    continue
                    
                except prawcore.exceptions.Forbidden:
                    log.append("Comment " + str(i) + " returned forbidden")
                    try:
                        sub.quaran.opt_in()
                    
                        v["description"] = sub.public_description
                        v["parent_title"] = parent.title
                        
                        new_test[k] = v
                        i += 1
                        
                    except prawcore.exceptions.Forbidden:
                        log.append("Comment " + str(i) + " remains forbidden. Skipping.")
                        i += 1
                        continue
                
        print()
        print("All comments read. Writing to file")
    
    except KeyboardInterrupt:
        print()
        print("Exiting...")
    
    except socket.timeout:
        print()
        print("Socket timed out.")
    
    finally:
        train_json = json.dumps(new_train)
        test_json = json.dumps(new_test)
        parent_json = json.dumps(parents)
        
        f = open(os.path.join(folder,"train-comments-new.json"),"w")
        f.write(train_json)
        f.close()
        g = open(os.path.join(folder,"test-comments-new.json"),"w")
        g.write(test_json)
        g.close()
        h = open(os.path.join(folder,"parents.json"),"w")
        h.write(parent_json)
        h.close()
        with open(os.path.join(folder,"comment-logs.txt"),"w") as e:
            for item in log:
                e.write(item + "\n")
    
        print("Done")