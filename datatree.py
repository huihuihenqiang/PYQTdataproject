# data_tree.py数据库栏的函数
import os
# 导入所需模块
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableView, QMdiArea, QMdiSubWindow
from PyQt5.QtWidgets import QTreeView  # 引入QTreeView模块
from childwindow import ChildWindow  # 自定义模块ChildWindow
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery  # 引入QSqlDatabase、QSqlTableModel、QSqlQuery模块
from dbmanager import DatabaseManager  # 自定义模块DatabaseManager
class DataTree:
    def __init__(self, parent):
        """
        数据树类
        Args:
            parent: 父对象
        """
        self.treeView_2 = None
        self.parent = parent
        self.tree_model = None

    def setup_datatree(self):
        """
        设置数据树
        """
        self.treeView_2 = self.parent.findChild(QTreeView, "treeView_2")
        self.treeView_2.setModel(None)
        if QSqlDatabase.contains("setup_connection"):
            db_connection = QSqlDatabase.database("setup_connection")
            db_connection.close()
            connection = db_connection.connectionName()
            db_connection = QSqlDatabase()
            db_connection.removeDatabase(connection)
        if os.path.exists('DATA.db'):
            db_connection = QSqlDatabase.addDatabase("QSQLITE", "setup_connection")  # 指定连接名
            db_connection.setDatabaseName('DATA.db')
            if not db_connection.open():
                print("无法打开数据库")
                return
            # 构建模型并设置到treeview中
            self.tree_model = QSqlTableModel(db=db_connection)
            self.tree_model.setTable("sqlite_master")  # 使用sqlite_master表获取所有表名
            self.tree_model.setFilter("type='table'")
            self.tree_model.select()

            self.treeView_2.setModel(self.tree_model)
            self.treeView_2.setColumnHidden(0, True)  # 隐藏第一列（通常是rowid）
            self.treeView_2.setColumnHidden(1, True)
            self.treeView_2.setColumnHidden(3, True)
            self.treeView_2.setColumnHidden(4, True)
            self.treeView_2.clicked.connect(self.show_table_data)
        else:
            print("DATA.db 文件不存在")

    def show_table_data(self, index):
        table_name = self.tree_model.data(index, Qt.DisplayRole)
        # 创建数据库连接管理器实例
        db_manager = DatabaseManager('DATA.db')
        # 显式打开新的数据库连接
        if not db_manager.open_connection():
            return
        # 创建并显示子窗口
        child_window = ChildWindow(table_name)

        # 在子窗口中创建并设置QTableView
        table_widget = QTableView()
        child_window.setCentralWidget(table_widget)

        # 为所点击的表创建一个新的QSqlTableModel，并与子窗口的QTableView关联
        table_model = QSqlTableModel(db=db_manager.connection)  # 使用新连接
        table_model.setTable(table_name)

        # 先设置模型再进行选择操作
        table_widget.setModel(table_model)

        # 加载数据
        if not table_model.select():
            print("无法从数据库加载数据")
        else:
            table_widget.resizeColumnsToContents()  # 自动调整列宽以适应内容

        # 显示子窗口
        self.mdiArea = self.parent.findChild(QMdiArea, 'mdiArea')
        sub_window = QMdiSubWindow()
        sub_window.setWidget(child_window)
        self.mdiArea.addSubWindow(sub_window)
        sub_window.show()
        # 关闭当前子窗口使用的数据库连接
        db_manager.close_connection()
