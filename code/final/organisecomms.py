import json
import os

folder = os.path.join(os.path.dirname(__file__),"../..")


if __name__ == "__main__":
    sarc_comments = {}
    nonsarc_comments = {}
    parents = {}
    orig_train = {}
    orig_test = {}
    
    with open(os.path.join(folder,"train-comments-new.json")) as f:
        orig_train = json.loads(f.read())
        
    with open(os.path.join(folder,"test-comments-new.json")) as f:
        orig_test = json.loads(f.read())
        
    print("Comments read...")
    
    i = 0
    for k,v in orig_train.items():
        if i >= 50000:
            i = 0
            break
        if "text" in v:
            if v.get("marker") == "1":
                sarc_comments[k] = v
                i += 1
            elif v.get("marker") == "0":
                nonsarc_comments[k] = v
                i += 1
            else:
                parents[k] = v
                i += 1
                
    print("Training set read...")
                
    # for k,v in orig_test.items():
        # if i >= 300:
            # break
        # if "text" in v:
            # if v.get("marker") == "1":
                # sarc_comments[k] = v
                # i += 1
            # elif v.get("marker") == "0":
                # nonsarc_comments[k] = v
                # i += 1
            # else:
                # parents[k] = v
                # i += 1
                
    # print("Test set read...")
                
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
