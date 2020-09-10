"""
GUI code for main module. Can run the program with this file. ※ remarking work isn't complete
모듈의 그래픽 구동을 위한 GUI 코드 파일. 본 코드로 프로그램 실행이 가능하다.

$ python final_GUI.py

Author : hekim
Working Log : 2020-08-17 19:36(ver.1)
         2020-08-18 (ver.1.1_코드 수정 및 주석 추가) _ 개선예정작업 : 분산된 메인코드 재정렬 및, 너무 긴 코드 함수화, 프로그램 효율성 재고
         2020-08-18 (ver.1.2_사용자가 1~14번 외에도 222번 등을 입력가능한 부분 발견 후 except IndexError: 추가(추후 재 개선 예정))
         2020-08-20 (ver.2_함수로만 기술했던 프로그램을 클래스화 함(GUI와의 연동 편의를 위해서), 코드 대폭 변경)
         2020-08-21 (ver.2.1_GUI연동 과정에서 show_textview1,2, runprogram1,2 메서드 소스 수정 및 기타부분 대폭 수정...) _ 1차 완성
         2020-08-24 (ver.3_레시피 직접 검색하도록 수정 및 서브 윈도우 클래스를 생성 및(이렇게 안하면 창이 자꾸 닫힘) 레시피 편집기능 추가)
                    참조 _ https://stackoverflow.com/questions/53225320/open-a-new-window-when-the-button-is-clicked-pyqt5
         2020-08-25 (ver.4_사용자가 레시피를 직접 입력하지 않고, 콤보박스에 체크 가능한 레시피 리스트가 나타나도록 GUI 수정(run_funcs,
                    runpro1), 영문설명 추가)
"""
#!/usr/bin/env python3

import sys
import module_0824 as mod
from PyQt5.QtWidgets import QApplication, QTextBrowser, QComboBox, QMainWindow, QAction, qApp, QMessageBox, QPushButton, QFileDialog, QTextEdit
from PyQt5.QtGui import QIcon

ingt1 = None
ingt2 = None
menuname = None
filename = None

# second class for another window
class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("레시피 입력/수정/삭제")

        btn1 = QPushButton(self)
        btn2 = QPushButton(self)
        btn3 = QPushButton(self)
        btn4 = QPushButton(self)
        btn1.setText("새로  입력")
        btn1.move(10, 20) # move(x,y)
        btn1.clicked.connect(self.NewEvent)
        btn2.setText("레시피 수정")
        btn2.move(110, 20)
        btn2.clicked.connect(self.OpenRead)
        btn3.setText("레시피 삭제")
        btn3.move(210, 20)
        btn3.clicked.connect(self.DelEvent)
        btn4.setText("창 닫기")
        btn4.move(310, 20)
        btn4.clicked.connect(self.close)

        self.editor = QTextEdit(self)   # if want call this in other functions of same class, should use 'self.xxx'
        self.editor.move(10, 60)        # editor앞에 self를 안붙이면 클래스 내 다른 함수에서 호출 불가!
        self.editor.resize(400, 320)

        btn5 = QPushButton(self)
        btn5.setText("저        장")
        btn5.move(10, 385)
        btn5.resize(400, 30)
        btn5.clicked.connect(self.SaveEvent)

    def DelEvent(self):
        QFileDialog.getOpenFileName(self, '다음 파일목록에서 Del키로 삭제하고 Ctrl+z키로 되돌릴 수 있습니다. 작업 후에는 취소를 눌러주세요.', './menu/')

    def NewEvent(self):
        global filename
        self.editor.clear()
        self.editor.setText("첫 줄에는 재료들을 써 주세요 ex) 어묵,감자,계란\n두 번째 줄 부터는 레시피를 작성해주시면 됩니다. ex)감자를 씻는다\nex)어묵은 잘게 썬다\n     .\n     .\n\n※이 안내 글은 지우고 작성해 주시면 됩니다.")
        filename = None
        temp = QMessageBox(self)
        temp.question(self, '안내', "초기화 완료\n새 레시피 작성 후 저장이 가능합니다.", QMessageBox.Close)

    def SaveEvent(self):
        global filename
        txt = self.editor.toPlainText() #텍스트 얻어오기(https://freeprog.tistory.com/325)
        if filename == None:
            filename = QFileDialog.getSaveFileName(self, '저장하기', './menu/', '*.txt')
            if filename[0]:
                with open(filename[0], 'w') as f:
                    print(txt)
                    f.write(txt)
                    temp = QMessageBox(self)
                    temp.question(self, '안내', "성공적으로 저장되었습니다.", QMessageBox.Close)
            self.editor.clear()
            filename = None
        else:
            with open(filename[0], 'w') as f:
                f.write(txt)
                temp = QMessageBox(self)
                temp.question(self, '안내', "성공적으로 저장되었습니다.", QMessageBox.Close)
                self.editor.clear()
            filename = None

    def OpenRead(self):
        global filename
        #print(filename)
        filename = QFileDialog.getOpenFileName(self, '파일열기', './menu/') #디렉터리 미 존재시 오류처리 작성함(아래).
        if filename == ('', ''): #if filename[0]:만 써버리면 창을 열어서 파일을 선택안하고 그냥 닫을 경우 저장시 경로명('', '')로 인한 오류 발생
            filename = None
        #example of filename =('', ''), ('D:/kimhe/PycharmProjects/ACProject1/menu/냸옔찌게.txt', 'All Files (*)')
        else:#filename[0]:
            with open(filename[0], 'r') as f: #ex of fname[0] = D:/kimhe/PycharmProjects/ACProject1/menu/꺐국.txt
                data = f.read()
                self.editor.clear()
                self.editor.append(data) #At here using 'append' instead setText(data)

