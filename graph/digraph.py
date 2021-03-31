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
            if b not in relation[a]:
                relation[a][b] = 1
            else:
                relation[a][b] += 1


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
    # print(key,class_num[key])
    for _ in relation[key]:
        relation[key][_] = relation[key][_]/class_num[key]
    # print(relation[key])
# with open('relation_digraph.json','w',encoding='utf8') as f:
#     f.write(json.dumps(relation,ensure_ascii=False))
dis_dit = {1:0,10:0,50:0,100:0,1000:0,2000:0}
for key in class_num:
    n = class_num[key]
    if n < 10:
        dis_dit[1] += 1
    elif n < 50:
        dis_dit[10] += 1
    elif n < 100:
        dis_dit[50] += 1
    elif n < 1000:
        dis_dit[100] += 1
    elif n < 2000:
        dis_dit[100] += 1
    else:
        dis_dit[2000] += 1
print(dis_dit)