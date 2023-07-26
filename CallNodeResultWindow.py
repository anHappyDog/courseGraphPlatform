import sys

import pymysql
from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QTableView

from AppInfo import AppInfo
from NodeResultWindow import Ui_NodeResultWindow
from MyWidget import MyNeo4jView
from MySignals import myNodeResultSignal


class MyNodeResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.ui = Ui_NodeResultWindow()
        self.ui.setupUi(self)
        self.__initDatabaseConnAndResult()
        myNodeResultSignal.myNodeResultSignal.connect(self.setCourse)
        self.ui.platformSortBtns.addItem('All')
        self.ui.platformSortBtns.addItems(self.coursePlatform)
        self.ui.platformSortBtns.currentTextChanged.connect(self.__platfomBoxChanged)
        self.ui.nodeResult.setEditTriggers(QTableView.NoEditTriggers)
        proxyModel = QSortFilterProxyModel()
        proxyModel.setSourceModel(self.model)
        self.ui.nodeResult.setModel(proxyModel)
        self.ui.commentsRadBtn.clicked.connect(self.__sortedByComments)
        self.ui.durationRadBtn.clicked.connect(self.__sortedByDuration)
        self.ui.playsRadBtn.clicked.connect(self.__sortedByPlays)
        self.ui.nameRadBtn.clicked.connect(self.__sortedByName)

    def __sortedByName(self):
        self.ui.nodeResult.model().sort(0,Qt.DescendingOrder)

    def __sortedByDuration(self):
        self.ui.nodeResult.model().sort(4, Qt.DescendingOrder)

    def __sortedByPlays(self):
        self.ui.nodeResult.model().sort(2, Qt.DescendingOrder)

    def __sortedByComments(self):
        self.ui.nodeResult.model().sort(3, Qt.DescendingOrder)

    def __platfomBoxChanged(self):
        selectText = self.ui.platformSortBtns.currentText()
        if selectText == 'All':
            filterText = ''
        else:
            filterText = selectText
        if filterText:
            self.ui.nodeResult.model().setFilterRegExp(filterText)
            self.ui.nodeResult.model().setFilterKeyColumn(1)
        else:
            self.ui.nodeResult.model().setFilterRegExp('')
            self.ui.nodeResult.model().setFilterKeyColumn(-1)

    def addRow(self, data):
        row_count = self.model.rowCount()  # 获取当前的行数
        self.ui.nodeResult.model().insertRow(row_count)  # 在最后插入一行
        for i in range(len(self.columnList)):
            self.ui.nodeResult.model().setData(self.ui.nodeResult.model().index(row_count, i), data[i])

    def __initDatabaseConnAndResult(self):
        self.course = None
        self.dbConnection = pymysql.connect(host=AppInfo.DatabaseInfo.host, user=AppInfo.DatabaseInfo.user
                                            , password=AppInfo.DatabaseInfo.password,
                                            database=AppInfo.DatabaseInfo.database)
        with self.dbConnection.cursor() as cur:
            cur.execute('Desc ' + AppInfo.DatabaseInfo.courseDbName)
            result = cur.fetchall()
            self.columnList = [col[0] for col in result]
            cur.execute('select * from %s;' % AppInfo.DatabaseInfo.platformDbName)
            result = cur.fetchall()
            self.coursePlatform = [col[0] for col in result]
            self.model = QStandardItemModel(0, len(self.columnList))
            self.ui.nodeResult.setModel(self.model)
            self.model.setHorizontalHeaderLabels(self.columnList)

    def setCourse(self, course):
        with self.dbConnection.cursor() as cur:
            cur.execute('select * from ' + AppInfo.DatabaseInfo.courseDbName + f' where courseName=\'{course}\'')
            result = cur.fetchall()
            for i in range(self.ui.nodeResult.model().rowCount() - 1, -1, -1):
                self.ui.nodeResult.model().removeRow(i)
            for row, line in enumerate(list(result)):
                self.addRow(line)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyNodeResultWindow()
    win.setCourse('操作系统')
    win.show()
    sys.exit(app.exec_())
