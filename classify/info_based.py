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
    ret = []
    for i in list(set(l)):
        if l.count(i) > len(l) *0.34:
            ret.append(i)
    return ret

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
            else:
                course_concept[id] = [concept_field[concept]]
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

#4.按老师划分
def class_teacher(course):
    course_teacher = {}
    with open('../relations/teacher-course.json', 'r', encoding='utf8') as f:
        for i in f:
            teacher, id = (i.strip().split('\t'))
            course_teacher[id] = teacher
    ret = {}
    for id in course:
        if id not in course_teacher:
            course[id]['teacher'] = None
            print(id , course[id])
            continue
        course[id]['teacher'] = course_teacher[id]
    for i in course:
        if not course[i]['teacher']:
            continue
        teacher = course[i]['teacher']
        if teacher in ret:
            ret[teacher].append(i)
        else:
            ret[teacher] = [i]
    for i in ret:
        if len(ret[i]) <4:
            continue
        print(i, len(ret[i]))
        with open(f'teacher/{i}.txt', 'w', encoding='utf8') as f:
            for c in ret[i]:
                f.write(c + '\t' + course[c]['name'] + '\n')
    return course

#4.按老师划分
def class_school(course):
    course_school = {}
    with open('../relations/school-course.json', 'r', encoding='utf8') as f:
        for i in f:
            school, id = (i.strip().split('\t'))
            course_school[id] = school
    ret = {}
    for id in course:
        if id not in course_school:
            course[id]['school'] = None
            print(id , course[id])
            continue
        course[id]['school'] = course_school[id]
    for i in course:
        if not course[i]['school']:
            continue
        school = course[i]['school']
        if school in ret:
            ret[school].append(i)
        else:
            ret[school] = [i]
    for i in ret:
        if len(ret[i]) <4:
            continue
        print(i, len(ret[i]))
        with open(f'school/{i}.txt', 'w', encoding='utf8') as f:
            for c in ret[i]:
                f.write(c + '\t' + course[c]['name'] + '\n')
    return course

if __name__ == '__main__':
    course = get_course_info('../entities/course.json')
    course = get_field_all(course)
    print(course)
    for key in course:
        if (len(course[key]['field'])) > 2:
            print(course[key])
    # print(len(course))
    class_field(course)
    # class_teacher(course)
    # class_school(course)
