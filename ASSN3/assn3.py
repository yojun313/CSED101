import random
import copy

def posmontoO(first_posmon_index_list, second_posmon_index_list): # 사용자와 컴퓨터의 포스몬을 O/X로 표현하여 반환하는 함수
    Olist = ["X" for i in range(len(first_posmon_index_list))] # 처음에 포스몬의 개수에 맞춰서 X로 이루어진 리스트 생성
    for i in second_posmon_index_list:
        Olist[first_posmon_index_list.index(i)] = "O" # 살아남은 포스몬의 위치에 인덱싱하여 O로 변환
    return ''.join(Olist) # 문자열로 변경 후 반환

def auto_change(battle_posmon, first_posmon_index_list, second_posmon_index_list, posmon_list, posmon_name_list, dead_posmon_list, player): # 포스몬이 쓰러지면 자동으로 다음 포스몬으로 교체하는 함수
    second_posmon_index_list.remove(first_posmon_index_list[posmon_name_list.index(battle_posmon.get_name())])
    posmon_list.remove(battle_posmon)
    battle_posmon.health = 0
    dead_posmon_list.append(battle_posmon) # 쓰러진 포스몬을 모은 리스트에 해당 포스몬 추가
    
    if posmon_list == []: # 포스몬 리스트가 비어있다면
        return battle_posmon # 바꾸지 않고 바로 현재 포스몬을 반환하여 메인 코드에서 게임이 종료되게 함
    
    if player == "com": # com의 포스몬이 자동교체 될 때
        print("컴퓨터 %s: 쓰러짐" % battle_posmon.get_name())
        battle_posmon = posmon_list[0] # battle_posmon에 현재 남은 포스몬 리스트의 가장 첫 번째 포스몬을 대입
        print("컴퓨터 포스몬: %s로 교대" % battle_posmon.get_name())
        
    elif player == "user": # user의 포스몬이 자동교체 될 때
        print("당신의 %s: 쓰러짐" % battle_posmon.get_name())
        battle_posmon = posmon_list[0] 
        print("당신의 포스몬: %s로 교대" % battle_posmon.get_name())
    
    return battle_posmon

class Posmon: # 포스몬 클래스
    def __init__(self, health, max_health, attack, defence, moves, name):
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.initial_attack = attack
        self.defence = defence
        self.initial_defence = defence
        self.moves = moves
        self.name = name
        
    def get_name(self): # 포스몬의 이름을 반환
        return self.name
    
    def get_max_health(self): # 포스몬의 최대 체력을 반환
        return self.max_health
    
    def get_type(self): # 오버라이딩을 통해 구현
        pass
    
    def reset_status(self, reset_health = False): # 포스몬의 공격력 및 방어력을 초기값으로 초기화해주고 reset_health == True이면 체력도 초기화
        self.attack = self.initial_attack 
        self.defence = self.initial_defence
        if reset_health == True:
            self.health = self.max_health
        
class Ponix(Posmon): # Ponix 클래스
    def __init__(self):
        super().__init__(health = 86, max_health = 86, attack = 20, defence = 23, moves = [Tackle(), Growl(), SwordDance()], name = "Ponix")
        self.type = "Paper"
        self.life = True
    
    def get_type(self): # type을 반환
        return self.type

    
class Normie(Posmon):
    def __init__(self):
        super().__init__(health = 80, max_health = 80, attack = 20, defence = 20, moves = [Tackle(), Swift(), TailWhip()], name = "Normie")
        self.type = "Nothing"
        self.life = True
        
    def get_type(self):
        return self.type
    
class Rocky(Posmon):
    def __init__(self):
        super().__init__(health = 80, max_health = 80, attack = 15, defence = 25, moves = [Tackle(), Growl()], name = "Rocky")
        self.type = "Rock"
        self.life = True
        
    def get_type(self):
        return self.type

class Swania(Posmon):
    def __init__(self):
        super().__init__(health = 80, max_health = 80, attack = 30, defence = 10, moves = [ScissorsCross(), SwordDance()], name = "Swania")
        self.type = "Scissors"
        self.life = True
        
    def get_type(self):
        return self.type
    
    
class Move: # 기술의 최상위 클래스
    def __init__(self, name):
        self.name = name
        
    def get_name(self): # 기술의 이름을 반환
        return self.name
    
    def get_speed(self): # 오버라이딩을 통해 구현
        pass
    
    def use(self, our_posmon, opponent_posmon, is_player_move = True): # 오버라이딩을 통해 구현
        pass

