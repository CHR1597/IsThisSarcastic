import ijson
import csv

folder = r"C:\Users\Chris\Documents\Final Year Project"

if __name__ == '__main__':

    i = 0;
    originals = []
    with open(folder+r"\SARC\main\train-balanced.csv",'r') as g:
        reader = csv.reader(g, delimiter='|')
        for row in reader:
            originals.append(row[0])

    for row in originals:
        print(row)
      
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
        
