date = input("날짜(연/월/일)입력: ")
date_list = date.split("/")
print("입력한 날짜의 10년 후는 %d년 %s월 %s일" % (int(date_list[0]) + 10, date_list[1], date_list[2]))