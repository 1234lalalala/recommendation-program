import json

train_data = []
test_data = []
n = 0
with open('../entities/user.json','r',encoding='utf8') as f:
    for i in f:
        data = (json.loads(i.strip()))
        # if len(data['course_order']) > 10 and len(data['course_order']) < 20 and n < 2000:
        if len(data['course_order']) > 5:

            test_data.append(data)
            n+=1
            continue
        train_data.append(data)

print(len(test_data))
print(len(train_data))
#
# with open('train.json','w',encoding='utf8') as f:
#     for i in train_data:
#         f.write(json.dumps(i,ensure_ascii=False) + '\n')
#
# with open('test.json','w',encoding='utf8') as f:
#     for i in test_data:
#         f.write(json.dumps(i,ensure_ascii=False) + '\n')