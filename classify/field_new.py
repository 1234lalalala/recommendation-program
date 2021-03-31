#为用户推荐主要领域的热门课程
import os
top_n = 10
file = '../classify/field'
class_year = {i.strip().split('\t')[0]:int(i.strip().split('\t')[1])     for i in open('../knowledge_graph/course_time.txt',encoding='utf8')}

id_field = {}
field_num = {}
field_class = {}
for each_file in os.listdir(file):
    num = 0
    field_class[each_file[:-4]] = []
    with open(file+'/' +each_file,'r',encoding='utf8') as f:
        for line in f:
            num+=1
            field_class[each_file[:-4]].append(line.strip().split('\t')[0])
            if line.strip().split('\t')[0] not in id_field:
                id_field[line.strip().split('\t')[0]] = [each_file[:-4]]
            else:
                id_field[line.strip().split('\t')[0]].append(each_file[:-4])
    field_num[each_file[:-4]] = num
print(id_field)


import json
import time
threshold = 0.2

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


def get_field(l):
    ret = {}
    for i in l:
        if i not in id_field:
            continue
        for _ in id_field[i]:
            if _ in ret:
                ret[_] += 1
            else:
                ret[_] = 1
    l = [(i,ret[i]/field_num[i]) for i in ret]
    l.sort(key=lambda x:x[1],reverse=True)
    return l

def field_course(field):
    l = field_class[field]
    # print(len(class_year))
    l = [i for i in l if i in class_year and class_year[i] <= 1]
    l.sort(key=lambda x:class_year[x])
    # print(l)
    return l[:top_n]

n = m = 0
length = 0
f =  open(f'../result/field_new_{top_n}','w',encoding='utf8')

for i in range(len(train)):
    field = (get_field(train[i]))
    l = field_course(field[0][0]) + field_course(field[1][0]) if len(field) >1 else []
    # l = field_course(field[0][0])

    f.write('\t'.join(l) + '\n')
    for _ in target[i]:
        if _ in l:
            n += 1
        m += 1
    length += len(l)
print(n / m)
print(length / len(train))