import random
import os

def main():
    category_list = ["1", "2", "3", "4", "5", "6", "c", "4k", "fh", "ss", "ls", "y"]
    while True:
        
        print("[Yacht Dice]") # 실행 화면
        print("----------------------------------")
        print("1. New Game 2. Load Game 3. Exit")
        print("----------------------------------")
        while True: # 프로그램 초기화면 입력받는 부분
            score_list = [["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""]] # score_list 초기화
            while True:
                try:
                    menu_num = int(input("Select a menu: "))
                    break
                except: # 문자열 등 정수를 입력하지 않았을 때
                    print("Wrong Input!\n\n")
                
            if menu_num == 1: # new game 선택
                turn_num = 1
                clear_screen() 
                break
            elif menu_num == 2: # load game 선택, 파일 불러오고 menu_num == 1(게임 플레이) 코드로 넘어감
                while True:
                    filename = input("\n\nEnter filename to load: ")
                    if os.path.isfile(filename) == True: # 파일이 존재할 때
                        score_list = load_file2list(filename) # 텍스트 파일을 score_list 리스트로 변환
                        if check_error(score_list) == False: # 파일 형태에 문제가 없을 때
                            menu_num = 1 # 게임 시작하기 위해
                            turn_num = 2
                            for i in score_list: # score_list에서 점수가 적힌 부분의 개수를 셈
                                for j in i:
                                    if type(j) == int:
                                        turn_num += 1
                            turn_num /= 2
                            break
                        else:
                            print("Invalid file content.")
                    else:
                        print("File does not exist.")
                clear_screen()
                break     
            elif menu_num == 3:
                print("Program ended. Bye!")
                break
            else:
                print("Wrong Input!\n\n")
            
        turn = 1 # 사용자 먼저 시작
        quitnum = 1 # Q를 입력했을 때 루프를 빠져나오기 위한 인자
        
        if menu_num == 1:
            print("\n\nStarting a game...")
            print_score_board(score_list)
            while True: 
                
                if turn_num > 12: # score_list가 12칸이 다 찼을 때 게임 종료
                    print("<Final Score Board>")
                    print_score_board(score_list)
                    
                    if player_total > computer_total:
                        print("You win!")
                    elif computer_total > player_total:
                        print("You lose!")
                    else:
                        print("Draw")
                    
                    enterinput = input("\nPress Enter to continue...")
                    if enterinput == "":
                        clear_screen()
                        break
                
                if turn == 1: # 사용자 먼저 시작
                    print("\n[Player's Turn (%d/12)]" % turn_num)

                    dice_set = roll_dice() # 처음 주사위를 굴림
                    print("Roll:", dice_set)
                    
                    for i in range(2): # 주사위 두 번 더 던지기
                        while True:  # 다시 던질 주사위 위치 입력받기
                            reroll_indices = list(set(input("Which dice to reroll (1~5)? ").split()))
                            
                            if reroll_indices == []: # 엔터 입력하면 빠져나가기
                                break
            
                            elif reroll_indices[0].lower() == "q": # 사용자가 게임 도중에 중단할 때
                                quitnum = file_save(category_list, score_list) # score_list를 텍스트 파일로 저장한 뒤 quit_num에 0 대입해서 루프문 탈출
                                break
                                         
                            else: 
                                try: 
                                    reroll_indices = [int(str) for str in reroll_indices] # 리스트에 있는 숫자를 정수형으로 변환
                                    reroll_indices.sort()
                                    break
                                except: # 리스트에 있는 문자가 숫자가 아닐 때
                                    print("Wrong input!")

                        if quitnum == 0: # input == "Q"일 때 루프 탈출
                            break
                                
                        dice_set = roll_dice(dice_set, reroll_indices)
                        print("Roll:", dice_set)
                    
                    if quitnum == 0:
                        break
                    
                    dice_set.sort()
                    print("\nSorted Roll:", dice_set) # 최종 주사위 정렬한 후 출력
                
                    while True: # 카테고리 번호 입력받기
                        category_word = input("Choose a category: ").lower() # category_list가 소문자로만 이루어져 있기 때문에 어떤 문자든 소문자로 바꿔줌

                        if category_word in category_list: # 입력한 문자가 category_list 안에 있을 때
                            if score_list[category_list.index(category_word)][0] != "": # 이미 점수 리스트에 값이 입력되어있을 때 wrong input 출력
                                print("Wrong Input!")
                            else:
                                break
                        elif category_word == "q": # 중단을 위해 입력창에 Q을 입력했을 때
                            quitnum = file_save(category_list, score_list)
                            break
                        else: # 입력한 문자가 category_list 안에 없을 때
                            print("Wrong Input!")
  
                    if quitnum == 0: # input == "Q"일 때 루프 탈출
                        break
                    
                    score_list[category_list.index(category_word)][0] = calc_score(dice_set, category_word) # 점수 리스트에 calc_score를 통해 계산한 값 대입
                    print_score_board(score_list)
                    clear_screen()
                    turn = 2 # 컴퓨터 차례로 넘어감
                
                elif turn == 2: # 컴퓨터 차례
                    print("[Computer's Turn (%d/12)]" % turn_num)
                    
                    dice_set = roll_dice()
                    print("Roll:", dice_set)
                    
                    for i in range(2): 
                        sel, reroll_indices = computer_pattern(dice_set, score_list, category_list) # computer_pattern 함수를 통해 최대의 점수를 낼 수 있는 다시 굴리기 주사위 조합(reroll_indices)와 입력할 점수 항목 반환
                        reroll_indices.sort()
                        print("Which dice to reroll (1~5)?", *reroll_indices)
                        dice_set = roll_dice(dice_set, reroll_indices) # reroll_indices를 인자로 줘서 주사위를 굴림
                        print("Roll:", dice_set)
                    
                    dice_set.sort()
                    sel, reroll_indices = computer_pattern(dice_set, score_list, category_list) # 최종 sel 업데이트

                    print("\nSorted Roll:", dice_set) # 정렬된 주사위 출력
                    print("Choose a category:", sel) # 입력할 점수 항목 출력
                    
                    score_list[category_list.index(sel)][1] = calc_score(dice_set, sel) # 점수 리스트에 calc_score를 통해 계산한 값 대입
                    print_score_board(score_list)
                    print("\n\n")
                    
                    turn_num += 1
                    turn = 1

        elif menu_num == 3: # 3번 메뉴를 선택했을 때 프로그램 종료
            exit()
                         
def print_score_board(score_list): # 보고서 기록
    global player_total # total은 다른 함수 내에서도 쓰이므로 전역변수 처리
    global computer_total
    
    player_35 = 0
    computer_35 = 0
    player_subtotal = 0
    computer_subtotal = 0
    player_total = 0
    computer_total = 0
    
    for i in range(6): # subtotal을 계산하는 loop
        try:
            player_subtotal += score_list[i][0]
        except: # score_list가 채워져있지 않은 항목일 때, 즉 문자열("")일 때 player_35를 공백으로 비워둠 / 이 부분이 실행되지 않는다면 score_list가 다 채워져있다는 의미이므로 초기값 0으로 유지됨
            player_35 = "   "
            pass
    
    for i in range(6):
        try:
            computer_subtotal += score_list[i][1]
        except:
            computer_35 = "   "
            pass
        
    for i in range(12): # total을 계산하는 loop
        try:
            player_total += score_list[i][0]
        except: # 위와 마찬가지로 score_list가 채워져있지 않은 항목일 때
            pass
        
    for i in range(12):
        try:
            computer_total += score_list[i][1]
        except:
            pass
    
    if player_subtotal >= 63: # player_subtotal이 63보다 크면 +35를 대입
        player_35 = "+35"
        player_total += 35
        
    if computer_subtotal >= 63:
        computer_35 = "+35"
        computer_total += 35
    
    print("┌────────────────────┬────────────────────┐")
    print("│       Player       │      Computer      │")
    print("├────────────────────┴────────────────────┤")
    print("│ 1:         %2s      │ 1:         %2s      │"%(score_list[0][0],score_list[0][1]))
    print("│ 2:         %2s      │ 2:         %2s      │"%(score_list[1][0],score_list[1][1]))
    print("│ 3:         %2s      │ 3:         %2s      │"%(score_list[2][0],score_list[2][1]))
    print("│ 4:         %2s      │ 4:         %2s      │"%(score_list[3][0],score_list[3][1]))
    print("│ 5:         %2s      │ 5:         %2s      │"%(score_list[4][0],score_list[4][1]))
    print("│ 6:         %2s      │ 6:         %2s      │"%(score_list[5][0],score_list[5][1]))
    print("├─────────────────────────────────────────┤")
    print("│ Sub total: %3d/63  │ Sub total: %3d/63  │"%(player_subtotal,computer_subtotal))
    print("│ +35 bonus: %3s     │ +35 bonus: %3s     │"%(player_35,computer_35))
    print("├─────────────────────────────────────────┤")
    print("│ C:        %2s       │ C:        %2s       │"%(score_list[6][0],score_list[6][1]))
    print("├─────────────────────────────────────────┤")
    print("│ 4K:        %2s      │ 4K:        %2s      │"%(score_list[7][0],score_list[7][1]))
    print("│ FH:        %2s      │ FH:        %2s      │"%(score_list[8][0],score_list[8][1]))
    print("│ SS:        %2s      │ SS:        %2s      │"%(score_list[9][0],score_list[9][1]))
    print("│ LS:        %2s      │ LS:        %2s      │"%(score_list[10][0],score_list[10][1]))
    print("│ Yaucht:    %2s      │ Yaucht:    %2s      │"%(score_list[11][0],score_list[11][1]))
    print("├─────────────────────────────────────────┤")
    print("│ Total:    %3d      │ Total:    %3d      │"%(player_total, computer_total))
    print("└─────────────────────────────────────────┘")
    
    return player_total, computer_total
    
def roll_dice(dice_set = [], reroll_indices = []): # 보고서 기록
    dice = []
    if dice_set == []: # 주사위를 처음 굴릴 때
        for i in range(5):
            dice.append(random.randint(1,6))
        return dice
    else: # 주사위를 처음 굴리지 않을 때, 즉 다시 굴릴 때
        for i in range(1,6): # 굴릴 주사위 항목이 1에서 5이면(1~5 범위 바깥의 숫자가 입력되었을 때 주사위를 굴리는 것을 방지)
            if i in reroll_indices:
                dice.append(random.randint(1,6))
            else:
                dice.append(dice_set[i-1])
        return dice

def calc_score(dice_set, sel): # 주사위 조합과 채울 항목(sel)을 입력할 때 점수를 반환하는 함수 # 보고서 기록
    if sel in ["1", "2", "3", "4", "5", "6"]: # sel이 숫자이면 그 숫자에 해당하는 주사위 개수에 그 숫자를 곱한 만큼의 점수를 반환
        return int(sel)*dice_set.count(int(sel))
    
    elif sel == "c": # sel이 choice이면 모든 주사위 눈의 합 반환
        return sum(dice_set)
    
    elif sel == "4k":
        for i in dice_set: 
            if dice_set.count(i) >= 4: # 모든 주사위에 대해서 그 주사위의 개수가 4개 이상일 때
                return sum(dice_set) # 모든 주사위 눈의 합 반환
        return 0
    
    elif sel == "fh":
        newlist = list(set(dice_set)) # 중복 요소 제거한 리스트
        if len(newlist) == 2: # 3개 2개이면 중복 제거했을 때 2개만 남게된다.
            if dice_set.count(newlist[0]) == 3 or dice_set.count(newlist[1]) == 3: # 중복 요소한 리스트의 원소 개수가 dice_set에서 3개, 2개로 되어있는지 확인 (4개, 1개로 되어있을 때 처리되는 것을 방지)
                return sum(dice_set)
            else:
                return 0
        elif len(newlist) == 1: # 모든 주사위가 같을 때도 포함
            return sum(dice_set)
        else: # 중복 요소 제거한 리스트 길이가 2개가 아니라면 0 반환
            return 0
            
    elif sel == "ss":
        count = 1
        for i in range(1, 5):
            if i == 4 and count == 4: # [1,2,3,4,6]의 경우 밑에서 count = 1로 초기화될 수 있기 때문에 loop문이 끝까지 돌고 count가 4(연속된 숫자가 4개)인 경우 loop문 미리 탈출
                break
            elif dice_set[i] == dice_set[i - 1] + 1: # 앞의 숫자와 뒤의 숫자가 1차이 날 때
                count += 1 # count에 1 추가
            else: # [1,2,4,5,6]을 예로 들 때 1,2 까지는 count가 1씩 증가하다가 2->4를 만나는 순간 연속 조건이 깨지므로 count 초기화
                count = 1
        if count >= 4: # 연속된 숫자가 4개 이상일 때
            return 15
        else:
            return 0
    
    elif sel == "ls":
        count = 1
        for i in range(1, 5):
            if dice_set[i] == dice_set[i - 1] + 1:
                count += 1
            else:
                count = 1
        if count == 5:
            return 30
        else:
            return 0

    elif sel == "y":
        if len(list(set(dice_set))) == 1: # 모든 주사위의 눈이 같으면 중복을 제거한 리스트의 길이가 1개
            return 50
        else:
            return 0

def computer_pattern(dice_set, score_list, category_list): # 보고서 기록
    expected_score_list = [] # dice_set로 만들 수 있는 모든 항목의 점수 기댓값을 모으는 리스트
    reroll_indices = [] # 다시 굴릴 주사위 리스트
    for sel in category_list: # category_list의 항목에 대해서
        expected_score = calc_score(sorted(dice_set), sel) # 기댓값을 calc_score 함수를 통해 계산
        if score_list[category_list.index(sel)][1] == "": # 점수판에서 채워지지 않은 칸을 고를 때, 즉 신규 칸을 고를 때
            if sel == "c": # 루프문에서 항목이 "c"일 때, choice는 total이 20이상일 때만 고려해야 한다.
                if expected_score < 20:
                    testlist = [i[1] for i in score_list]
                    if testlist.count("") == 1:
                        expected_score_list.append(expected_score)
                    else:
                        expected_score_list.append(-1)
                else:
                    expected_score_list.append(expected_score)
            else:  
                expected_score_list.append(expected_score) # 항목이 "c"가 아닐 때 기댓값 추가
        else:
            expected_score_list.append(-1)  # 점수판에서 이미 채워진 칸을 고를 때 -1값(다른칸에서는 나올 수 없는 기댓값)을 줌으로써 가장 높은 점수를 만들 수 있는 칸에 해당될 수 없게한다.
    
    max_expected_index_list = [i for i, value in enumerate(expected_score_list) if value == max(expected_score_list)] # 기댓값 리스트에서 가장 큰 수의 인덱스를 모은 리스트
    sel = category_list[random.choice(max_expected_index_list)] # 가장 높은 점수가 2개 이상일 경우 랜덤으로 하나를 뽑아서 그 인덱스를 sel에 대입                ################여기까지 가장 기댓값이 큰 sel을 결정하는 과정
    #print("Sel:", sel)
    if sel in ["1", "2", "3", "4", "5", "6"]: 
        reroll_indices = [i+1 for i in range(5) if dice_set[i] != int(sel)]
        return sel, reroll_indices

    elif sel == "c":
        for i in range(5): # i는 주사위의 눈
            if dice_set[i] <= 3: # 주사위의 눈이 3보다 작을 때 reroll_indices에 그 주사위의 인덱스를 추가함
                reroll_indices.append(i+1)
        return sel, reroll_indices
    
    else:  # sel이 ["4k", "fh", "ss", "ls", "y"] 안에 있을 때
        if expected_score_list[category_list.index(sel)] == 0:
            reroll_indices = [1,2,3,4,5]
        else:
            reroll_indices = [] # 주사위를 굴리지 않음
        return sel, reroll_indices
        
def clear_screen(): # 보고서 기록
    try:
        os.system('clear')
    except:
        os.system('cls')    
             
def file_save(category_list, score_list): # Q입력했을 때 파일 저장하는 함수 및 끝났을 때 파일 저장하는 함수
    
    quitnum = 0
    print("\n\nGame paused. Enter the filename to save:")
    filename = input("")
    
    for i in range(len(score_list)):
        for j in range(2):
            if score_list[i][j] == "":
                score_list[i][j] = "x"  # score_list가 공란일 때 "x"로 변경
    
    with open(filename, 'w+') as file:
        indexnum = 0
        for i in score_list:
            file.write("%s: %s %s\n" %(category_list[indexnum].upper(), i[0], i[1])) # 이 형태로 파일 저장
            indexnum += 1
            
    print("File saved.\n")
    return quitnum

def load_file2list(filename):  # 보고서 기록
    with open(filename, "r") as file:
        text = file.readlines() # 파일 텍스트 전체를 리스트로 변환
        indexlist = ["1", "2", "3", "4", "5", "6", "c", "4k", "fh", "ss", "ls", "y"]
        scorelist = [["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""]]
        for i in text:
            i = i.split() 
            for k in range(1,3):
                if i[k] == "x":
                    i[k] = ""
                else:
                    try: 
                        i[k] = int(i[k])
                    except:
                        pass
            rowlist = [i[1],i[2]]
            if i[0][:-1].lower() in indexlist: 
                scorelist[indexlist.index(i[0][:-1].lower())] = rowlist
            else: # indexlist에 없는 인덱스가 들어왔을 때
                scorelist.append(rowlist)
        return scorelist
    
def check_error(score_list): # 보고서 기록
    checklist = []
    if len(score_list) == 12: 
        if score_list[0][0] in [""]+[i for i in range(6)] and score_list[0][1] in [""]+[i for i in range(6)]: # [1]: 0,1,2,3,4,5, ""
            checklist.append(1)
        if score_list[1][0] in ["",0,2,4,6,8,10] and score_list[1][1] in ["",0,2,4,6,8,10]: # [2]: 0,2,4,6,8,10, ""
            checklist.append(2)
        if score_list[2][0] in ["",0,3,6,9,12,15] and score_list[2][1] in ["",0,3,6,9,12,15]: # [3]: 0,3,6,9,12,15, ""
            checklist.append(3)
        if score_list[3][0] in ["",0,4,8,12,16,20] and score_list[3][1] in ["",0,4,8,12,16,20]: # [4]: 0,4,8,12,16,20, ""
            checklist.append(4)
        if score_list[4][0] in ["",0,5,10,15,20,25] and score_list[4][1] in ["",0,5,10,15,20,25]: # [5]: 0,5,10,15,20,25, ""
            checklist.append(5)
        if score_list[5][0] in ["",0,6,12,18,24,30] and score_list[5][1] in ["",0,6,12,18,24,30]: # [6]: 0,6,12,18,24,30, ""
            checklist.append(6)
        if score_list[6][0] in [""]+[i for i in range(31)] and score_list[6][1] in [""]+[i for i in range(31)]: # [C]: 0~30, ""
            checklist.append(7)
        if score_list[7][0] in ["",0]+[i for i in range(5,31)] and score_list[7][1] in ["",0]+[i for i in range(5,31)]: # [4K]: 0, 5~30, ""
            checklist.append(8)
        if score_list[8][0] in ["",5,30]+[i for i in range(7,29)] and score_list[8][1] in ["",5,30]+[i for i in range(7,29)]: # [FH]: 5, 7~28, 30, ""
            checklist.append(9)
        if score_list[9][0] in ["",0,15] and score_list[9][1] in ["",0,15]: # [SS]: 0, 15, ""
            checklist.append(10)
        if score_list[10][0] in ["",0,30] and score_list[10][1] in ["",0,30]: # [LS]: 0, 30, ""
            checklist.append(11)
        if score_list[11][0] in ["",0,50] and score_list[11][1] in ["",0,50]: # [Y]: 0, 50, ""
            checklist.append(12)
        
        if len(checklist) == 12: # 위에서 항목이 유효하면 리스트에 숫자를 하나씩 추가하고 모든 항목이 유효할 때(리스트의 길이가 12일 때)
            return False
        else:
            return True
    else: # 점수판이 12칸이 아닐 때
        return True

main()

