import json


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
                if concept_field[concept] not in  course_concept[id]:
                    course_concept[id].append(concept_field[concept])
            else:
                course_concept[id] = [concept_field[concept]]
    # print(course_concept)
    for id in course:
        if id not in course_concept:
            course[id]['field'] = []
            # print(id , course[id])
            continue
        course[id]['field'] = course_concept[id]
    return course

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

user_course = {}
with open('../relations/user-course.json','r',encoding='utf8') as f:
    for i in f:
        id,course = i.strip().split('\t')
        if id in user_course:
            user_course[id].append(course)
        else:
            if len(user_course) > 99:
                break
            user_course[id] = [course]
print(user_course)
course = get_course_info('../entities/course.json')
course = get_field_all(course)
print(course)

a = 0
b = 0
for user in user_course:
    a += 1
    ret = []
    n = len(user_course[user])
    for c in user_course[user]:
        ret += course[c]['field']
    l = {}
    for i in ret:
        if i in l:
            l[i] += 1
        else:
            l[i] = 1
    l = [(i,l[i]) for i in l]
    l.sort(key=lambda x:x[1],reverse=True)
    b += l[0][1]/n
    print(l[0][1]/n,l,[course[id]['name'] for id in user_course[user]])
print(b/a)