class PhysicalMove(Move): # Move 클래스를 상속받은 물리 공격 class
    def __init__(self, power, name):
        super().__init__(name)
        self.power = power
    
    def get_power(self): # power을 반환
        return self.power
    
    def use(self, our_posmon, opponent_posmon, is_player_move = True):
        if our_posmon.get_type() == "Scissors" and opponent_posmon.get_type() == "Paper": # our_posmon, opponent_posmon의 type에 따라 배율을 설정
            self.multiple = 2
        elif our_posmon.get_type() == "Paper" and opponent_posmon.get_type() == "Rock":
            self.multiple = 2
        elif our_posmon.get_type() == "Rock" and opponent_posmon.get_type() == "Scissors":
            self.multiple = 2
        else:
            self.multiple = 1
        
        self.damage = max(0, self.get_power() + our_posmon.attack - opponent_posmon.defence) * self.multiple # 데미지 공식에 따라 데미지 계산
        
        if is_player_move == True: # 사용자가 공격할 때 
            print("- %s 포스몬의 [체력] %d 감소 (%d -> %d)" %("컴퓨터", self.damage, opponent_posmon.health, opponent_posmon.health - self.damage))
        else: # 컴퓨터가 공격할 때
            print("- %s 포스몬의 [체력] %d 감소 (%d -> %d)" %("당신", self.damage, opponent_posmon.health, opponent_posmon.health - self.damage))
        opponent_posmon.health -= self.damage
        
        
        
class Tackle(PhysicalMove): # Tackle 스킬 클래스
    def __init__(self):
        super().__init__(power = 25, name = "Tackle")
        self.speed = 0
    
    def get_speed(self): # speed 반환
        return 0
    
class ScissorsCross(PhysicalMove):
    def __init__(self):
        super().__init__(power = 30, name = "ScissorsCross")
        self.speed = 0
    
    def get_speed(self):
        return 0
    
class Swift(PhysicalMove):
    def __init__(self):
        super().__init__(power = 0, name = "Swift")
        self.speed = 3
    
    def get_speed(self):
        return 3


class StatusMove(Move): # 능쳑치 변환 class
    def __init__(self, name):
        super().__init__(name)

class Growl(StatusMove): # Growl 스킬 class
    def __init__(self, name = "Growl"):
        super().__init__(name)
        self.amount = -5
    
    def get_speed(self): # 스킬 speed 반환
        return 1
    
    def use(self, our_posmon, opponent_posmon, is_player_move = True):
        if opponent_posmon.attack + self.amount == 0: # 줄어든 공격력이 0일 때
            if is_player_move == True:
                print("- %s 포스몬의 [공격력] %d 감소 (%d -> %d)" %("컴퓨터", opponent_posmon.attack, opponent_posmon.attack, 0))
            else:
                print("- %s 포스몬의 [공격력] %d 감소 (%d -> %d)" %("당신", opponent_posmon.attack, opponent_posmon.attack, 0))
            opponent_posmon.attack += self.amount
                
                
        elif opponent_posmon.attack + self.amount < 0: # 줄어든 공격력이 0보다 작을 때
            if is_player_move == True:
                print("- %s 포스몬의 [공격력] %d 감소 (%d -> %d)" %("컴퓨터", 0,0,0))
            else:
                print("- %s 포스몬의 [공격력] %d 감소 (%d -> %d)" %("당신", 0,0,0))
                
        else:
            if is_player_move == True:
                print("- %s 포스몬의 [공격력] %d 감소 (%d -> %d)" %("컴퓨터", self.amount, opponent_posmon.attack, opponent_posmon.attack + self.amount))
            else:
                print("- %s 포스몬의 [공격력] %d 감소 (%d -> %d)" %("당신", self.amount, opponent_posmon.attack, opponent_posmon.attack + self.amount))
            opponent_posmon.attack += self.amount
                
        
        
class SwordDance(StatusMove):
    def __init__(self, name = "SwordDance"):
        super().__init__(name)
        self.amount = 10
    
    def get_speed(self):
        return 0
    
    def use(self, our_posmon, opponent_posmon, is_player_move = True):
        if is_player_move == True:
            print("- %s 포스몬의 [공격력] %d 증가 (%d -> %d)" %("당신", 10, our_posmon.attack, our_posmon.attack + self.amount))
        else:
            print("- %s 포스몬의 [공격력] %d 증가 (%d -> %d)" %("컴퓨터", 10, our_posmon.attack, our_posmon.attack + self.amount))
        our_posmon.attack += self.amount
    
