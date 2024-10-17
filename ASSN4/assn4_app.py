import tkinter as tk
from assn4_model import Board

TITLE = "Yojun's Minesweeper"
BTN_WIDTH = 30
BTN_HEIGHT = 30
BORDER_SIZE = 2
OUTTER_PADDING_SIZE = 10
BACKGROUND_COLOR = "#DCDCDC"


class App(tk.Frame):
    def __init__(self, master, mine, height, width):
        super(App, self).__init__(master)
        
        master.title(TITLE)
        self.board = Board() # self.board 인스턴스에 Board 객체 대입, 생성
        self.board.reset(mine, height, width) # board의 reset 함수 실행 해 panel 생성
        self.success_num = 0
        self.height = height
        self.width = width
        self.mine = mine
        
        self.answer_print()
        
        master.geometry(
            f"{width * (BTN_WIDTH) + (OUTTER_PADDING_SIZE + BORDER_SIZE) * 2}x{(height + 1) * (BTN_HEIGHT) + (OUTTER_PADDING_SIZE + BORDER_SIZE) * 5}")
        
        self.base_icon = tk.PhotoImage(file="//mac/iCloud/VS Code/Python/프로그래밍과 문제해결/ASSN/assn4/imgs/smile.png")
        self.success_icon = tk.PhotoImage(file="//mac/iCloud/VS Code/Python/프로그래밍과 문제해결/ASSN/assn4/imgs/sunglasses.png")
        self.fail_icon = tk.PhotoImage(file="//mac/iCloud/VS Code/Python/프로그래밍과 문제해결/ASSN/assn4/imgs/skull.png")
        self.flag_icon = tk.PhotoImage(file="//mac/iCloud/VS Code/Python/프로그래밍과 문제해결/ASSN/assn4/imgs/flag.png")
        self.bomb_icon = tk.PhotoImage(file="//mac/iCloud/VS Code/Python/프로그래밍과 문제해결/ASSN/assn4/imgs/bomb.png")
        
        self["bg"] = BACKGROUND_COLOR
        self["relief"] = tk.SUNKEN
        self["bd"] = BORDER_SIZE
        self["padx"] = OUTTER_PADDING_SIZE
        self["pady"] = OUTTER_PADDING_SIZE   

        head = tk.Frame(self, bg=BACKGROUND_COLOR, relief=tk.SUNKEN, bd=BORDER_SIZE) # GUI의 Header 부분
        head.grid(row=0, column=0, columnspan=width, pady=(0, OUTTER_PADDING_SIZE), sticky='ew')
        
        start_wrapper = tk.Frame(head, width=BTN_WIDTH, height=BTN_HEIGHT)
        start_wrapper.pack_propagate(0)
        start_wrapper.pack(padx=OUTTER_PADDING_SIZE, pady=OUTTER_PADDING_SIZE)
        self.start = tk.Button(start_wrapper, image=self.base_icon, bd=BORDER_SIZE) # 초기화 버튼
        self.start.bind("<Button-1>", lambda e: self.reset_board(mine, height, width))
        self.start.pack(expand=True, fill='both')
        
        body = tk.Frame(self, bg=BACKGROUND_COLOR, relief=tk.SUNKEN, bd=BORDER_SIZE) # GUI의 Body 부분
        body.grid(row=1, column=0, columnspan=width)
        
        self.button_list = [["" for i in range(width)] for j in range(height)] # 버튼을 담은 리스트 생성
        
        for row in range(height): # 처음크기는 버튼 10x10 고정
            for col in range(width):
                btn_wrapper = tk.Frame(body, width = BTN_WIDTH, height = BTN_HEIGHT) # GUI의 버튼을 배치할 구역
                btn_wrapper.pack_propagate(0)
                btn_wrapper.grid(row = row, column = col)
                
                btn = tk.Button(btn_wrapper, bg = BACKGROUND_COLOR, bd = BORDER_SIZE) # panel 버튼 생성
                btn.bind("<Button-1>", lambda e, y = row, x = col: self.left_click(y,x)) # 좌클릭에 left_click 함수 bind
                btn.bind("<Button-3>", lambda e, y = row, x = col: self.right_click(y,x)) # 우클릭에 right_click 함수 bind
                btn.pack(expand = True, fill = 'both')
                self.button_list[row][col] = btn # button_list에 버튼 대입
        
        self.pack()        
        
        
    def reveal_panel(self, row, col): # panel 버튼을 좌클릭할 때 panel을 밝히는 메서드
        button = self.button_list[row][col] # button 변수에 button_list의 row 행, col 열에 해당하는 버튼 대입
        button.config(relief = tk.SUNKEN, state = tk.DISABLED) # button을 눌린 상태로 변경
        if self.board.checkMine(row, col) == True: # 해당 panel이 지뢰이면
            button.config(image = self.bomb_icon) # 버튼 이미지 지뢰로 변경
        else: # 해당 panel이 emptypanel이면
            if self.board.getNumOfNearMines(row, col) != 0: # 만약 주변 지뢰가 0개가 아니라면
                button.config(text = "%d" % self.board.getNumOfNearMines(row, col), font = ('koverwatch')) # 주변 지뢰 개수 표시
            
    def right_click(self, row, col): # panel 버튼을 우클릭할 때 깃발을 꽂거나 제거하는 메서드
        button = self.button_list[row][col] # button 변수에 button_list의 row 행, col 열에 해당하는 버튼 대입
        if self.board.checkReveal(row, col) == False: # 버튼이 reveal 되어 있지 않으면
            if self.board.checkFlag(row, col) == False: # 깃발이 꽂혀 있지 않으면 
                button.config(image = self.flag_icon) # 버튼 깃발 아이콘으로 변화
            else:
                button.config(image = '')
            self.board.toggleFlag(row, col) # flag 토글
        
    def left_click(self, row, col): # panel 버튼을 좌클릭할 때 실행되는 메서드
        if self.board.checkFlag(row, col) == False: # panel에 깃발이 꽂혀 있지 않을 때 
            self.reveal_panel(row, col) # reveal_panel 메서드 실행
            self.board.unveil(row, col) # row 행, col 열에 대해 unveil 메서드 실행
        '''
            if self.board.unveil(row, col) == -1: # 만약 해당 panel이 지뢰라면
                self.end_game() # 게임 종료 메서드 실행
            
            else:
                if self.board.getNumOfNearMines(row, col) == 0: # panel의 주변 지뢰 개수가 0개일 때
                    for row in range(len(self.board.panels)): 
                        for col in range(len(self.board.panels[0])):
                            if self.board.checkReveal(row, col) == True: # 패널의 Reveal 여부가 True일 때
                                self.button_list[row][col].config(image = "") # 깃발 삭제
                                self.reveal_panel(row, col) # reveal_panel 함수 실행
                                               
        for row in range(len(self.board.panels)): # 지뢰찾기 성공 유무 판단
            for col in range(len(self.board.panels[0])):
                if self.board.checkMine(row, col) == False: # 모든 패널에 대해 각 패널이 지뢰가 아닐 때
                    if self.board.checkReveal(row, col) == True: # reveal 유무가 True이면
                        self.success_num+=1 # success_num에 1추가
                               
        if self.success_num == self.height*self.width-self.mine: # success_num이 전체 패널 개수-지뢰개수 이면
            self.start.config(image = self.success_icon) # 리셋 버튼 이미지를 성공 이미지로 변경
        else:
            self.success_num = 0 # 그렇지 않으면 success_num 0으로 초기화
        '''
    def end_game(self): # 게임을 실패했을 때 실행되는 메서드
        self.start.config(image = self.fail_icon) # 리셋 버튼 이미지 실패 이미지로 변경
        for row in range(len(self.board.panels)):
            for col in range(len(self.board.panels[0])):
                if self.board.checkMine(row, col) == True:
                    self.button_list[row][col].config(image = self.bomb_icon, state = tk.DISABLED, relief = tk.SUNKEN)
                else:
                    self.button_list[row][col].config(image = "", text = "%d" % self.board.getNumOfNearMines(row, col), font = ('koverwatch'), state = tk.DISABLED, relief = tk.SUNKEN)
                
    def reset_board(self, mine, height, width): # 리셋 버튼 누를 때 실행되어 리셋하는 메서드
        self.board = Board() # 객체 대입, 생성자 실행
        self.success_num = 0 # 아래에서 초기화
        self.board.reset(mine, height, width)
        self.answer_print()
        for row in range(len(self.board.panels)):
            for col in range(len(self.board.panels[0])):
                button = self.button_list[row][col]
                button.config(image = "", state = tk.NORMAL, relief = tk.RAISED, text = "")
                self.start.config(image = self.base_icon)
    
    def answer_print(self): # 정답표 출력
        print("\n\n")
        for i in self.board.panels:
            for j in i:
                if j.get_name() == "Mine":
                    print("M", end = "  ")
                else:
                    print("E", end = "  ")
            print("")
                
def menu_select(menu): # menu를 인자(난이도)로 받아 app에 tkinter 객체 생성
    global app
    
    app.destroy()
    if menu == "easy":
        app = App(root, 10, 10, 10)
    elif menu == "normal":
        app = App(root, 30, 15, 15)
    else:
        app = App(root, 50, 20, 20)


if __name__ == '__main__':
    title = "YOJUN MINESWEEPER"

    root = tk.Tk()
    menu_bar = tk.Menu(root)
    root.config(menu = menu_bar)
    
    level_menu = tk.Menu(menu_bar)
    menu_bar.add_cascade(label = "난이도", menu = level_menu)
    
    level_menu.add_command(label = "Easy", command = lambda: menu_select("easy"))
    level_menu.add_command(label = "Normal", command = lambda: menu_select("normal"))
    level_menu.add_command(label = "Hard", command = lambda: menu_select("hard"))
    
    app = App(root, 10, 10, 10)
    app.mainloop()
