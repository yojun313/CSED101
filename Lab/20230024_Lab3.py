######################################################
# 학번: 20230024
# 이름: 문요준
######################################################


######################################################
# 실습1 - (함수 완성하기)
def sec_to_hms(seconds):
    hr = seconds // 3600
    min_ = (seconds % 3600) / 60
    sec = ((seconds % 3600) % 60)
    return hr, min_, sec

def problem1():
    hr, min_, sec = sec_to_hms(57894)
    print("%d시간 %d분 %d초" % (hr, min_, sec))

######################################################
# 실습2 - (함수 완성하기)
def merge_list(L1, L2):
    list1 = L1 + L2
    list1.sort()
    return list1

def problem2():
    L = [3, 5, 9, 1, 2]
    ml1 = merge_list(L, [2, 1])
    ml2 = merge_list([6, 9, 4], L)

    print(ml1) 
    print(ml2) 

######################################################
# 실습3 - (함수 완성하기)
def get_min_max(L):
    a = min(L)
    b = max(L)
    L.remove(a)
    L.remove(b)
    return a,b

def problem3():
    nlist = [3, 5, 9, 1, 2]
    min_val, max_val = get_min_max(nlist)
    print(min_val)
    print(max_val)
    print(nlist)

######################################################
# 실습4 - 랜덤 모듈 사용 

# 랜덤 모듈 불러오기 (채울 것)


def problem4(): # (함수 완성하기)
    import random
    menu = ["된장찌개", "부대찌개", "김치찌개", "삼계탕", "파스타", "돈까스", "쌀국수"]
    food = random.choice(menu)
    print("오늘 점심은 %s입니다." % food)

######################################################
if __name__ == "__main__":
    problem1() # 실습1
    problem2() # 실습2
    problem3() # 실습3
    problem4() # 실습4


