import ijson
import csv

folder = r"C:\Users\Chris\Documents\Final Year Project"

if __name__ == '__main__':

    
    originals = []
    responses = []
    markers = []
    with open(folder+r"\SARC\main\train-balanced.csv",'r') as g:
        reader = csv.reader(g, delimiter='|')
        for row in reader:
            originals.append(row[0])
            responses.append(row[1])
            markers.append(row[2])

    for row in responses:
        options = row.split(" ")
        for option in options:
            i = 1;
            print(option)
            with open(folder+r"\SARC\main\comments.json",'r') as f:
                parser = ijson.parse(f)
                for prefix, event, value in parser:
                    print(i,"lines read...",end='\r')
                    alt = prefix.split(".")
                    if len(alt) > 1:
                        if alt[0]==option and alt[1]=="text":
                            print()
                            print(value)
                            input()
                            break;
                    i += 1
      
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
        
