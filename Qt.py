from PyQt5.QtSensors import QMagnetometer
from PyQt5.QtWidgets import *
import sys, os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from ffmDivideVideo import ffmDivideVideo


def searchGUI():
    root = Tk()
    root.withdraw()
    filename = askopenfilename()
    dirLine.setText(filename)

def getFromQt():
    if dirLine.text() == '':
        QMessageBox.information(dirLine,"警告","你还没有输入文件路径")
        return
    else:
        directory = str(dirLine.text())
    if divLine.text()== "":
        divnum=-1
    else:
        divnum=float(divLine.text())
    if fpsSettingLine.text()== "":
        fpsnum=-1
    else:
        fpsnum=float(fpsSettingLine.text())
    if piecesLine.text()!= "5" and piecesLine.text()!= "10" and piecesLine.text()!= "15":
        piecesnum=int(5)
    else:
        piecesnum=int(piecesLine.text())
    ffmDivideVideo(directory,divnum,fpsnum,piecesnum)
    fileName, _ = os.path.splitext(directory)
    fileName = ".\\output\\"+os.path.basename(fileName)
    fileNamelist=[]
    oversizedFiles=[]
    maxNum=0
    for i in range(piecesnum):
        fileNamelist.append(f"{fileName}_{i}_output.gif")
    for index,filename in enumerate(fileNamelist):
        maxNum=max(maxNum,checkFilesize(filename))
        if checkFilesize(filename) > 5.0:
            oversizedFiles.append(index)
    if maxNum<5.0:
        QMessageBox.information(divLine, "完成", f"完成")
    else:
        QMessageBox.information(divLine, "有超出5MB的文件", f"最大的大小是{maxNum}MB，超出的分块分别是{oversizedFiles}")

def openSaveDir():
    if not os.path.exists('.\\output'):
        os.mkdir('.\\output')
    os.startfile(".\\output")


def checkFilesize(filename):
    stats = os.stat(filename)
    return float((stats.st_size/(1024**2)).__format__("0.2f"))

app = QApplication(sys.argv)
GUI = QWidget()
dirLabel = QLabel("输入源文件路径")
dirLine = QLineEdit(GUI)
divLabel = QLabel("输入要除以多少倍（不输入即为不更换）")
divLine = QLineEdit(GUI)
fpsSettingLabel = QLabel("输入转换后的fps（不输入即为不更换）")
fpsSettingLine = QLineEdit(GUI)
piecesLabel=QLabel("分割成5/10/15块（默认5）")
piecesLine = QLineEdit(GUI)
EnterButton = QPushButton("分割", GUI)
SearchButton = QPushButton("浏览",GUI)
SaveButton = QPushButton("打开存储目录",GUI)
GUI.setGeometry(1000, 800, 600, 100)
subLayout = QHBoxLayout()
subLayout2 = QHBoxLayout()
subLayout.addStretch(1)
bodyLayout = QVBoxLayout()
bodyLayout.addWidget(dirLabel)
bodyLayout.addWidget(dirLine)
bodyLayout.addWidget(SearchButton)
subLayout.addWidget(divLabel)
subLayout.addWidget(divLine)
subLayout.addWidget(fpsSettingLabel)
subLayout.addWidget(fpsSettingLine)
bodyLayout.addLayout(subLayout)
subLayout.addWidget(piecesLabel)
subLayout.addWidget(piecesLine)
bodyLayout.addLayout(subLayout2)
subLayout2.addWidget(EnterButton)
subLayout2.addWidget(SaveButton)
EnterButton.clicked.connect(getFromQt)
SearchButton.clicked.connect(searchGUI)
SaveButton.clicked.connect(openSaveDir)
GUI.setLayout(bodyLayout)
GUI.setWindowTitle("Steam个人资料动图制作")
GUI.show()
sys.exit(app.exec_())