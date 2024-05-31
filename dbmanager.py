# dbmanager.py 文件内容
#管理子窗口数据库的函数
from PyQt5.QtSql import QSqlDatabase
class DatabaseManager:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = None

    def open_connection(self):
        self.connection = QSqlDatabase.addDatabase("QSQLITE", f"{self.database_name}_connection")
        self.connection.setDatabaseName(self.database_name)
        if not self.connection.open():
            print(f"无法打开数据库 {self.database_name}")
            return False
        return True

    def close_connection(self):
        if QSqlDatabase.contains(f"{self.database_name}_connection"):
            db_connection = QSqlDatabase.database(f"{self.database_name}_connection")
            db_connection.commit()
            db_connection.close()

            connection = db_connection.connectionName()
            db_connection = QSqlDatabase()
            db_connection.removeDatabase(connection)
