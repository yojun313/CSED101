import os
import random

def main():
    global com_choice
    global user_choice
    global win_num
    global move_num
    
    player_stairs = 0 #변수 초기화
    com_stairs = 0
    move_num = 1
    win_num = 3 #0이면 무승부, 1이면 user 승, #2이면 com 승 4이면 user승으로 묵찌빠 종료, 5이면 com승으로 묵찌빠 종료
    print("=====================") #시작화면 출력
    print("[묵찌빠 계단 오르기]")
    print("=====================")
    print("○         ●")
    print("▨         ▨")
    print("▨▨       ▨▨")
    print("▨▨▨     ▨▨▨")
    print("▨▨▨▨   ▨▨▨▨")
    print("▨▨▨▨▨ ▨▨▨▨▨")
    print("▨▨▨▨▨▨▨▨▨▨▨\n")
    while True: 
        stairs_num = int(input("게임을 위한 계단의 개수를 입력해주세요. <10 ~ 30> >> ")) #총 계단 개수 범위에 맞게 입력받음
        if stairs_num >= 10 and stairs_num <= 30:
            break
    os.system('clear')
    print_stairs(stairs_num, player_stairs, com_stairs)
    enter()
    while True: #공격권 결정 가위바위보
        while True: #무승부가 아닌 공격권이 결정될 때까지 공격권 결정 가위바위보 while문을 반복함. 
            print("[공격권 결정 가위바위보]")
            com_choice = computer_choice() #com_choice 변수에 computer_choice() 함수 호출, COMPUTER의 선택을 대입한다.
            user_choice = user_select() #user_choice 변수에 user_select() 함수 호출, USER의 선택을 대입한다.
            
            choice_output(com_choice, user_choice) #user_choice, com_choice를 매개변수로 사용하는 choice_output()을 호출하여 그림을 출력한다.
            
            print("[결과] ", end = '')
            if user_choice == com_choice: #com_choice와 user_choice가 같다면 “무승부”를 출력하고 앞의 과정을 다시 반복한다. 만약 같지 않다면 whowinforrsp()를 호출하여 전역변수 win_num을 1 또는 2로 변경하고 공격권 결정 가위바위보 while문을 종료한다.
                print("무승부입니다.")
                win_num = 0
                enter()
            else:
                whowinforrsp(user_choice, com_choice)
                
            if win_num != 0:
                break
                   
        enter()
        
        while True:
            print("[묵찌빠]")
            print("승리 시 이동 칸 수:", move_num) #move_num 변수를 이용해 승리 시 이동 칸 수를 출력한다.
            whowinforrsp(user_choice, com_choice) #user_choice, com_choice를 매개변수로 사용하는 whowinforrsp()를 호출하여 현재 묵찌빠 공격권을 출력하고 win_num을 변경한다.
            
            com_choice = computer_choice() #com_choice 변수에 computer_choice() 함수 호출, COMPUTER의 선택을 대입한다.
            user_choice = user_select() #user_choice 변수에 user_select() 함수 호출, USER의 선택을 대입한다.
            
            choice_output(com_choice, user_choice) #user_choice, com_choice를 매개변수로 사용하는 choice_output()을 호출하여 그림을 출력한다.
            whowin(user_choice, com_choice) #user_choice, com_choice를 매개변수로 사용하는 whowin()을 호출한다.
        
            if win_num == 4: 
                player_stairs += move_num
                if player_stairs >= stairs_num: #win_num가 4 또는 5가 되면 USER와 COMPUTER의 계단 이동 칸 수를 move_num만큼 증가시키고 만약 이동한 칸 수가 전체 계단의 수보다 많다면 누가 승리했는지를 출력하고 프로그램을 종료한다.
                    player_stairs = stairs_num
                    print_stairs(stairs_num, player_stairs, com_stairs)
                    print("▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨")
                    print("플레이어 최종 승리!!!")
                    print("▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨\n")
                    print("게임을 종료합니다...")
                    exit()
                print_stairs(stairs_num, player_stairs, com_stairs)  # 이동한 칸 수가 전체 계단의 수보다 적다면, 즉 아직 계단의 끝에 도달하지 않았다면 이동 칸 수, move_num을 1 증가시키고 묵찌빠의 처음으로 돌아간다.
                move_num = 1
                enter()
                break
                
            elif win_num == 5:
                com_stairs += move_num
                if com_stairs >= stairs_num:
                    com_stairs = stairs_num
                    print_stairs(stairs_num, player_stairs, com_stairs)
                    print("▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨")
                    print("컴퓨터 최종 승리!!!")
                    print("▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨ ▨\n")
                    print("게임을 종료합니다...")
                    exit()
                print_stairs(stairs_num, player_stairs, com_stairs)
                move_num = 1
                enter()
                break
    
