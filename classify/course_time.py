# import json
# def get_course_time(f):
#     ret = {}
#     with open(f,'r',encoding='utf8') as user_f:
#         for line in user_f:
#             user_data = json.loads(line.strip())
#             course_list = user_data['course_order']
#             course_time = user_data['enroll_time']
#             for c,t in zip(course_list,course_time):
#                 if c in ret:
#                     ret[c].append(t)
#                 else:
#                     ret[c] = [t]
#
#
#     return ret
#
# def time_count(l):
#     ret = {}
#     for i in l:
#         year =i[:4]
#         mouth = i[5:7]
#         sem = 1
#         # print(year)
#         if year in ret:
#             ret[year]['n'] += 1
#             if mouth in  ret[year]:
#                 ret[year][mouth] += 1
#             else:
#                 ret[year][mouth] = 1
#         else:
#             ret[year] = {}
#             ret[year]['n'] = 1
#             ret[year][mouth] = 1
#     return ret
#
# if __name__ == '__main__':
#     course = get_course_time('../entities/user.json')
#     # course = get_field_all(course)
#     f = open('../knowledge_graph/course_semester.txt','w',encoding='utf8')
#     for key in course:
#         a = (time_count(course[key]))
#         f.write(key + '\t' + str(len(a)) +  '\n')
#         # print(course[key])
#         # break

with open('./course_id.txt',encoding='utf8') as f:
    for i in f:
        name,id = (i.strip().split(';'))
        if id[-2:] == 'T1':
            continue
        elif id[-2:].lower() == 't2':
            continue
        elif id[-2:].lower() == 'sp':
            print(name,id)
            continue

        else:
            # print(name,id)
            continue