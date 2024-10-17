import random

class Panel:
    def __init__(self, isRevealed = False, hasFlag = False):
        self.isRevealed = isRevealed # instance 생성 시 False로 초기화
        self.hasFlag = hasFlag # instance 생성 시 False로 초기화

    def toggleFlag(self):
        if self.hasFlag == False: # 토글 기능 구현
            self.hasFlag = True
        else:
            self.hasFlag = False

    def unveil(self): 
        self.isRevealed = True # isRevealed 값 True로 변경
        

class EmptyPanel(Panel):
    def __init__(self):
        super().__init__(isRevealed = False, hasFlag = False)
        self.numOfNearMines = 0 # instance 생성 시 0으로 초기화
    
    def addNumOfNearMines(self):
        self.numOfNearMines += 1 # panel의 numOfNearMines의 값 1 증가

    def unveil(self):
        self.isRevealed = True # Panel unveil 수행
        return self.numOfNearMines # 인접한 mine의 수 반환
    
    def get_name(self): # EmptyPanel임을 알려주는 함수
        return "Empty"


class MinePanel(Panel):
    def __init__(self):
        super().__init__(isRevealed = False, hasFlag = False)
    
    def unveil(self):
        self.isRevealed = True # Panel unveil 수행
        return -1 # -1 return
    
    def get_name(self): # MinePanel임을 알려주는 함수
        return "Mine"


class Board:
    def __init__(self):
        self.panels = [[]] # Panel을 2차원 리스트로 저장하는 instance
        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] # 중심 Panel로부터 주변 8개의 지뢰 좌표를 담은 리스트
        self.newcoordinatelist = [] # newcoordinatelist는 unveil 함수에서 체크한 panel의 좌표를 저장하는 리스트, 
    
    def reset(self, numMine, height, width):
        self.panels, coordinate_list = [["" for j in range(width)] for i in range(height)], [[j, i] for i in range(height) for j in range(width)]
        # Panels 2차원 리스트로 초기화, 좌표 2차원 리스트로 초기화
        
        for i in range(numMine):
            mine_coordinate = random.choice(coordinate_list) # 지뢰를 넣을 좌표 위치 랜덤으로 선택
            self.panels[mine_coordinate[1]][mine_coordinate[0]] = MinePanel() # 해당 좌표의 panel에 MinePanel 객체 대입
            coordinate_list.remove(mine_coordinate) # 같은 좌표가 중복해서 걸리지 않도록 coordinate_list에서 해당 좌표 삭제
        
        for i in range(height):
            for j in range(width):
                if self.panels[i][j] == "": # panels의 리스트에서 칸이 비어있으면, 즉 지뢰가 없으면
                    self.panels[i][j] = EmptyPanel() # 그 칸에 EmptyPanel 객체 대입
        
        for i in range(height):
            for j in range(width):
                if self.panels[i][j].get_name() == "Empty": # EmptyPanel일 때
                    for plusy, plusx in self.directions: # 비어있는 칸 주변 8칸에 대하여
                        newy, newx = i + plusy, j + plusx
                        if 0 <= newy <= height-1 and 0 <= newx <= width-1:
                            if self.panels[newy][newx].get_name() == "Mine": # 해당 칸이 지뢰이면
                                self.panels[i][j].addNumOfNearMines() # addNumOfNearMines 함수 실행
                
    def getNumOfRevealedPanels(self):
        num = 0
        for i in self.panels:
            for j in i:
                if j.isRevealed == True: # 모든 패널에 대해서 해당 패널이 밝혀져 있으면
                    num += 1 # 숫자 1 더하기
        return num
    

    def unveil(self, y, x):
        
        self.panels[y][x].unveil() # 인자로 받은 좌표에 위치한 panel unveil 수행
        
        if self.panels[y][x].get_name() == "Mine": # 해당 좌표의 panel이 지뢰 패널일 경우 
            return -1 # -1 반환
        
        else:
            if self.panels[y][x].numOfNearMines == 0: # y행 x열의 위치한 panel의 numOfNearMines의 값이 0일 때
                for plusy, plusx in self.directions: # 이 panel의 인접한 8칸에 대하여
                    newy, newx = y + plusy, x + plusx
                    if [newy, newx] not in self.newcoordinatelist: # 반복 체크를 피하기 위해서 검사 안 한 좌표에 대해서만 코드 실행
                        if 0 <= newy <= len(self.panels)-1 and 0 <= newx <= len(self.panels[0])-1:
                            if self.panels[newy][newx].get_name() != "Mine":  # 지뢰가 없는 칸일 때
                                if self.panels[newy][newx].hasFlag == True: # 깃발이 있는경우
                                    self.panels[newy][newx].toggleFlag() # 깃발을 제거하고
                                self.newcoordinatelist.append([newy, newx]) # newcoordinatelist에 해당 좌표 추가
                                self.unveil(newy, newx) # unveil() 함수 반복 실행(재귀함수)

    def toggleFlag(self, y, x): 
        self.panels[y][x].toggleFlag() # panels의 y행 x열에 위치한 Panel의 flag toggle

    def checkReveal(self, y, x): 
        return self.panels[y][x].isRevealed # panels의 y행 x열에 위치한 Panel이 밝혀져 있는지 확인 후 반환

    def checkFlag(self, y, x): 
        return self.panels[y][x].hasFlag # panels의 y행 x열에 위치한 Panel에 flag가 있는지 확인

    def checkMine(self, y, x): 
        if self.panels[y][x].get_name() == "Mine": # panels의 y행 x열에 위치한 Panel에 Mine이 있으면 
            return True # True 반환
        else:
            return False # 그렇지 않으면 False 반환

    def getNumOfNearMines(self, y, x): 
        if self.panels[y][x].get_name() == "Empty": # panels의 y행 x열에 위치한 Panel이 Mine이 아닌 비어있으면
            return self.panels[y][x].numOfNearMines # 주변 지뢰 개수 반환
    
    