def print_stairs(stairs_num, player_stairs, com_stairs):
    line_list = []
    all_list = []
    print("총 계단 수:", stairs_num)
    print("PLAYER:    ○ < %d>" % player_stairs)
    print("COMPUTER:  ● < %d>\n\n" % com_stairs)
    if stairs_num % 2 == 0: # 계단의 개수가 짝수일 때
        for i in range(int(stairs_num/2)+1):
            line_list += "▨"*i #가로줄의 행이 증가할수록(0,1,2,..,i) 왼쪽 계단은 0,1,2,..,i으로 증가하는 경향을 보이므로 우선 가로줄 리스트에 왼쪽 계단 "▨"을 i개 만큼 추가한다.
            for j in range((stairs_num+1)-2*i):
                line_list += ' ' #가로줄의 왼쪽 계단과 오른쪽 사이의 공백에 (stairs_num+1)-2*i개 만큼, “ “을 추가한다. (스페이스바 한 칸) (맥 OS 기준 "▨"와 “ “가 차지하는 영역은 동일)
            line_list += "▨"*i #가로줄 리스트에 오른쪽 계단 "▨"을 i개 만큼 추가한다.
            all_list.append(line_list) #세로줄 리스트에 방금 생성한 가로줄 리스트 1개를 추가한다.
            line_list = [] # 가로줄 리스트를 []로 초기화한다.
            
        if player_stairs + com_stairs == stairs_num: #컴퓨터와 플레이어의 계단 위치가 같다면 둘의 이동칸수를 더하면 전체 계단의 개수이다.
            if player_stairs > stairs_num/2: #우측
                all_list[stairs_num-player_stairs][player_stairs] = "◑" 
                
            else: #좌측
                all_list[player_stairs][player_stairs] = "◑" 
            
        else:
            if player_stairs > stairs_num/2: #우측
                all_list[stairs_num-player_stairs][player_stairs] = "○"
                
            else: #좌측
                all_list[player_stairs][player_stairs] = "○"
                
            if com_stairs > stairs_num/2: #좌측
                all_list[stairs_num-com_stairs][stairs_num-com_stairs] = "●"
            
            else: #우측
                all_list[com_stairs][stairs_num-com_stairs] = "●"
    else: # 계단의 개수가 홀수일 때
        for i in range(int((stairs_num//2)+2)):
            line_list += "▨"*i
            for j in range((stairs_num+1)-2*i):
                line_list += " "
            line_list += "▨"*i
            all_list.append(line_list)
            line_list = []
            
        if player_stairs + com_stairs == stairs_num:
            if player_stairs >= (stairs_num//2)+1: #우측
                all_list[stairs_num-player_stairs][player_stairs] = "◑" 
            
            else:
                all_list[player_stairs][player_stairs] = "◑"  #좌측
        
        else:
            if player_stairs >= (stairs_num//2)+1: #우측
                all_list[stairs_num-player_stairs][player_stairs] = "○"
            
            else:
                all_list[player_stairs][player_stairs] = "○" #좌측
            
            if com_stairs >= (stairs_num//2)+1: #좌측
                all_list[stairs_num-com_stairs][stairs_num-com_stairs] = "●"
            
            else: #우측
                all_list[com_stairs][stairs_num-com_stairs] = "●"
            
    for k in all_list:
        for p in k:
            print(p, end = '')
        print()
    print("")
    
def computer_choice(): #컴퓨터 가위주먹보 판정
    com_choice = random.choice(["가위", "바위", "보"])
    return com_choice

def print_scissors():
    print("┌────────────────────┐")
    print("│               ▩▩   │")
    print("│       ▩▩    ▩▩▩▩▩  │")
    print("│     ▩▩▩▩▩  ▩▩▩▩▩▩▩ │")
    print("│   ▩▩▩▩▩▩▩▩▩▩▩▩▩▩   │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩▩      │")
    print("│  ▩▩▩▩▩▩▩▩▩         │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩       │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩▩▩     │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩   │")
    print("│   ▩▩▩▩▩▩▩ ▩▩▩▩▩▩▩  │")
    print("│    ▩▩▩▩▩▩   ▩▩▩▩▩  │")
    print("│      ▩▩▩      ▩▩   │")
    print("└────────────────────┘")

def print_rock():
    print("┌────────────────────┐")
    print("│                    │")
    print("│     ▩▩▩▩▩          │")
    print("│    ▩▩▩▩▩▩▩▩▩       │")
    print("│   ▩▩▩▩▩▩▩▩▩▩▩      │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩▩      │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩▩▩     │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩▩▩     │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩▩▩     │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩▩      │")
    print("│   ▩▩▩▩▩▩▩▩▩▩       │")
    print("│    ▩▩▩▩▩▩▩         │")
    print("│                    │")
    print("└────────────────────┘")
    
def print_paper():
    print("┌───────────────────┐")
    print("│                   │")
    print("│     ▩▩▩▩▩         │")
    print("│    ▩▩▩            │")
    print("│   ▩▩▩▩▩▩▩▩▩▩▩▩▩   │")
    print("│  ▩▩▩▩▩▩▩▩▩        │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩  │")
    print("│  ▩▩▩▩▩▩▩▩▩        │")
    print("│  ▩▩▩▩▩▩▩▩▩▩▩▩▩▩   │")
    print("│  ▩▩▩▩▩▩▩▩▩        │")
    print("│   ▩▩▩▩▩▩▩▩▩▩▩     │")
    print("│    ▩▩▩▩▩          │")
    print("│                   │")
    print("└───────────────────┘")

def enter(): #엔터키 입력받았을 때 clear
    while True:
        print("\n계속하려면 엔터를 눌러주세요...")
        enter = input("")
        if enter == "":
            os.system('clear')
            break

def whowinforrsp(user_choice, com_choice): #가위바위보 승리판정 위한 함수
    global win_num
    if user_choice == "가위" and com_choice == "보":
        print("플레이어 공격, 컴퓨터 수비입니다.")
        win_num = 1
    elif user_choice == "바위" and com_choice == "가위":
        print("플레이어 공격, 컴퓨터 수비입니다.")
        win_num = 1
    elif user_choice == "보" and com_choice == "바위":
        print("플레이어 공격, 컴퓨터 수비입니다.")
        win_num = 1
    elif user_choice == "보" and com_choice == "가위":
        print("컴퓨터 공격, 플레이어 수비입니다.")
        win_num = 2
    elif user_choice == "가위" and com_choice == "바위":
        print("컴퓨터 공격, 플레이어 수비입니다.")
        win_num = 2
    else:
        print("컴퓨터 공격, 플레이어 수비입니다.")
        win_num = 2
     
def user_select(): #사용자 가위바위보 선택
    while True:
        user_select = input("가위, 바위, 보 중 하나 선택: ")
        if user_select == '가위' or user_select == '바위' or user_select == '보':
            break
    print("")
    return user_select

def choice_output(com_choice, user_choice): # 그림 출력
    print("[컴퓨터 선택]")
    if com_choice == "가위":
        print_scissors()
    elif com_choice == "바위":
        print_rock()
    else:
        print_paper()
        
    print("[플레이어 선택]")
    if user_choice == "가위":
        print_scissors()
    elif user_choice == "바위":
        print_rock()
    else:
        print_paper()

def whowin(user_choice, com_choice): #묵찌빠 우승 판정 함수
    global win_num
    global move_num
    if win_num == 1: #win_num = 1이라면 USER가 공격권을 지닌다.
        if user_choice == com_choice: #user_choice와 com_choice와 같다면 묵찌빠가 종료되었음을 출력하고 win_num을 4로 변경한다.
            print("[결과] 묵찌빠 종료")
            print("플레이어 승, %d칸 이동합니다." %move_num)
            win_num = 4
        
        else: #user_choce와 com_choice가 같지 않다면 whowinforrsp를 호출하여 승패에 따른 win_num을 변경하고 move_num을 1 증가시킨다
            print("[결과] ", end = '')
            whowinforrsp(user_choice, com_choice)
            move_num += 1
        enter()

    else: #win_num = 2이라면 COMPUTER가 공격권을 지닌다.
        if user_choice == com_choice: #user_choice와 com_choice와 같다면 묵찌빠가 종료되었음을 출력하고 win_num을 5로 변경한다.
            print("[결과] 묵찌빠 종료")
            print("컴퓨터 승, %d칸 이동합니다." %move_num)
            win_num = 5
        else: #user_choce와 com_choice가 같지 않다면 whowinforrsp를 호출하여 승패에 따른 win_num을 변경하고 move_num을 1 증가시킨다
            print("[결과] ", end = '')
            whowinforrsp(user_choice, com_choice)
            move_num += 1
        enter()
main()

