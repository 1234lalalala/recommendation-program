#直接使用转移概率进行投票
import json
import time
threshold = 1

train = []
target = []

with open('../train_data/test.json','r',encoding='utf8') as f:
    for i in f:
        data = (json.loads(i.strip()))
        time1 = data['enroll_time']
        # timeArray = time.strptime(time1, "%Y-%m-%d %H:%M:%S")
        c_list = data['course_order']
        c_list = [[i,time1[num]] for num,i in enumerate(c_list)]
        c_list.sort(key=lambda x:time.strptime(x[1], "%Y-%m-%d %H:%M:%S"))
        l = [_[0] for _ in c_list]
        train.append(l[:-1])
        target.append(l[-1:])

relation_dit = {}
with open('../knowledge_graph/interaction_graph_p.txt','r',encoding='utf8') as f:
    for i in f:
        c1,c2,p = i.strip().split('\t')
        p = float(p)
        if not p:
            continue
        if c1 in relation_dit:
            relation_dit[c1][c2] = p
        else:
            relation_dit[c1] = {c2:p}

for k in relation_dit:
    for k1 in relation_dit[k]:
        a = relation_dit[k][k1]
        b = relation_dit[k1][k]
        relation_dit[k][k1] = max(a,b)
        relation_dit[k1][k] = max(a,b)


def get_course_list1(c_list,dit):
    ret = {}
    for each in c_list:
        if each in dit:
            for _ in dit[each]:
                if _ in ret:
                    ret[_] += dit[each][_]
                else:
                    ret[_] = dit[each][_]
    return [_ for _ in ret if ret[_] > threshold]

f =  open(f'../result/vote_result_p/{threshold}','w',encoding='utf8')
n = m = 0
length = 0
for i in range(len(train)):
    l = get_course_list1(train[i],relation_dit)
    # print(target[i],l)
    f.write('\t'.join(l) + '\n')
    for _ in target[i]:
        if _ in l:
            n+=1
        m+=1
    length+=len(l)
print(n/m)
print(length/len(train))