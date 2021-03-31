import json
import time

train = []
target = []

with open('./train_data/test.json','r',encoding='utf8') as f:
    for i in f:
        data = (json.loads(i.strip()))
        time1 = data['enroll_time']
        # timeArray = time.strptime(time1, "%Y-%m-%d %H:%M:%S")
        c_list = data['course_order']
        c_list = [[i,time1[num]] for num,i in enumerate(c_list)]
        c_list.sort(key=lambda x:time.strptime(x[1], "%Y-%m-%d %H:%M:%S"))
        l = [_[0] for _ in c_list]
        train.append(l[:-3])
        target.append(l[-3:])


def get_course_list1(c_list,dit):
    ret = []
    for each in c_list:
        if each in dit:
            ret+=dit[each]
    return ret

def check(target,l):
    n = 0
    for i in target:
        if i in l:
            n+=1
    return n/len(target)

n = 0
m = 0
undigraph = json.load(open('./graph/cluster_undigraph/all_cluster_0.7.dict','r',encoding='utf8'))
digraph = json.load(open('./graph/cluster_digraph/all_cluster_0.2.dict','r',encoding='utf8'))
name = json.load(open('./classify/dit/name','r',encoding='utf8'))
teacher = json.load(open('./classify/dit/teacher','r',encoding='utf8'))
field = json.load(open('./classify/dit/field1','r',encoding='utf8'))
school = json.load(open('./classify/dit/school','r',encoding='utf8'))

test = json.load(open('./test.dict','r',encoding='utf8'))

dit_list = [field]
for i in range(len(train)):
    # l = get_course_list1(train[i], dit) + get_course_list1(train[i], dit1)
    l = []
    for each in dit_list:
        l+= get_course_list1(train[i],each)
    l = list(set(l))
    n += (check(target[i], l))
    m+=len(l)
print(n/len(train))
print(m/len(train))