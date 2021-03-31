import json
import time

relation = {}
class_num = {}
def update_graph(l):
    for i in l:
        if i in class_num:
            class_num[i] += 1
        else:
            class_num[i] = 1
    for i in range(len(l)-1):
        for j in range(i+1,len(l)):
            a,b = (l[i],l[j])
            if a not in relation:
                relation[a] = {}
            if b not in relation:
                relation[b] = {}
            if b not in relation[a]:
                relation[a][b] = 1
            else:
                relation[a][b] += 1
            if a not in relation[b]:
                relation[b][a] = 1
            else:
                relation[b][a] += 1


with open('../train_data/train.json','r',encoding='utf8') as f:
    for i in f:
        data = (json.loads(i.strip()))
        time1 = data['enroll_time']
        # timeArray = time.strptime(time1, "%Y-%m-%d %H:%M:%S")
        c_list = data['course_order']
        c_list = [[i,time1[num]] for num,i in enumerate(c_list)]
        c_list.sort(key=lambda x:time.strptime(x[1], "%Y-%m-%d %H:%M:%S"))
        update_graph([i[0] for i in c_list])
for key in relation:
    print(key,class_num[key])
    for _ in relation[key]:
        relation[key][_] = relation[key][_]/class_num[key]
    print(relation[key])
with open('relation_undigraph.json','w',encoding='utf8') as f:
    f.write(json.dumps(relation,ensure_ascii=False))

print(len(relation))
course_all = {json.loads(i.strip())['id']:json.loads(i.strip())['name'] for i in open('../entities/course.json','r',encoding='utf8')}
print(set(list(course_all.keys()))-set(list(relation.keys())))