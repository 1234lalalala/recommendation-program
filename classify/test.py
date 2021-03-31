import json

dit = {}
c_id = {i.strip().split(';')[0]:i.strip().split(';')[1] for i in open('./course_id.txt','r',encoding='utf8')}
with open('name_based.txt','r',encoding='utf8') as f:
    for i in f:
        a,b = i.strip().split('\t')
        b = eval(b)
        dit[c_id[a].strip()] = [c_id[_.strip()] for _ in b]

with open('dit/name','w',encoding='utf8') as f:
    f.write(json.dumps(dit))