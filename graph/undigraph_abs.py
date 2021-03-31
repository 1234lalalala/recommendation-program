import json
import time

relation = {}
class_num = {}
#统计所有的边
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



#将连接的边的权重由数字替换为转移概率
for key in relation:
    # print(key,class_num[key])
    for _ in relation[key]:
        if class_num[key]<=50:
            relation[key][_] = 0
            relation[_][key] = 0
        else:
            relation[key][_] = relation[key][_]/class_num[key]
    # print(relation[key])

print(len(relation))

#挑出选课数量小于50的课程
relation_less = {}
for key in relation:
    if class_num[key] <= 50:
        relation_less[key] = relation[key]


threshold = 0.3
course_all = {json.loads(i.strip())['id']:json.loads(i.strip())['name'] for i in open('../entities/course.json','r',encoding='utf8')}
# print(course_all)

def show_course(l):
    print(len(l),[course_all[i] for i in l])

def find_sub_graph(c_id):
    ret = set()
    l = [c_id]
    merge_flag = False
    while l:
        # print(l)
        key = l.pop(0)
        ret.add(key)
        for i in relation[key]:
            if relation[key][i] < threshold:
                continue
            # print(relation[key][i],relation[i][key])
            if i in ret :
                continue
            if i not in course_set:
                merge_flag = True
            ret.add(i)
            l.append(i)
    # show_course(ret)
    return ret,merge_flag
course_set = set(course_all.keys())
# show_course(find_sub_graph('C_course-v1:SPI+40281x+sp'))

sub_graph_list = []
while course_set:
    a = course_set.pop()
    if a not in relation:
        # sub_graph_list.append({a})
        continue

    sub_graph,flag = find_sub_graph(a)
    course_set -= sub_graph
    if not flag:
        sub_graph_list.append(sub_graph)
    else:
        for num,i in enumerate(sub_graph_list):
            if i & sub_graph:
                # print(len(sub_graph),sub_graph)
                sub_graph_list[num] = i | sub_graph
                break

# print(sub_graph_list)
# print(len(sub_graph_list))
final_dict = {}

def merge(graph_list):
    if len(graph_list) == 1:
        return graph_list

    while 1:
        flag = 1
        x = graph_list[0]
        l = []
        for i in graph_list[1:]:
            if i & x:
                x = x | i
                flag = 0
            else:
                l.append(i)
        if flag:
            break
        graph_list = [x] + l
    return [x] + merge(l)
print(len(merge(sub_graph_list)))
sub_graph_list = merge(sub_graph_list)


def check_distribute(l):
    l = list(l)
    for i in range(len(l)):
        # print(class_num[l[i]])
        for j in range(i,len(l)):
            if l[j] in relation[l[i]] and relation[l[i]][l[j]] > 0.1:
                print(relation[l[i]][l[j]],course_all[l[i]],course_all[l[j]])

for each in sub_graph_list:
    if len(each) > 1:
        show_course(each)
        # check_distribute(each)
# with open(f'./cluster_digraph/all_cluster_{threshold}.json','w',encoding='utf8') as f:
#     for each in sub_graph_list:
#         if len(each) > 1:
#             show_course(each)
#             f.write('\t'.join(each) + '\n')


dit = {}
for lst in sub_graph_list:
    # print(lst)
    if len(lst) < 2:
        continue

    lst = list(lst)
    for a in range(len(lst) - 1):
        for b in range(a + 1, len(lst)):
            if lst[a] not in dit:
                dit[lst[a]] = []
            if lst[b] not in dit:
                dit[lst[b]] = []
            dit[lst[a]].append(lst[b])
            dit[lst[b]].append(lst[a])

# for key in dit:
#     print(len(dit[key]))
with open('../test.dict','w',encoding='utf8') as f:
    f.write(json.dumps(dit))

import json
import time

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
    # for each in target:
    #     if each not in l:
    #         print(course_all[each],class_num[each])
    return n/len(target)

n = 0
m = 0
name = json.load(open('../classify/dit/name','r',encoding='utf8'))
teacher = json.load(open('../classify/dit/teacher','r',encoding='utf8'))
field = json.load(open('../classify/dit/field1','r',encoding='utf8'))
school = json.load(open('../classify/dit/school','r',encoding='utf8'))



dit_list = [dit,field,name,teacher]
for i in range(len(train)):
    # l = get_course_list1(train[i], dit) + get_course_list1(train[i], dit1)
    l = []
    for each in dit_list:
        l+= get_course_list1(train[i],each)
    l = list(set(l))
    # print([course_all[_] for _ in train[i]])
    n += (check(target[i], l))
    m+=len(l)
print(n/len(train))
print(m/len(train))