class TailWhip(StatusMove):
    def __init__(self, name = "TailWhip"):
        super().__init__(name)
        self.amount = -5
    
    def get_speed(self):
        return 1
    
    def use(self, our_posmon, opponent_posmon, is_player_move = True):
        if opponent_posmon.defence + self.amount == 0:
            if is_player_move == True:
                print("- %s 포스몬의 [방어력] %d 감소 (%d -> %d)" %("컴퓨터", opponent_posmon.defence, opponent_posmon.defence, 0))
            else:
                print("- %s 포스몬의 [방어력] %d 감소 (%d -> %d)" %("당신", opponent_posmon.defence, opponent_posmon.defence, 0))
            opponent_posmon.defence += self.amount
                
        elif opponent_posmon.defence + self.amount < 0:
            if is_player_move == True:
                print("- %s 포스몬의 [방어력] %d 감소 (%d -> %d)" %("컴퓨터", 0,0,0))
            else:
                print("- %s 포스몬의 [방어력] %d 감소 (%d -> %d)" %("당신", 0,0,0))
                
        else:
            if is_player_move == True:
                print("- %s 포스몬의 [방어력] %d 감소 (%d -> %d)" %("컴퓨터", self.amount, opponent_posmon.defence, opponent_posmon.defence + self.amount))
            else:
                print("- %s 포스몬의 [방어력] %d 감소 (%d -> %d)" %("당신", self.amount, opponent_posmon.defence, opponent_posmon.defence + self.amount))
            opponent_posmon.defence += self.amount


