import json
import re
import pprint

#1.读取所有的课程
def get_course_info(f):
    ret = {}
    with open(f,'r',encoding='utf8') as course_f:
        for line in course_f:
            text = line.strip()
            if not text:
                continue
            data_line = json.loads(text)
            ret[data_line['id']] =  {'name':data_line['name'],'prerequisites':data_line['prerequisites']}
    return ret
#2.先修课程的提取
def prerequisites_process(s):
    if re.search(r'^无',s):
        return []
    if re.search(r'《(.*?)》',s):
        ret = re.findall(r'《(.*?)》',s)
        return ret
    if re.search('、',s):
        return s.split('、')
    return [s]
#3.添加领域信息
def get_field_all(course):

    concept_field = {}
    with open('relations/concept-field.json', 'r', encoding='utf8') as f:
        for i in f:
            concept,field = (i.strip().split('\t'))
            concept_field[concept] = field
        # print(len(concept_field))
    course_concept = {}
    with open('relations/course-concept.json','r',encoding='utf8') as f:
        for i in f:
            id,concept = (i.strip().split('\t'))
            if id in course_concept :
                if concept_field[concept] not in  course_concept[id]:
                    course_concept[id].append(concept_field[concept])
            else:
                course_concept[id] = [concept_field[concept]]
    # print(course_concept)
    for id in course:

        course[id]['field'] = course_concept[id]
    return course

#4.添加教师信息
def get_teacher_all(course):
    course_teacher = {}
    with open('relations/teacher-course.json', 'r', encoding='utf8') as f:
        for i in f:
            teacher, id = (i.strip().split('\t'))
            course_teacher[id] = teacher
    teacher_school = {}
    with open('relations/school-teacher.json', 'r', encoding='utf8') as f:
        for i in f:
            school, teacher = (i.strip().split('\t'))
            teacher_school[teacher] = school
    for id in course:
        course[id]['teacher'] = course_teacher[id]
        course[id]['school'] = course[id]['teacher']




if __name__ == '__main__':
    path = 'course_10'
    course = get_course_info(path + '/course_10.json')
    print(course)
    for key in course:
        print(key)
        course[key]['prerequisites'] = prerequisites_process(course[key]['prerequisites'])
    get_field_all(course)
    # get_teacher_all(course)
    pprint.pprint(course)