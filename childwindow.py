# childwindow.py子窗口函数
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget
class ChildWindow(QMainWindow):  # 定义一个继承自QMainWindow的子窗口类ChildWindow
    def __init__(self, child_win_name):  # 初始化方法
        super(ChildWindow, self).__init__()  # 调用父类QMainWindow的初始化方法

        self.setWindowTitle(child_win_name)  # 设置当前窗口标题为"子窗口"
        central_widget = QWidget()  # 创建一个QWidget对象作为窗口中央部件
        self.setCentralWidget(central_widget)  # 将创建的QWidget对象设置为窗口的中央部件
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/png/ico/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)