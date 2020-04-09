import os
import pandas as pd

df = pd.read_excel(os.path.join(os.path.dirname(__file__),"../..", "Detecting Sarcasm in Reddit Comments (Responses).xlsx"))

tp = 0
fp = 0
tn = 0
fn = 0
i = 0
for (column, data) in df.iteritems():
    if i % 4 == 0:
        truth = column.split(".")[0]
        for entry in data:
            if entry == "Sarcastic" and truth == "Sarcastic":
                tp += 1
            elif entry == "Sarcastic" and truth == "Not sarcastic":
                fp += 1
            elif entry == "Not sarcastic" and truth == "Sarcastic":
                fn += 1
            elif entry == "Not sarcastic" and truth == "Not sarcastic":
                tn += 1
        
    i += 1

precision = tp / (tp+fp)
recall = tp / (tp+fn)

f1 = 2 * ((precision * recall) / (precision + recall))

print("Sarcastic:")
print("Precision:",precision)
print("Recall:",recall)
print("F1 score:",f1)