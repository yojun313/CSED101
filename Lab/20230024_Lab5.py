dict = {}
list = []
sen = input("Enter a sentence: ")

for i in sen:
    if i not in list:
        list.append(i)

for i in list:
    key = i
    value = sen.count(key)
    dict[key] = value

print(dict)
    
