from _datetime import datetime
import json
import time


def get_course_info(f):
    ret = {}
    with open(f,'r',encoding='utf8') as course_f:
        for line in course_f:
            text = line.strip()
            if not text:
                continue
            data_line = json.loads(text)
            ret[data_line['id']] =  {'name':data_line['name']}
    return ret
course = get_course_info('../entities/course.json')
print(course)

n_self = 0
n_self_t = datetime.now() - datetime.now()

n_all = 0
n_online = 0
n_online_t = datetime.now() - datetime.now()

import re
with open('../train_data/train.json','r',encoding='utf8') as f:
    for i in f:
        data = (json.loads(i.strip()))
        time1 = data['enroll_time']
        # timeArray = time.strptime(time1, "%Y-%m-%d %H:%M:%S")
        c_list = data['course_order']
        c_list = [[i,time1[num]] for num,i in enumerate(c_list)]
        c_list.sort(key=lambda x:time.strptime(x[1], "%Y-%m-%d %H:%M:%S"))
        c_list_name = [course[_[0]]['name'] for _ in c_list]
        n = len(set([re.sub(r'（[^下上一二先修课]*）','',_) for _ in c_list_name]))
        if n < len(set(c_list_name)):
            # print(n,len(set(c_list_name)),c_list_name)
            # print(c_list)
            dit = {}
            for num,_ in enumerate(c_list_name):
                if re.sub(r'（[^下上一二先修课]*）','',_) not in dit:
                    dit[re.sub(r'（[^下上一二先修课]*）','',_)] = [(_,c_list[num])]
                else:
                    dit[re.sub(r'（[^下上一二先修课]*）','',_)].append((_,c_list[num]))
            for k in dit:
                if len(dit[k]) == 2:
                    t1 = dit[k][0][1][1]
                    t2 = dit[k][1][1][1]
                    print(datetime.strptime(str(t2),"%Y-%m-%d %H:%M:%S") - datetime.strptime(str(t1),"%Y-%m-%d %H:%M:%S"),dit[k])
                    # print(dit[k])
                    l_model = ([re.search(r'（([^下上一二先修课]*)）',i[0]).group(1) if re.search(r'（[^下上一二先修课]*）',i[0]) else i[0] for i in dit[k]])
                    if l_model[0] == '自主模式':
                        n_self_t += datetime.strptime(str(t2),"%Y-%m-%d %H:%M:%S") - datetime.strptime(str(t1),"%Y-%m-%d %H:%M:%S")
                        n_self += 1
                    elif l_model[-1] == '自主模式':
                        n_online_t += datetime.strptime(str(t2),"%Y-%m-%d %H:%M:%S") - datetime.strptime(str(t1),"%Y-%m-%d %H:%M:%S")
                        n_online += 1
                    n_all += 1
print(n_self_t/n_self,n_online_t/n_online)

        # break
        # print(c_list)
# l = ['中国近现代史纲要（2019春）', '中国近现代史纲要（2019春）', '中国近现代史纲要（自主模式）']
# print([re.sub(r'（[^下上0-9]*）','',_) for _ in l])