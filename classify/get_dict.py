import json
import os
file = './field2'
dit = {}
for each_file in os.listdir(file):
    with open(file+'/' +each_file,'r',encoding='utf8') as f:
        lst = [i.strip().split('\t')[0] for i in f]
        for a in range(len(lst)-1):
            for b in range(a+1,len(lst)):
                if lst[a] not in dit:
                    dit[lst[a]] = []
                if lst[b] not in dit:
                    dit[lst[b]] = []
                dit[lst[a]].append(lst[b])
                dit[lst[b]].append(lst[a])
for i in dit:
    print(len(set(dit[i])))
    dit[i] = list(set(dit[i]))
with open('dit/'+file[2:],'w',encoding='utf8') as f:
    f.write(json.dumps(dit))