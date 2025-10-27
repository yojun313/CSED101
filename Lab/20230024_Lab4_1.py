mid = int(input("중간고사 점수 입력: "))
final = int(input("기말고사 점수 입력: "))

def calc_average(mid, final):
    return (mid + final)/2

def calc_grade(average):
    if average >= 90:
        return 'A'
    elif average >= 80 and average < 90:
        return 'B'
    elif average >= 70 and average < 80:
        return 'C'
    elif average >= 60 and average < 70:
        return 'D'
    else:
        return 'F'

print("평균:", calc_average(mid, final))
print("학점:", calc_grade(calc_average(mid, final)))
    