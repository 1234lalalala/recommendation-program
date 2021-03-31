import json
threshold = 0.2
with open('relation_digraph.json','r',encoding='utf8') as f:
    relation = json.loads(f.read())
# print(relation)

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
with open(f'./cluster_digraph/all_cluster_{threshold}.json','w',encoding='utf8') as f:
    for each in sub_graph_list:
        if len(each) > 1:
            show_course(each)
            f.write('\t'.join(each) + '\n')



# C_course-v1:JNU+11022048+2019_T1
# C_course-v1:SDUx+00931800X+sp
# C_course-v1:NEU+2018051501+sp