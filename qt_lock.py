import sys

from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 设置背景
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('./1.jpg')))  # 设置背景图片
        self.setPalette(palette1)
        self.setAutoFillBackground(True)  # 不设置也可以


def show_mywindow():
    app = QApplication(sys.argv)
    mywindows = MyWindow()
    QLabel(mywindows).setText(
        "<p style='color: gray; margin-left: 60px;margin-top:100px;font-size:35px'><b>主人离开了谁都别想动我哦(๑•ᴗ•๑)</b></p>")
    mywindows.showFullScreen()
    # app.exec_()
    sys.exit(app.exec_())

if __name__ == '__main__':
    show_mywindow()