# menu_actions.py菜单和工具栏动作类函数（注意不是工具按钮）
from PyQt5.QtWidgets import QMdiSubWindow, QMdiArea, QDockWidget, QMessageBox, QDialog, QVBoxLayout
from PyQt5.QtWidgets import QAction, QFileDialog
import os
from PyQt5.QtCore import QDir, QUrl
from datatree import DataTree
import webbrowser
# 定义菜单栏动作管理类
class MenuActions:
    def __init__(self, parent):
        # 初始化父窗口对象引用和QMdiArea组件引用
        self.datatree = None
        self.mdiArea = None
        self.parent = parent

    # 设置菜单栏的动作连接方法
    def setup_menu(self):


        # 查找并连接“clear”按钮触发信号至相应槽函数
        actionclear = self.parent.findChild(QAction, 'actionclear')
        actionclear.triggered.connect(self.on_actionclear_clicked)

        # 查找并连接“tile”按钮触发信号至相应槽函数
        actiontile = self.parent.findChild(QAction, 'actiontile')
        actiontile.triggered.connect(self.on_actiontile_clicked)

        # 查找并连接“cascade”按钮触发信号至相应槽函数
        actioncascade = self.parent.findChild(QAction, 'actioncascade')
        actioncascade.triggered.connect(self.on_actioncascade_clicked)

        # 查找并连接新建工作空间按钮触发信号至相应槽函数
        actionNew = self.parent.findChild(QAction, 'actionNew')
        actionNew.triggered.connect(self.on_actionNew_clicked)

        # 查找并连接打开工作空间按钮触发信号至相应槽函数
        actionOpen = self.parent.findChild(QAction, 'actionOpen')
        actionOpen.triggered.connect(self.on_actionOpen_clicked)

        actionRefresh = self.parent.findChild(QAction, 'actionRefresh')
        actionRefresh.triggered.connect(self.on_actionRefresh_clicked)

        actionExit = self.parent.findChild(QAction, 'actionExit')
        actionExit.triggered.connect(self.on_actionExit_clicked)

        actionhelp = self.parent.findChild(QAction, 'actionhelp')
        actionhelp.triggered.connect(self.on_actionhelp_clicked)

        actionabout = self.parent.findChild(QAction, 'actionabout')
        actionabout.triggered.connect(self.on_actionabout_clicked)

        actionuser_agreement = self.parent.findChild(QAction, 'actionuser_agreement')
        actionuser_agreement.triggered.connect(self.on_actionuser_agreement_clicked)


    def on_actionhelp_clicked(self):
        # 指定要打开的网址
        url = 'https://huihuihenqiang.github.io/article/Software/help.html'
        # 使用webbrowser模块打开网址
        webbrowser.open(url)

    def on_actionabout_clicked(self):
        # 指定要打开的网址
        url = 'https://huihuihenqiang.github.io/article/Software/about.html'
        # 使用webbrowser模块打开网址
        webbrowser.open(url)
    def on_actionuser_agreement_clicked(self):
        # 指定要打开的网址
        url = 'https://huihuihenqiang.github.io/article/Software/user.html'
        # 使用webbrowser模块打开网址
        webbrowser.open(url)

    def on_actionExit_clicked(self):
        reply = QMessageBox.question(self.parent, '确认', "强制退出程序可能会导致数据丢失，是否继续？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.parent.close()
    def on_actionRefresh_clicked(self):
        # 实现自动检测数据库变化功能
        # 创建DataTree类实例并初始化
        self.datatree = DataTree(self.parent)
        self.datatree.setup_datatree()

    # 处理"clear"按钮点击事件
    def on_actionclear_clicked(self):
        # 创建并实例化子窗口类
        #child_window = ChildWindow('ff')

        # 获取QMdiArea组件，并将新创建的子窗口添加到QMdiArea作为子窗口部件
        self.mdiArea = self.parent.findChild(QMdiArea, 'mdiArea')
        #sub_window = QMdiSubWindow()
        #sub_window.setWidget(child_window)
        subwin=self.mdiArea.subWindowList()
        for i in range(len(subwin)):
            self.mdiArea.removeSubWindow(subwin[i])
        #print(subwin)
        #self.mdiArea.closeActiveSubWindow()
        #self.mdiArea.addSubWindow(sub_window)
        #sub_window.show()  # 显示子窗口

    def on_actiontile_clicked(self):

        # 获取QMdiArea组件，并将新创建的子窗口添加到QMdiArea作为子窗口部件
        self.mdiArea = self.parent.findChild(QMdiArea, 'mdiArea')
        self.mdiArea.tileSubWindows()

    def on_actioncascade_clicked(self):
        # 获取QMdiArea组件，并将新创建的子窗口添加到QMdiArea作为子窗口部件
        self.mdiArea = self.parent.findChild(QMdiArea, 'mdiArea')
        self.mdiArea.cascadeSubWindows()

    # 处理"新建工作空间"按钮点击事件
    def on_actionNew_clicked(self):
        default_workspace_name = "MyWorkspace"
        # 弹出文件对话框，让用户选择一个目录以创建新的工作空间
        workspace_path = QFileDialog.getExistingDirectory(
            self.parent, "选择工作区路径并创建", QDir.homePath(),
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )

        if workspace_path:
            # 创建完整的工作空间路径并确保其存在
            full_workspace_path = os.path.join(workspace_path, default_workspace_name)
            os.makedirs(full_workspace_path, exist_ok=True)
            os.chdir(full_workspace_path)  # 切换当前工作目录到新创建的工作空间

            # 更新工作空间状态（此处未在注释中显示具体实现）
            self.update_workspace_status()

            # 设置主函数中的workspace_selected标志为True
            self.parent.workspace_selected = True

    # 处理"打开工作空间"按钮点击事件
    def on_actionOpen_clicked(self):
        workspace_path = QFileDialog.getExistingDirectory(self.parent, "选择工作区", QDir.homePath())

        if workspace_path:
            os.chdir(workspace_path)  # 切换当前工作目录到选定的工作空间

            # 更新工作空间状态（此处未在注释中显示具体实现）
            self.update_workspace_status()

            # 设置主函数中的workspace_selected标志为True
            self.parent.workspace_selected = True

            # 实现自动检测数据库变化功能
            # 创建DataTree类实例并初始化
            self.datatree = DataTree(self.parent)
            self.datatree.setup_datatree()

    # 更新当前工作区状态的方法
    def update_workspace_status(self):
        # 更新状态栏信息以显示当前工作区路径
        self.parent.statusBar().showMessage(f"当前工作区: {os.getcwd()}")


