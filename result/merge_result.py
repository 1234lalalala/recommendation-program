import json
import time,os

class_num = {i.strip().split('\t')[0]:i.strip().split('\t')[1]     for i in open('../knowledge_graph/class_num.txt',encoding='utf8')}
course_all = {json.loads(i.strip())['id']:json.loads(i.strip())['name'] for i in open('../entities/course.json','r',encoding='utf8')}
file = '../classify/field1'
id_field = {}
for each_file in os.listdir(file):
    with open(file+'/' +each_file,'r',encoding='utf8') as f:
        for line in f:
            if line.strip() not in id_field:
                id_field[line.strip().split('\t')[0]] = [each_file[:-4]]
            else:
                id_field[line.strip().split('\t')[0]].append(each_file[:-4])
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

name = [i.strip().split('\t') for i in open('./name_result','r',encoding='utf8')]
teacher = [i.strip().split('\t') for i in open('./teacher_result','r',encoding='utf8')]
field = [i.strip().split('\t') for i in open('./field_result','r',encoding='utf8')]
vote = [i.strip().split('\t') for i in open('./vote_result/0.1','r',encoding='utf8')]
vote_p = [i.strip().split('\t') for i in open('./vote_result_p/0.5','r',encoding='utf8')]
field_hot = [i.strip().split('\t') for i in open('./field_hot_20','r',encoding='utf8')]
field_new = [i.strip().split('\t') for i in open('./field_new_10','r',encoding='utf8')]
vote_cold = [i.strip().split('\t') for i in open('./vote_cold_50.txt','r',encoding='utf8')]

class_year = {i.strip().split('\t')[0]:int(i.strip().split('\t')[1])     for i in open('../knowledge_graph/course_time.txt',encoding='utf8')}

def show_error_course(l,target):
    print()
    print(class_num[target[0]])
    #输出已选课程的领域 老师 学校信息
    print(class_year[target[0]])
    print([course_all[_] for _ in target],[course_all[_] for _ in l])
    print([id_field[i] if i in id_field else None for i in target],'---', [id_field[i] if i in id_field else None for i in l])
    # print([id_teacher[i] if i in id_teacher else None for i in target],'---', [id_teacher[i] if i in id_teacher else None for i in l])


def get_result(i,dit_l):
    ret = []
    for _ in dit_l:
        ret += _[i]
    return set(ret)
dit_l = [name,vote,teacher,vote_cold,field_hot]
n = m =length =0
for i in range(len(target)):
    l = get_result(i,dit_l)
    for _ in target[i]:
        if _ in l:
            n += 1
        else:
            show_error_course(train[i], target[i])
        m += 1
    length += len(l)
print(n / m)
print(length / len(train))

















