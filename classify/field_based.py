import json
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



def filter_concept(l):
    # ret = []
    # for i in list(set(l)):
    #     if l.count(i) > len(l) *0.34:
    #         ret.append(i)
    ret = {}
    for i in l:
        if i in ret:
            ret[i] += 1
        else:
            ret[i] = 1
    l = [[_,ret[_]] for _ in ret if ret[_] > len(l) * 0.2]
    l.sort(key=lambda x:x[1],reverse=True)
    return l

#2.添加领域信息
def get_field_all(course):

    concept_field = {}
    with open('../relations/concept-field.json', 'r', encoding='utf8') as f:
        for i in f:
            concept,field = (i.strip().split('\t'))
            concept_field[concept] = field
        # print(len(concept_field))
    course_concept = {}
    with open('../relations/course-concept.json','r',encoding='utf8') as f:
        for i in f:
            id,concept = (i.strip().split('\t'))
            if id in course_concept :
                # if concept_field[concept] not in  course_concept[id]:
                course_concept[id].append(concept_field[concept])
                # course_concept[id].append(concept)

            else:
                course_concept[id] = [concept_field[concept]]
                # course_concept[id] = [concept]

    # print(course_concept)
    for id in course:
        if id not in course_concept:
            course[id]['field'] = []
            # print(id , course[id])
            continue
        course[id]['field'] = filter_concept(course_concept[id])
    return course

#3.按领域划分
def class_field(course):
    ret = {}
    ret1 = {}
    for i in course:
        if not course[i]['field']:
            continue
        for each in course[i]['field']:
            if each in ret:
                ret[each].append(i)
            else:
                ret[each] = [i]
        key = str(course[i]['field'])
        if key not in ret1:
            ret1[key] = [i]
        else:
            ret1[key].append(i)
    print(ret1)

    for i in ret1:
        print(i, len(ret1[i]))
        if len(ret1[i]) < 2:
            continue
        with open(f'field1/{i}.txt', 'w', encoding='utf8') as f:
            for c in ret1[i]:
                f.write(c + '\t' + course[c]['name'] + '\n')
if __name__ == '__main__':
    course = get_course_info('../entities/course.json')
    course = get_field_all(course)
    print(course)
    dit1 = {}
    dit = {}
    for i in course:
        if (len(course[i]['field'])) == 1:
            k =  course[i]['field'][0][0]
            if k in dit1:
                dit1[k].append(i)
            else:
                dit1[k] = [i]
            continue
        if (len(course[i]['field'])) == 0:
            continue
            print(course[i])
        if (len(course[i]['field'])) >= 2:
            l = course[i]['field'][:2]
            for _ in l:
                if _[0] in dit:
                    dit[_[0]].append(i)
                else:
                    dit[_[0]] = [i]
# for i in dit1:
#     # print(i, len(dit1[i]))
#     if len(dit1[i]) < 2 and len(dit1[i]) > 30:
#         continue
#     with open(f'field1/{i}.txt', 'w', encoding='utf8') as f:
#         for c in dit1[i]:
#             f.write(c + '\t' + course[c]['name'] + '\n')
print(dit)
k_list = list(dit.keys())
for i in range(len(k_list) -1 ):
    for j in range(i+1,len(k_list)):
        k1 = k_list[i]
        k2 = k_list[j]
        c_l = list(set(dit[k1]) & set(dit[k2]))
        if len(c_l) < 2:
            continue
        # print(k1,k2,len(c_l))
        with open(f'./field2/{k1}_{k2}.txt','w',encoding='utf8') as f:
            for _ in c_l:
                f.write(_+'\t'+ course[_]['name'] + '\n')



