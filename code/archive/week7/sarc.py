import ijson
import json
import csv

folder = r"C:\Users\Chris\Documents\Final Year Project"

if __name__ == '__main__':

    
    
    train_comments = {}
    test_comments = {}
    
    attributes = ["text","score","subreddit"]
    
    with open(folder+r"\SARC\main\train-balanced.csv",'r') as g:
        reader = csv.reader(g, delimiter='|')
        for row in reader:
            response = row[1].split(" ")
            marker = row[2].split(" ")
            train_comments[row[0]] = {}
            train_comments[row[0]]["parent"] = ""
            train_comments[row[0]]["marker"] = ""
            for res,mark in zip(response,marker):
                train_comments[res] = {}
                train_comments[res]["parent"] = row[0]
                train_comments[res]["marker"] = mark

    with open(folder+r"\SARC\main\test-balanced.csv",'r') as g:
        reader = csv.reader(g, delimiter='|')
        for row in reader:
            response = row[1].split(" ")
            marker = row[2].split(" ")
            test_comments[row[0]] = {}
            test_comments[row[0]]["parent"] = ""
            test_comments[row[0]]["marker"] = ""
            for res,mark in zip(response,marker):
                test_comments[res] = {}
                test_comments[res]["parent"] = row[0]
                test_comments[res]["marker"] = mark
    
    i = 1;
    with open(folder+r"\SARC\main\comments.json",'r') as f:
        parser = ijson.parse(f)
        for prefix, event, value in parser:
            print(i,"lines read...",end='\r')
            alt = prefix.split(".")
            if len(alt) > 1:
                if alt[0] in train_comments and alt[1] in attributes:
                    #print()
                    #print(alt[0],alt[1])
                    train_comments[alt[0]][alt[1]] = value
                    #print()
                    #print(prefix,":",value)
                    #print()
                elif alt[0] in test_comments and alt[1] in attributes:
                    test_comments[alt[0]][alt[1]] = value
            i += 1
            #if i == 231100:
                #break
            
             
    print()
    train_json = json.dumps(train_comments)
    test_json = json.dumps(test_comments)
    f = open(folder+r"\train-comments.json",'w')
    f.write(train_json)
    f.close()
    g = open(folder+r"\test-comments.json",'w')
    g.write(test_json)
    g.close()
    
    print("Done.")
      
    ##with open(folder+r"\SARC\main\comments.json",'r') as f:
    ##    parser = ijson.parse(f)
    ##    for prefix, event, value in parser:
            ##if "." in prefix:
            ##    sub = prefix.split(".")
            ##    if sub[1] == "subreddit":
            ##        print(i, ". ", value,sep="")
            ##        i += 1
            ##        if i > 500:
            ##            break

        # Prints entire structure
        ##parser = ijson.parse(f)
        ##for prefix, event, value in parser:
        ##    print('prefix={}, event={}, value={}'.format(prefix, event, value))

        # Gets specific item - loops through entire file on every run so not ideal.
        ##for row in originals:
        ##    item = ijson.items(row)
        ##    for s in item:
        ##        print(s["subreddit"])
        
