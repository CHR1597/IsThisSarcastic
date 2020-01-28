import json
import os
import praw

folder = os.path.join(os.path.dirname(__file__),"../..")


if __name__ == "__main__":
    sarc_comments = {}
    nonsarc_comments = {}
    parents = {}
    orig_train = {}
    orig_test = {}
    
    reddit = praw.Reddit("project1")
    
    with open(os.path.join(folder,"train-comments.json")) as f:
        orig_train = json.loads(f.read())
        
    with open(os.path.join(folder,"test-comments.json")) as f:
        orig_test = json.loads(f.read())
        
    
    i = 1
    for k,v in orig_train.items():
        print(i, "comments read...",end="\r")
        if "text" in v and v.get("parent") != "" and len(v.get("parent").split(" ")) == 1:
            
            sub = reddit.subreddit(v.get("subreddit"))
            parent = reddit.submission(id=v.get("parent"))
            
            v["description"] = sub.public_description
            v["parent_title"] = parent.title
            
            if v.get("marker") == "1":
                sarc_comments[k] = v
                i += 1
            elif v.get("marker") == "0":
                nonsarc_comments[k] = v
                i += 1
            else:
                parents[k] = v
                i += 1
                
                
    for k,v in orig_test.items():
        print(i, "comments read...", end="\r")
        if "text" in v and v.get("parent") != "":
        
            sub = reddit.subreddit(v.get("subreddit"))
            parent = reddit.submission(id=v.get("parent"))
            
            v["description"] = sub.public_description
            v["parent_title"] = parent.title
            
            if v.get("marker") == "1":
                sarc_comments[k] = v
                i += 1
            elif v.get("marker") == "0":
                nonsarc_comments[k] = v
                i += 1
            else:
                parents[k] = v
                i += 1
                
    print()
    print("All comments read. Writing to file")
                
    sarc_json = json.dumps(sarc_comments)
    nonsarc_json = json.dumps(nonsarc_comments)
    parent_json = json.dumps(parents)
    
    f = open(os.path.join(folder,"sarc-comments.json"),"w")
    f.write(sarc_json)
    f.close()
    g = open(os.path.join(folder,"nonsarc-comments.json"),"w")
    g.write(nonsarc_json)
    g.close()
    h = open(os.path.join(folder,"parents.json"),"w")
    h.write(parent_json)
    h.close()
    
    print("Done")