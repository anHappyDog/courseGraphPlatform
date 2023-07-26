import sys

import pymysql
from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QStatusBar
from BookMarkWindow import Ui_BookMarkWindow
from AppInfo import AppInfo
from MySignals import myChangeStackWidgetSignal
from MySignals import myPassSelectGraphSignal
from MySignals import myDeleteGraphInListPageSignal
from MySignals import myAddGraphBookMarkSignal

class MyBookMarkWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.__initSetting()

    def __initSetting(self):
        self.ui = Ui_BookMarkWindow()
        self.ui.setupUi(self)
        self.bookSqlConnection = pymysql.connect(host=AppInfo.DatabaseInfo.host, user=AppInfo.DatabaseInfo.user,
                                                 password=AppInfo.DatabaseInfo.password,
                                                 database=AppInfo.DatabaseInfo.database)
        self.ui.openGraphBtn.clicked.connect(self.__openGraph)
        self.ui.delFromBookMarkBtn.clicked.connect(self.__delGraphFromBookMark)
        self.ui.bookMarkList.itemClicked.connect(self.__enableBtns)
        self.__disableBtns()
        self.installEventFilter(self)
        self.__fillData()
        myDeleteGraphInListPageSignal.myDeleteGraphInListPageSignal.connect(self.__deleteNode)
        myAddGraphBookMarkSignal.myAddGraphBookMarkSignal.connect(self.__addBookMark)
    def __deleteNode(self, name):
        item = self.ui.bookMarkList.findItems(name, Qt.MatchExactly)[0]
        self.ui.bookMarkList.takeItem(self.ui.bookMarkList.row(item))

    def __addBookMark(self,name):
        self.ui.bookMarkList.addItem(name)
    def __fillData(self):
        self.ui.bookMarkList.clear()
        with self.bookSqlConnection.cursor() as cur:
            cur.execute(
                'SELECT neo4jName from ' + AppInfo.DatabaseInfo.userNeo4jListDbName +
                ' where isBookMark=1 AND username=\'%s\';' % self.username)
            result = cur.fetchall()
            result = [t[0] for t in result]
            self.ui.bookMarkList.addItems(result)

    def __openGraph(self):
        myChangeStackWidgetSignal.myChangeStackWidgetSignal.emit(AppInfo.SUB_WINDOW.GRAPH_SHOW.value)
        myPassSelectGraphSignal.myPassSelectGraphSignal.emit(
            self.username + "_" + self.ui.bookMarkList.selectedItems()[0].text())

    def __delGraphFromBookMark(self):
        item = self.ui.bookMarkList.selectedItems()[0]
        with self.bookSqlConnection.cursor() as cur:
            cur.execute(
                'UPDATE ' + AppInfo.DatabaseInfo.userNeo4jListDbName +
                ' SET isBookMark=0 WHERE username=\'%s\' AND neo4jName=\'%s\''
                % (self.username, item.text()))
            self.bookSqlConnection.commit()
        self.ui.bookMarkList.takeItem(self.ui.bookMarkList.row(item))

    def __enableBtns(self):
        self.ui.delFromBookMarkBtn.setEnabled(True)
        self.ui.openGraphBtn.setEnabled(True)

    def __disableBtns(self):
        self.ui.delFromBookMarkBtn.setEnabled(False)
        self.ui.openGraphBtn.setEnabled(False)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj == self and event.type() == QEvent.MouseButtonPress:
            self.__disableBtns()
        return super().eventFilter(obj, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyBookMarkWindow('T1')
    win.show()
    sys.exit(app.exec_())
