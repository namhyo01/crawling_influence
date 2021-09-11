from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from crawl import Crawling
import time

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
 

class CWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.s = Crawling()
        self.initUI()

   
    def initUI(self):
        self.setWindowTitle('crawling')
        
        # 서버 설정 부분
        ipbox = QHBoxLayout()

        gb = QGroupBox('카테고리')
        ipbox.addWidget(gb)

        box = QHBoxLayout()
        label = QLabel('메인 카테고리')
        self.main_category = QLineEdit() # 메인 카테고리 입력
        box.addWidget(label)
        box.addWidget(self.main_category)

        label = QLabel('서브 카테고리')
        self.sub_category = QLineEdit()
        box.addWidget(label)
        box.addWidget(self.sub_category)

        gb.setLayout(box)
        
        ivbox = QHBoxLayout()
        box = QHBoxLayout()
        gb = QGroupBox('크롤링 수 결정')
        ivbox.addWidget(gb)
        label = QLabel('이 인플루언서  위치부터 ')
        self.start = QLineEdit('1')
        self.start.setInputMask("0000;")
        box.addWidget(label)
        box.addWidget(self.start)
        

        label = QLabel('이 인플루언서 위치까지')
        self.finish = QLineEdit('20')
        self.finish.setInputMask("0000;")
        box.addWidget(label)
        box.addWidget(self.finish)
        
        gb.setLayout(box)


        ikbox = QHBoxLayout()
        box = QHBoxLayout()
        gb = QGroupBox('결과 저장 폴더 선택')
        ikbox.addWidget(gb)
        label = QLabel('결과 저장 폴더 선택해주세요')
        self.btn = QPushButton('버튼을 눌러주세요')
        self.btn.setCheckable(True)
        self.btn.toggled.connect(self.toggleButton)
        self.dir_path = QLineEdit()
        box.addWidget(label)
        box.addWidget(self.btn)
        box.addWidget(self.dir_path)
        gb.setLayout(box)

        iqbox = QHBoxLayout()
        box = QHBoxLayout()
        gb = QGroupBox()
        iqbox.addWidget(gb)
        self.btn_run = QPushButton('실행')
        self.btn_run.setCheckable(True)
        self.btn_run.toggled.connect(self.run)
        self.btn_run.resize(250,150)
        box.addWidget(self.btn_run,alignment=Qt.AlignRight)
        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)
        vbox.addLayout(ivbox)
        vbox.addLayout(ikbox)
        vbox.addLayout(iqbox)
        
        self.setLayout(vbox)

        self.show()

    def run(self):
        main_category = self.main_category.text()
        sub_category = self.sub_category.text()
        start = int(self.start.text())
        finish = int(self.finish.text())
        dir_path = self.dir_path.text()
        print(main_category)
        print(sub_category)
        a = self.s.crawling(main_category,sub_category,start,finish)
        if a==-1:
            QMessageBox.about(self,'크롤링','잘못된 카테고리 입력')    
            return
        elif a==-2:
            QMessageBox.about(self,'크롤링','잘못된 서브 카테고리 입력')
            return
        
        self.s.list_crawling(dir_path)
        self.btn_run.setText("엑셀 마무리중")
        
        self.s.excel_style(dir_path)
        self.btn_run.setText("실행")
        QMessageBox.about(self,'크롤링','완료 되었습니다')

    def toggleButton(self, state):
        dirName = QFileDialog.getExistingDirectory(self, self.tr("Open Data files"), "./", QFileDialog.ShowDirsOnly)
        self.dir_path.setText(dirName)
        print(dirName)

    def closeEvent(self, e):
        self.s.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec())
    