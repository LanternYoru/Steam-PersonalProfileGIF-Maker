import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, \
    QMessageBox, QFileDialog

from ffmDivideVideo import ffmDivideVideo


def openSaveDir():
    if not os.path.exists('.\\output'):
        os.mkdir('.\\output')
    os.startfile(".\\output")

def checkFilesize(filename):
    stats = os.stat(filename)
    return float((stats.st_size/(1024**2)).__format__("0.2f"))

class SteamProfileGifMaker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建组件
        self.dirLabel = QLabel("输入源文件路径")
        self.dirLine = QLineEdit(self)
        self.divLabel = QLabel("输入要除以多少倍（不输入即为不更换）")
        self.divLine = QLineEdit(self)
        self.fpsSettingLabel = QLabel("输入转换后的fps（不输入即为不更换）")
        self.fpsSettingLine = QLineEdit(self)
        self.piecesLabel = QLabel("分割成5/10/15块（默认5）")
        self.piecesLine = QLineEdit(self)
        self.EnterButton = QPushButton("分割", self)
        self.SearchButton = QPushButton("浏览", self)
        self.SaveButton = QPushButton("打开存储目录", self)

        # 设置布局
        self.initLayout()

        # 设置窗口
        self.setGeometry(1000, 800, 600, 100)
        self.setWindowTitle("Steam个人资料动图制作")

        # 绑定信号和槽
        self.EnterButton.clicked.connect(self.getFromQt)
        self.SearchButton.clicked.connect(self.searchGUI)
        self.SaveButton.clicked.connect(openSaveDir)

    def initLayout(self):
        subLayout = QHBoxLayout()
        subLayout2 = QHBoxLayout()

        subLayout.addStretch(1)
        bodyLayout = QVBoxLayout()

        # 布局各组件
        bodyLayout.addWidget(self.dirLabel)
        bodyLayout.addWidget(self.dirLine)
        bodyLayout.addWidget(self.SearchButton)

        subLayout.addWidget(self.divLabel)
        subLayout.addWidget(self.divLine)
        subLayout.addWidget(self.fpsSettingLabel)
        subLayout.addWidget(self.fpsSettingLine)
        bodyLayout.addLayout(subLayout)

        subLayout.addWidget(self.piecesLabel)
        subLayout.addWidget(self.piecesLine)

        bodyLayout.addLayout(subLayout2)
        subLayout2.addWidget(self.EnterButton)
        subLayout2.addWidget(self.SaveButton)

        self.setLayout(bodyLayout)
        # 绑定按钮事件的槽函数
    def getFromQt(self):
        if self.dirLine.text() == '':
            QMessageBox.information(self.dirLine, "警告", "你还没有输入文件路径")
            return
        else:
            directory = str(self.dirLine.text())
        if self.divLine.text() == "":
            divnum = -1
        else:
            divnum = float(self.divLine.text())
        if self.fpsSettingLine.text() == "":
            fpsnum = -1
        else:
            fpsnum = float(self.fpsSettingLine.text())
        if self.piecesLine.text() != "5" and self.piecesLine.text() != "10" and self.piecesLine.text() != "15":
            piecesnum = int(5)
        else:
            piecesnum = int(self.piecesLine.text())
        ffmDivideVideo(directory, divnum, fpsnum, piecesnum)
        fileName, _ = os.path.splitext(directory)
        fileName = ".\\output\\" + os.path.basename(fileName)
        fileNamelist = []
        oversizedFiles = []
        maxNum = 0
        for i in range(piecesnum):
            fileNamelist.append(f"{fileName}_{i}_output.gif")
        for index, filename in enumerate(fileNamelist):
            maxNum = max(maxNum, checkFilesize(filename))
            if checkFilesize(filename) > 5.0:
                oversizedFiles.append(index)
        if maxNum < 5.0:
            QMessageBox.information(self, "完成", f"完成")
        else:
            QMessageBox.information(self, "有超出5MB的文件",
                                    f"最大的大小是{maxNum}MB，超出的分块分别是{oversizedFiles}")
        pass

    def searchGUI(self):
        filename,_ = QFileDialog.getOpenFileName(self,'浏览')
        self.dirLine.setText(filename)
        pass


def main():
    app = QApplication(sys.argv)
    window = SteamProfileGifMaker()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()