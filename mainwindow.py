# mainwindow.py主窗口文件
from PyQt5.QtWidgets import QMainWindow, QLabel  # 导入PyQt5库中用于构建GUI的模块
from PyQt5.uic import loadUi  # 导入uic模块，用于加载.ui设计文件
from menuactions import MenuActions  # 导入自定义的菜单动作类
from toolactions import ToolActions  # 导入自定义的工具动作类

class MainWindow(QMainWindow):  # 定义主窗口类，继承自PyQt5.QtWidgets.QMainWindow
    def __init__(self):  # 初始化方法
        super(MainWindow, self).__init__()  # 调用父类的初始化方法

        # 加载UI界面文件（.ui格式）
        loadUi('process_data_project.ui', self)  # 将.ui文件转换为Python代码并应用到当前窗口实例上
        # 在主应用初始化时创建单例
        #self.app_state = AppState()
        # 使用全局状态
        #self.app_state.set_value('key', 'value from MainWindow')
        #print("Value from MainWindow:", self.app_state.get_value('key'))
        # 使用全局状态
        #global_state.set_value('key', 'value from MainWindow')
        #print("Value from MainWindow:", global_state.get_value('key'))
        self.setWindowTitle("软件v1.0.1")

        # 设置状态栏信息
        self.statusBar().showMessage("未设置工作区")  # 在状态栏显示消息提示用户尚未选择工作区


        # 创建一个布尔变量记录是否已选择工作区
        self.workspace_selected = False  # 初始状态下工作区未被选择
        # 创建MenuActions类的实例对象，将当前窗口作为参数传入
        self.menuactions = MenuActions(self)
        # 设置菜单和工具栏的动作，并连接相应的信号与槽函数
        self.menuactions.setup_menu()
        # 创建ToolActions类的实例对象，同样将当前窗口作为参数传入
        self.toolactions = ToolActions(self)
        # 设置工具的动作，并连接对应的信号与槽函数
        self.toolactions.setup_tool()


