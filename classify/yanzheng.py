import json


def check1(id_class,user_course):
    a = 0
    b = 0
    flag = 0
    for i in user_course:
        course_list = user_course[i]
        l = [id_class[_] if _ in id_class else _ for _ in course_list]
        a += 1
        if len(set(l)) != len(l):
            b+= 1
            flag = 1
        print(i,l,flag)
        flag = 0

    print(b/a)
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


course_teacher = {}
with open('../relations/teacher-course.json', 'r', encoding='utf8') as f:
    for i in f:
        teacher, id = (i.strip().split('\t'))
        course_teacher[id] = teacher
course_school = {}
with open('../relations/school-course.json', 'r', encoding='utf8') as f:
    for i in f:
        school, id = (i.strip().split('\t'))
        course_school[id] = school
course = get_course_info('../entities/course.json')
with open('name_based.txt', 'r', encoding='utf8') as f:
    name_based = {}
    for i in f:
        c,nei = i.strip().split('\t')
        nei = eval(nei)
        name_based[c] = nei

def func(l,d):
    for each in l:
        if each in d:
            return True
def check2(user_course):
    a = 0
    b = 0
    flag = 0
    for i in user_course:
        a += 1
        l = [course[_]['name'] for _ in user_course[i]]
        for num,j in enumerate(l):
            if j in name_based:
                if func(l[num+1:],name_based[j]):
                    flag = 1
                    b += 1
                    break
        print(l,flag)
        flag = 0
    print(b/a)




# check1(course_school,user_course)
check2(user_course)