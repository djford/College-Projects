
term = "monkey"
docID = 56
position = 2;

index = dict()
if term not in index:
    index[term] = dict()
if docID not in index[term]:
    index[term][docID] = list()
index[term][docID].append(position)



print(index["monkey"])