# first class for main window
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = '냉장고를 비우자!'

        # 최상단 메뉴바 관련 코드
        # 0824레시피 작성/편집/삭제 메뉴를 상단 메뉴바에 연계시킬까 하다가.. 그냥 탭으로..
        exitAction = QAction(QIcon(None), 'Exit', self)  # 하위메뉴1
        exitAction.setStatusTip('프로그램 종료')
        exitAction.triggered.connect(qApp.quit)  # 이벤트 연결

        explAction = QAction(QIcon(None), 'About..', self)  # 하위메뉴2
        explAction.setStatusTip('프로그램 설명')
        explAction.triggered.connect(Window.ShowDialog)  # 이벤트 연결

        recipedit = QAction(QIcon(None), 'edit', self)
        recipedit.setStatusTip('레시피 입력/수정/삭제를 합니다.')
        recipedit.triggered.connect(self.window2)                           #  <===========

        self.statusBar()  # 대소문자 주의 #하단에 상태바 생성(StatusTip 출력될 곳)

        menubar = self.menuBar()  # 바 생성
        menubar.setNativeMenuBar(False)  # Mac에서도 Win처럼 보이게 함.
        filemenu = menubar.addMenu('메뉴')  # 상위 메뉴 생성
        filemenu.addAction(explAction)  # 하위메뉴 연결
        filemenu.addAction(recipedit)
        filemenu.addAction(exitAction)

        # 상단 콤보 박스 2개
        cb = QComboBox(self)
        ingr_list = ["파", "우유", "양파", "오이", "두부", "계란", "당근", "시금치", "콩나물", "감자", "무", "가지", "양배추", "어묵", "대파"]
        cb.addItem("필수 선택")
        for i in ingr_list:
            cb.addItem(i)
        cb.move(50, 50)
        cb2 = QComboBox(self)
        cb2.addItem("선택 안함")
        for i in ingr_list:
            cb2.addItem(i)
        cb2.move(180, 50)

        cb.activated[str].connect(self.chg_glovar1)  # 콤보박스 값을 선택할 때마다 전역변수 ingt1,2의 값이 변한다.
        cb2.activated[str].connect(self.chg_glovar2)  # 이와 동시에 텍스트 브라우저의 출력 값도 다시 불러온다.
        # cb.activated.connect(self.run_funcs) -> 별도의 코드로 작성하자 매개변수가 바뀌는 시점과 함수가 호출되는 시점이 이상하게 꼬였었음..(이런것 주의)

        # 하단 텍스트 브라우저1
        self.tbr1 = QTextBrowser(self)
        self.tbr1.move(50, 90)
        self.tbr1.resize(400, 180)

        # 라인에디터를 콤보 박스로!(08/25수정)
        # 사용자 입력을 구현하기 위해 다음을 작성함.
        self.cb3 = QComboBox(self)
        self.cb3.setStatusTip("레시피 목록은 위 결과리스트 값을 반영하여 자동생성 됩니다.")
        self.cb3.addItem("레시피 선택")
        self.cb3.move(50, 280)
        self.cb3.activated[str].connect(self.return_menu)

        # 하단 텍스트 브라우저2
        self.tbr2 = QTextBrowser(self)
        self.tbr2.move(50, 320)
        self.tbr2.resize(400, 150)

        self.main_window()

    def ShowDialog(self):
        msgBox = QMessageBox()
        msgBox.setText(
            "이 프로그램은\n..\n...\n....\n.....\n......")
        msgBox.setWindowTitle("소개")
        msgBox.setStandardButtons(QMessageBox.Close)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Close:
            return 0

    def return_menu(self, text):
        global menuname
        if text == "레시피 선택":
            menuname = None
        else:
            menuname = text
        self.show_tbr2()

    def chg_glovar1(self, text):
        global ingt1
        global ingt2#
        if text == "선택 안함":
            ingt1 = None
        else:
            ingt1 = text
        print("ingt1=",ingt1, "ingt2=",ingt2)
        self.run_funcs() #최신 전역변수 값으로 재실행하여 텍스트 브라우저 값을 변경함.

    def run_funcs(self):
        self.cb3.clear() #()붙이면 작동하고 안붙이면 작동안함! / self.cb3.removeItem(1)은 인덱스 갯수 세야해서 clr
        self.cb3.addItem("레시피 선택")
        self.show_tbr1()
        #self.cb3.addItem("뭔가 추가함")

    def chg_glovar2(self, text):
        global ingt1#
        global ingt2
        if text == "선택 안함":
            ingt2 = None
        else:
            ingt2 = text
        print("ingt1=", ingt1, "ingt2=", ingt2)
        self.run_funcs()

    def runpro1(self):
        global ingt1
        global ingt2
        temp = mod.runprogram1(ingt1, ingt2) #인덱스0:메뉴명, 인덱스1:재료들인 리스트
        temp2 = []
        for i in temp[0]:   #deep copy, temp2 = temp[] is light copy, so can't sorting data.
            temp2.append(i)
        temp2.sort() #지금은 '가나다'순인데, 글자 길이 순으로 하고 싶으면 temp2.sort(key=len) 쓰면 됨.
        for i in temp2: #리턴값 넘기기 전에 .. 메뉴 리스트만 뽑아서 콤보박스에 이식하는 코드 추가함(08/25)
            self.cb3.addItem(i)
        return temp

    def show_tbr1(self):
        self.tbr1.clear()
        list_name_and_print = self.runpro1()
        for i in list_name_and_print[1]:    #재료들인 인덱스1 출력
            self.tbr1.append(i)
    def show_tbr2(self):
        self.tbr2.clear()
        global menuname
        try:
            with open(".\\menu\\{}.txt".format(menuname), "r") as f:
                temp = f.readlines()
                temp_ingt = temp[0] #
                del temp[0]
                self.tbr2.append("[{}의 레시피]\n해당재료:{}\n{}".format(menuname, temp_ingt, "".join(temp)))
        except FileNotFoundError:
            self.tbr2.append("해당되는 레시피가 없습니다.")

    def main_window(self):
        self.setWindowTitle(self.title)
        self.resize(500,500)
        self.show()

    def window2(self):                                             # <===
        self.w = Window2()
        self.w.resize(420, 420)
        self.w.show()
        #self.btn = QLabel()  #btn = QLabel(self)로 쓰면 main_window에 장착,self.btn = QLabel()으로 쓰면 세번째 창 열림,
        #self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())