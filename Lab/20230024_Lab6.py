fr = open("score.txt", "r") #파일 경로 입력

line = fr.readlines()
stu_num_list = []
stu_score_list = []
for i in line:
    stu_num = i[0:6]
    stu_score_1 = i[7:9]
    stu_score_2 = i[10:12]
    
    stu_num_list.append(stu_num) 
    average = (int(stu_score_1) + int(stu_score_2))/2
    if average >= 90:
        stu_score_list.append(str(average)+"(A)")
    elif average >= 80 and average < 90:
        stu_score_list.append(str(average)+"(B)")
    elif average >= 70 and average < 80:
        stu_score_list.append(str(average)+"(C)")
    elif average >= 60 and average < 70:
        stu_score_list.append(str(average)+"(D)")
    else:
        stu_score_list.append(str(average)+"(F)")
        
newfile = open("report.txt", "w")
for i in range(len(stu_num_list)):
    new = stu_num_list[i] + " " + stu_score_list[i] + "\n"
    newfile.write(new)
fr.close()
newfile.close()