user_posmon_list = []
while True:
    
    print(" ____    ___    _____ ___ ___   ___   ____") # 시작화면 출력
    print("|    \\  /   \\  / ___/|   T   T /   \\ |    \\")
    print("| o   )Y     Y(   \\_ | _   _ |Y     Y|  _  Y")
    print("|   _/ |  O  | \\__  T|  \\_/  ||  O  ||  |  |")
    print("|  |   |     | /  \\ ||   |   ||     ||  |  |")
    print("|  |   l     ! \\    ||   |   |l     !|  |  |")
    print("l__j    \\___/   \\___jl___j___j \\___/ l__j__j")
    print("============================================")
    print("0. 포스몬 선택")
    print("1. 배틀하기")
    print("2. 종료하기")
    print("============================================")
    
    
    
    while True: # 메뉴 번호 입력
        menu_num = input("입력: ")
        if menu_num in ["0", "1", "2"]:
            menu_num = int(menu_num)
            break
        else: # 0, 1, 2 이외의 입력에 대해
            print("잘못된 입력입니다. 다시 입력하세요.")
            
   
    if menu_num == 0: # 포켓몬 입력
        breaknum = 0
        user_posmon_list = []
        while True:
            
            print("\n============================================")
            print("당신이 사용할 포스몬을 선택하세요. 현재 %d 마리/최대 3마리" % len(user_posmon_list))
            print("0. Ponix")
            print("1. Normie")
            print("2. Swania")
            print("3. Rocky")
            if len(user_posmon_list) >= 1: # 포스몬 리스트에 포스몬이 추가되는 순간 -1. 그만두기 출력
                print("-1. 그만두기")
            print("============================================")
            
            while True:
                
                if len(user_posmon_list) == 3: # 포스몬 리스트가 3마리가 되면 반복문 탈출
                    breaknum = 1
                    break
                
                posmon_select = input("입력: ")
                if posmon_select == "0": 
                    user_posmon_list.append(Ponix()) # 해당 포스몬의 클래스를 생성자로 생성, 리스트에 추가
                    break
                
                elif posmon_select == "1":
                    user_posmon_list.append(Normie())
                    break
                
                elif posmon_select == "2":
                    user_posmon_list.append(Swania())
                    break
                
                elif posmon_select == "3":
                    user_posmon_list.append(Rocky())
                    break
                
                elif posmon_select == "-1":
                    if len(user_posmon_list) == 0:
                        print("잘못된 입력입니다. 다시 입력하세요.")
                    else:
                        breaknum = 1
                        break
                else:
                    print("잘못된 입력입니다. 다시 입력하세요.")
            
            if breaknum == 1:
                break
        print("\n============================================")
        print("당신의 포스몬 목록:", *[i.get_name() for i in user_posmon_list])
        print("============================================\n\n")

    elif menu_num == 1:
        user_dead_posmon_list = []
        com_dead_posmon_list = []
        
        posmon_num_list = [0,1,2,3]
        if len(user_posmon_list) == 0: # 포스몬 리스트가 비어있을 때 
            print("\n싸울 포스몬이 없습니다! 먼저 포스몬을 선택해주세요.\n\n")
        else: 
            com_posmon_list = []
            for i in range(3): # 컴퓨터 포스몬 리스트에 포스몬 랜덤으로 추가(생성자 사용)
                posmon = random.choice(posmon_num_list)
                if posmon == 0:
                    com_posmon_list.append(Ponix())
                elif posmon == 1:
                    com_posmon_list.append(Normie())
                elif posmon == 2:
                    com_posmon_list.append(Swania())
                else:
                    com_posmon_list.append(Rocky())
                posmon_num_list.remove(posmon)
                    
            com_posmon_name_list, user_posmon_name_list = [i.name for i in com_posmon_list], [i.name for i in user_posmon_list] # 컴퓨터/사용자 포스몬 보관하는 리스트
            first_com_posmon_index_list, first_user_posmon_index_list = [i for i in range(len(copy.deepcopy(com_posmon_list)))], [i for i in range(len(copy.deepcopy(user_posmon_list)))] # 컴퓨터/사용자 처음 포스몬의 인덱스 번호(위치)를 보관하는 리스트
            second_com_posmon_index_list, second_user_posmon_index_list = copy.deepcopy(first_com_posmon_index_list), copy.deepcopy(first_user_posmon_index_list) # 포스몬 상태(쓰러짐)변화에 따라 포스몬의 인덱스 번호(위치)를 보관하는 리스트
            
            com_battle_posmon, user_battle_posmon = com_posmon_list[0], user_posmon_list[0]
            
            print("\n============================================")
            print("당신의 포스몬 목록:", *[i.get_name() for i in user_posmon_list])
            print("컴퓨터 포스몬 목록:", *[i.get_name() for i in com_posmon_list])
            print("============================================")
            print("\n배틀이 시작됩니다.")
            
            while True:  # 배틀 반복문
                user_battle_posmon_skill_list = ["("+str(user_battle_posmon.moves.index(i))+") "+i.get_name() for i in user_battle_posmon.moves]
                print("############################################") # 컴퓨터, 사용자의 battle_posmon 상태 출력
                print("컴퓨터 포스몬: ["+ posmontoO(first_com_posmon_index_list, second_com_posmon_index_list) +"] " + str(len(com_posmon_list)) + " / 3")
                print("%s               <|%s %d / %d|" % (com_battle_posmon.get_name().ljust(8), com_battle_posmon.get_type().ljust(8), com_battle_posmon.health, com_battle_posmon.get_max_health()))
                print("                  VS")
                print("%s               <|%s %d / %d|" % (user_battle_posmon.get_name().ljust(8), user_battle_posmon.get_type().ljust(8), user_battle_posmon.health, user_battle_posmon.get_max_health()))
                print("당신의 포스몬: ["+ posmontoO(first_user_posmon_index_list, second_user_posmon_index_list) +"] " + str(len(user_posmon_list)) + " / " + str(len(first_user_posmon_index_list)))
                print("++++++++++++++++++++++++++++++++++++++++++++")
                print("기술:", *user_battle_posmon_skill_list)
                print("############################################")

                if len(user_posmon_list) == 0: # 사용자 포스몬 리스트가 비어있을 때
                    print("[배틀 결과] 컴퓨터가 이겼습니다.")
                    user_posmon_list = []
                    break #게임 종료
                    
                elif len(com_posmon_list) == 0: # 컴퓨터 포스몬 리스트가 비어있을 때
                    print("[배틀 결과] 당신이 이겼습니다.")
                    user_posmon_list = []
                    break
            
                while True: # 사용자 명령 입력받기
                    user_input = input("입력: ").split()
                    if user_input == ["e"]: # 사용자 명령이 e일 때
                        print("############################################")
                        for i in range(len(user_posmon_list)): # 살아있는 포스몬 출력
                            print("(%d) %s   <|%s %d / %d|" % (i, user_posmon_list[i].get_name().ljust(8), user_posmon_list[i].get_type().ljust(8), user_posmon_list[i].health, user_posmon_list[i].get_max_health()))
                        for j in range(len(user_dead_posmon_list)): # 쓰러진 포스몬 출력
                            print("(%d) %s   <|%s %d / %d|" % (j+i+1, user_dead_posmon_list[j].get_name().ljust(8), user_dead_posmon_list[j].get_type().ljust(8), user_dead_posmon_list[j].health, user_dead_posmon_list[j].get_max_health()))
                    
                        print("")
                    else:
                        user_input[1] = int(user_input[1])
                        if user_input[0] == "o":
                            if user_input[1] <= len(user_battle_posmon.moves) - 1: # 입력한 스킬 번호가 포스몬 스킬 리스트에 존재할 때
                                break
                            else:
                                print("선택할 수 없는 기술입니다!")
                        elif user_input[0] == "s":
                            if user_input[1] <= len(user_posmon_list) - 1 and user_posmon_list[user_input[1]] != user_battle_posmon: # 교체 가능한 포켓몬에 대한 검증
                                break
                            else:
                                print("포켓몬을 교대시킬 수 없습니다!")
                        else:
                            print("잘못된 명령어:", *user_input)

            
                if user_input[0] == "o": # 사용자 명령이 o일 때
                    print("############################################")
                    
                    com_posmon_skill = random.choice(com_battle_posmon.moves)
                    user_posmon_skill = user_battle_posmon.moves[user_input[1]]
                    
                    if user_posmon_skill.get_speed() >= com_posmon_skill.get_speed(): # 사용자 배틀 포스몬의 스킬 속도가 컴퓨터의 것보다 빠를 때
                        
                        print("당신의 %s: %s 기술 사용" %(user_battle_posmon.get_name(), user_posmon_skill.get_name()))
                        user_posmon_skill.use(user_battle_posmon, com_battle_posmon) # 사용자 배틀 포스몬 공격 시전
                        
                        if com_battle_posmon.health <= 0: # 컴퓨터 포스몬의 체력이 0 이하일 때
                            com_battle_posmon = auto_change(com_battle_posmon, first_com_posmon_index_list, second_com_posmon_index_list, com_posmon_list, com_posmon_name_list, com_dead_posmon_list, "com") # 컴퓨터 포스몬 자동 교체 시전
                        
                        else:
                            print("컴퓨터 %s: %s 기술 사용" %(com_battle_posmon.get_name(), com_posmon_skill.get_name()))
                            com_posmon_skill.use(com_battle_posmon, user_battle_posmon, False) # 컴퓨터 배틀 포스몬 공격 시전
                            
                            if user_battle_posmon.health <= 0: # 사용자 포스몬의 체력이 0 이하일 때
                                user_battle_posmon = auto_change(user_battle_posmon, first_user_posmon_index_list, second_user_posmon_index_list, user_posmon_list, user_posmon_name_list, user_dead_posmon_list, "user") # 사용자 포스몬 자동 교체 시전
                
                    else:
                        print("컴퓨터 %s: %s 기술 사용" %(com_battle_posmon.get_name(), com_posmon_skill.get_name()))
                        com_posmon_skill.use(com_battle_posmon, user_battle_posmon, False)
                        
                        if user_battle_posmon.health <= 0:
                            user_battle_posmon = auto_change(user_battle_posmon, first_user_posmon_index_list, second_user_posmon_index_list, user_posmon_list, user_posmon_name_list, user_dead_posmon_list, "user")
                        
                        else:
                            print("당신의 %s: %s 기술 사용" %(user_battle_posmon.get_name(), user_posmon_skill.get_name()))
                            user_posmon_skill.use(user_battle_posmon, com_battle_posmon)
                            
                            if com_battle_posmon.health <= 0:
                                com_battle_posmon = auto_change(com_battle_posmon, first_com_posmon_index_list, second_com_posmon_index_list, com_posmon_list, com_posmon_name_list, com_dead_posmon_list, "com")
                    print("")
                    
                else: # s를 고를 때
                    print("############################################")
                    user_battle_posmon = user_posmon_list[user_input[1]] # 사용자 배틀 포스몬 그 다음 포스몬으로 변경
                    user_battle_posmon.reset_status(False)
                    print("당신의 포스몬 %s로 교대" % user_battle_posmon.get_name())
                    
                    com_posmon_skill = random.choice(com_battle_posmon.moves) # 컴퓨터 배틀 포스몬 랜덤으로 결정
                    print("컴퓨터 %s: %s 기술 사용" %(com_battle_posmon.get_name(), com_posmon_skill.get_name()))
                    com_posmon_skill.use(com_battle_posmon, user_battle_posmon, False) # 컴퓨터 배틀 포스몬 스킬 시전
                    
                    if user_battle_posmon.health <= 0: # 사용자 배틀 포스몬 체력 0 이하로 떨어질 때
                        user_battle_posmon = auto_change(user_battle_posmon, first_user_posmon_index_list, second_user_posmon_index_list, user_posmon_list, user_posmon_name_list, "user") # 사용자 배틀 포스몬 자동 교체
                    
                    print("")
    else:
        break               
                    
                        

                    
                     
