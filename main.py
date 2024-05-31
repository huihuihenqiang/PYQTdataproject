# main.py主函数文件
import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
import img_rc

# 导入sys模块，用于获取命令行参数
# 导入PyQt5的QApplication模块，用于创建应用程序对象
# 自定义一个MainWindow类，用于创建主窗口对象
# 导入img_rc模块，用于加载图像资源
if __name__ == "__main__":
    # 创建一个应用程序对象，并将命令行参数传递给它
    app = QApplication(sys.argv)
    # 创建一个主窗口对象
    mainWindow = MainWindow()
    # 显示主窗口
    mainWindow.show()
    # 运行应用程序，直到主事件循环结束
    sys.exit(app.exec_())
