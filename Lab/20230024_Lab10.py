def bubble_sort(list):
    j = 1
    for i in range(len(list)-1):
        for i in range(len(list)-1):
            if list[i] > list[i+1]:
                list[i], list[i+1] = list[i+1], list[i]
        print("[step "+str(j)+"]", *list)
        j += 1
        
def seq_search(list, target):
    j = -1
    for i in list:
        j += 1
        if i == target:
            return j
    return -1
            
        
def sigma(a, b):
    sum = 0
    for i in range(a, b+1):
        sum += i
    return sum            
                
def sigma_rec(a, b):
    if a == b:
        return a
    else:
        return a + sigma_rec(a + 1, b)
    
