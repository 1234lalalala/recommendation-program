import json

f_name = './cluster_digraph/all_cluster_0.3.json'
dit = {}
with open(f_name,'r',encoding='utf8') as f:
    for i in f:
        lst = i.strip().split('\t')
        for a in range(len(lst)-1):
            for b in range(a+1,len(lst)):
                if lst[a] not in dit:
                    dit[lst[a]] = []
                if lst[b] not in dit:
                    dit[lst[b]] = []
                dit[lst[a]].append(lst[b])
                dit[lst[b]].append(lst[a])
for key in dit:
    print(len(dit[key]))
with open(f_name[:-4]+'dict','w',encoding='utf8') as f:
    f.write(json.dumps(dit))