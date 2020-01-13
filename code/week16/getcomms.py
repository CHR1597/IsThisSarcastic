import json

folder = r"C:\Users\Chris\Documents\Final Year Project"


if __name__ == "__main__":
    sarc_comments = {}
    nonsarc_comments = {}
    orig_train = {}
    orig_test = {}
    
    with open(folder+r"\train-comments.json") as f:
        orig_train = json.loads(f.read())
        
    with open(folder+r"\test-comments.json") as f:
        orig_test = json.loads(f.read())
        
    print("Comments read...")
    
    i = 0
    for k,v in orig_train.items():
        if i >= 200:
            i = 0
            break
        if "text" in v and "marker" in v:
            if v.get("marker") == "1":
                sarc_comments[k] = v
                i += 1
            else:
                nonsarc_comments[k] = v
                i += 1
                
    print("Training set read...")
                
    for k,v in orig_test.items():
        if i >= 200:
            break
        if "text" in v:
            if v.get("marker") == "1":
                sarc_comments[k] = v
                i += 1
            else:
                nonsarc_comments[k] = v
                i += 1
                
    print("Test set read...")
                
    sarc_json = json.dumps(sarc_comments)
    nonsarc_json = json.dumps(nonsarc_comments)
    
    f = open(folder+r"\sarc-comments.json","w")
    f.write(sarc_json)
    f.close()
    g = open(folder+r"\nonsarc-comments.json","w")
    g.write(nonsarc_json)
    g.close()
    
    print("Done")