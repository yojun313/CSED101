list1 = []
list2 = []
for i in range(1,10):
    for j in range(2,10):
        a = "%d*%d= %d " % (j,i,i*j)
        list1.append(a)
    list2.append(list1)
    list1 = []

for k in list2:
    for p in k:
        print(p, end = '')
    print()