from _datetime import datetime
t2 = '2017-05-01 11:07:53'
a = datetime.strptime(str(t2),"%Y-%m-%d %H:%M:%S")
b = datetime.strftime(a,"%y-%M")
print(b)