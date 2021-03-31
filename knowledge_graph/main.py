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

out =  open('./interaction_graph.txt','w',encoding='utf8')
# print(relation)
for i in relation:
    for j in relation[i]:
        out.write(i + '\t' + j + '\t' + str(relation[i][j]) + '\n')


out1 =  open('./class_num.txt','w',encoding='utf8')
# print(relation)
for i in class_num:
    out1.write(i + '\t' + str(class_num[i]) + '\n')
print(class_num)

less_relation = {}
for key in relation:
    if class_num[key] <= 50:
        less_relation[key] = relation[key]
    # print(key,class_num[key])
#     for _ in relation[key]:
#         if class_num[key]<=50:
#             relation[key][_] = 0
#             relation[_][key] = 0
#
#         else:
#             relation[key][_] = relation[key][_]/class_num[key]
#
# out2 =  open('./interaction_graph_p.txt','w',encoding='utf8')
# # print(relation)
# for i in relation:
#     for j in relation[i]:
#         out2.write(i + '\t' + j + '\t' + str(relation[i][j]) + '\n')

out3 =  open('./less_class_graph.txt','w',encoding='utf8')
# print(relation)
for i in less_relation:
    for j in less_relation[i]:
        out3.write(i + '\t' + j + '\t' + str(less_relation[i][j]) + '\n')