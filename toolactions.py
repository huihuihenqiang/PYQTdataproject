# tool_actions.py工具按钮类文件
import os
from childwindow import ChildWindow  # 自定义模块ChildWindow
from PyQt5.QtWidgets import QToolButton, QMessageBox, QTreeView, QMdiArea, QMdiSubWindow, QAction
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QDir
import sqlite3
import pandas as pd
from extract_data import ExtractData
from taskthread import TaskThread
from processdata import MergeData
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# 定义工具按钮动作管理类
class ToolActions:
    def __init__(self, parent):
        self.figure = None
        self.datatree = None
        self.parent = parent

    def setup_tool(self):
        # 查找并连接名为'toolButton'的工具栏按钮的点击事件至槽函数
        toolButton = self.parent.findChild(QToolButton, 'toolButton')
        toolButton.clicked.connect(self.on_toolButton_clicked)

        # 查找并连接名为'toolButton_2'的工具栏按钮的点击事件至槽函数
        toolButton_2 = self.parent.findChild(QToolButton, 'toolButton_2')
        toolButton_2.clicked.connect(self.on_toolButton_2_clicked)

        # 查找并连接名为'toolButton_2'的工具栏按钮的点击事件至槽函数
        toolButton_7 = self.parent.findChild(QToolButton, 'toolButton_7')
        toolButton_7.clicked.connect(self.on_toolButton_7_clicked)

        # 这个本来不应该出现在这里。但是太困了。不想思考了，就这么做吧。
        actionSave = self.parent.findChild(QAction, 'actionSave')
        actionSave.triggered.connect(self.save_figure)

    def on_toolButton_7_clicked(self):
        file_path = 'output_data.xlsx'
        column_name = 'loss_dis'
        if not self.parent.workspace_selected:
            QMessageBox.warning(self.parent, "警告", "请先新建或选择工作区！")
            return
        elif not os.path.isfile(file_path):
            QMessageBox.warning(self.parent, "警告", "请先合并数据!")
            return

        else:
            try:
                self.figure = Figure(figsize=(4, 10))  # 创建一个matplotlib的Figure对象
                self.canvas = FigureCanvas(self.figure)  # 将Figure包装进FigureCanvas，使其能在Qt窗口中显示
                # 设置图形内容
                self.axes = self.figure.add_subplot(111)
                # 读取Excel文件中的指定列
                df = pd.read_excel(file_path)
                column_data = df[column_name]
                # 如果需要，可以对数据进行清洗或预处理，比如去除缺失值等
                column_data = column_data.dropna()
                # 将该列转换为NumPy数组，虽然对于matplotlib来说不是必需的，但有时更方便
                y_values = column_data.to_numpy()
                # 如果没有x轴的数据，这里假设使用整数索引作为x轴
                x_values = range(len(y_values))
                # n = np.random.rand(100)
                # data = np.sin(10 * n)
                #self.axes.plot(x_values, y_values, label='Line Plot')
                #self.axes.scatter(x_values, y_values, color='r', s=3, label='Loss Point')
                #纵向显示
                self.axes.plot(y_values, x_values, label='Line Plot')
                self.axes.scatter(y_values, x_values, color='r', s=3, label='Loss Point')
                # 反转 y 轴方向
                self.axes.invert_yaxis()
                # 设置图形属性
                self.axes.set_xlabel('Loss(m^3)')
                self.axes.set_ylabel('Depth(m)')
                self.axes.set_title('Depth-Loss')
                self.axes.legend()
                # 创建并显示子窗口
                child_window = ChildWindow('漏失数据图')
                child_window.setCentralWidget(self.canvas)
                # 显示子窗口
                self.mdiArea = self.parent.findChild(QMdiArea, 'mdiArea_2')
                sub_window = QMdiSubWindow()
                sub_window.setWidget(child_window)
                self.mdiArea.addSubWindow(sub_window)
                sub_window.show()
                # 提醒用户绘图完成
                QMessageBox.information(self.parent, "提示", "绘图完成！请点击图像窗口查看！")
            except:
                QMessageBox.warning(self.parent, "警告", "绘图失败！出现了一点小问题~")

    def save_figure(self):
        if self.figure:
            # 使用QFileDialog获取用户选择的保存路径
            filename, _ = QFileDialog.getSaveFileName(self.parent, 'Save the image', 'depth-loss',
                                                      'PNG Files (*.png);;JPEG Files (*.jpg)')
            if filename:
                # 根据用户选择的路径和格式保存figure
                self.figure.savefig(filename, dpi=400)
        else:
            return

    def on_toolButton_2_clicked(self):
        # 实例化合并数据类
        mergedata = MergeData()

        # 连接到SQLite数据库（文件名为'DATA.db'），并开始一个事务
        db_filename = 'DATA.db'
        conn = sqlite3.connect(db_filename)
        # 创建一个游标对象
        cursor = conn.cursor()
        # 检查指定的表格是否存在
        tables_to_check = ['DDR', 'FDR', 'Drillingdata']
        table_count_query = """

            SELECT COUNT(*) 

            FROM sqlite_master 

            WHERE type = 'table' AND name IN ({});

        """.format(','.join(['?'] * len(tables_to_check)))
        cursor.execute(table_count_query, tables_to_check)
        # 获取查询结果
        count_of_tables = cursor.fetchone()[0]
        # 检查是否已选择工作区，如果没有则显示警告消息并返回
        # 不要忘记关闭数据库连接
        conn.close()
        if not self.parent.workspace_selected:
            QMessageBox.warning(self.parent, "警告", "请先新建或选择工作区！")
            return
        elif not count_of_tables == len(tables_to_check):
            QMessageBox.warning(self.parent, "警告", "请提取完成需要的全部数据!")
            return

        else:
            print("可以执行！")
            self.thread_merge = TaskThread(mergedata.merge_data)
            self.thread_merge.result_signal.connect(self.handle_result_mergedata)
            self.thread_merge.progress_signal.connect(lambda msg: self.update_status_bar(msg))
            self.thread_merge.finished_signal.connect(self.clear_progress_message)
            # 回收线程
            self.thread_merge.finished_signal.connect(self.thread_merge.deleteLater)
            self.thread_merge.start()

    # 处理工具栏按钮点击事件的槽函数，这个是提取数据的槽函数
    def on_toolButton_clicked(self):
        # 检查是否已选择工作区，如果没有则显示警告消息并返回
        if not self.parent.workspace_selected:
            QMessageBox.warning(self.parent, "警告", "请先新建或选择工作区！")
            return
        else:
            # 设置文件过滤器为Excel和PDF文件类型
            filters = "Excel Files (*.xlsx *.xls);;PDF Files (*.pdf)"
            # 弹出文件对话框让用户选择一个文件
            filename, _ = QFileDialog.getOpenFileName(self.parent, "选择文件", QDir.homePath(), filters)

            # 如果用户选择了文件，则调用handle_selected_file方法处理该文件
            if filename:
                print(filename)
                self.handle_selected_file(filename)

    # 提取选定文件数据并进行处理的函数
    def handle_selected_file(self, filename):
        # 获取文件扩展名小写形式
        file_extension = filename.split(".")[-1].lower()
        extract_data = ExtractData(filename)
        # 当文件为包含"DrillingData"的Excel文件时
        if (file_extension == "xlsx" or file_extension == "xls") and "DrillingData" in filename:
            self.thread = TaskThread(extract_data.extract_drillingdata)
            self.thread.result_signal.connect(self.handle_result)
            self.thread.progress_signal.connect(lambda msg: self.update_status_bar(msg))
            self.thread.finished_signal.connect(self.clear_progress_message)
            # 回收线程
            self.thread.finished_signal.connect(self.thread.deleteLater)
            self.thread.start()

        # 对于其他情况，如包含"DDR"的Excel文件或PDF文件，暂不处理
        elif (file_extension == "xlsx" or file_extension == "xls") and "DDR" in filename:
            self.thread = TaskThread(extract_data.extract_ddrdata)
            self.thread.result_signal.connect(self.handle_result)
            self.thread.progress_signal.connect(lambda msg: self.update_status_bar(msg))
            self.thread.finished_signal.connect(self.clear_progress_message)
            self.thread.start()

        elif file_extension == "pdf":
            self.thread = TaskThread(extract_data.extract_pdfdata)
            self.thread.result_signal.connect(self.handle_result)
            self.thread.progress_signal.connect(lambda msg: self.update_status_bar(msg))
            self.thread.finished_signal.connect(self.clear_progress_message)
            self.thread.start()

        else:
            # 对于不支持的文件类型，输出提示信息
            print("不支持的文件类型")
            QMessageBox.warning(
                self.parent,  # 父窗口
                "数据提取失败",  # 标题
                "不支持的文件类型!请检查文件名",  # 提示信息
                QMessageBox.Ok)

    def handle_result_mergedata(self, result):
        if isinstance(result, bool) and result:
            QMessageBox.information(
                self.parent,
                "数据合并成功",
                "数据合并成功！请点击菜单栏Refresh按钮更新工作区数据",
                QMessageBox.Ok)
            # 在Windows下尝试打开Excel文件
            os.startfile('output_data.xlsx')
        else:
            QMessageBox.warning(
                self.parent,
                "数据合并失败",
                f"数据合并失败！原因：{result}",
                QMessageBox.Ok)

    def handle_result(self, result):
        if isinstance(result, bool) and result:
            QMessageBox.information(
                self.parent,
                "数据提取成功",
                "数据提取成功！请点击菜单栏Refresh按钮更新工作区数据",
                QMessageBox.Ok)
        else:
            QMessageBox.warning(
                self.parent,
                "数据提取失败",
                f"数据提取失败！原因：{result}",
                QMessageBox.Ok)

    def update_status_bar(self, message):

        self.parent.statusBar().showMessage(message)

    def clear_progress_message(self):

        self.parent.statusBar().showMessage(f"当前工作区: {os.getcwd()}")
