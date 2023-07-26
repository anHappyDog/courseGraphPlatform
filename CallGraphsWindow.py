import sys

import pymysql
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtWidgets import QWidget, QApplication
from neo4j import GraphDatabase

from AppInfo import AppInfo
from MySignals import myDeleteGraphInListPageSignal
from GraphWindow import Ui_GraphListWindow
from MySignals import myPassSelectGraphSignal, myChangeStackWidgetSignal
from MySignals import myAddGraphBookMarkSignal, myPassMessageToMainSignal


class MyGraphsWindow(QWidget):
    def __init__(self, username):
        self.username = username
        super().__init__()
        self.ui = Ui_GraphListWindow()
        self.ui.setupUi(self)
        self.__initSettings()

    def __initSettings(self):
        self.__getMysqlConnect()
        self.__getNeo4jList()
        self.installEventFilter(self)
        self.ui.neo4jList.itemClicked.connect(self.__enableBtns)
        self.__initBtns()
        self.neo4jConnection = GraphDatabase.driver(uri=AppInfo.Neo4jInfo.url, auth=AppInfo.Neo4jInfo.auth)
        self.ui.addGraphInput.setPlaceholderText('Only 9 characters!')
        self.ui.addGraphInput.setMaxLength(9)

    def __initBtns(self):
        self.ui.delGraphBtn.setEnabled(False)
        self.ui.lookGraphBtn.setEnabled(False)
        self.ui.bookMarkBtn.setEnabled(False)
        self.ui.delGraphBtn.clicked.connect(self.__deleteGraph)
        self.ui.addGraphBtn.clicked.connect(self.__addGraph)
        self.ui.lookGraphBtn.clicked.connect(self.__lookGraph)
        self.ui.searchGraphBtn.clicked.connect(self.__searchGraphs)
        self.ui.bookMarkBtn.clicked.connect(self.__bookMarkGraph)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj == self and event.type() == QEvent.MouseButtonPress:
            self.__disableBtns()
        return super().eventFilter(obj, event)

    def __addGraph(self):
        text = self.ui.addGraphInput.text()

        with self.mysqlConnect.cursor() as cur:
            cur.execute(
                'SELECT * FROM ' + AppInfo.DatabaseInfo.userNeo4jListDbName + ' WHERE username=\'%s\' AND neo4jName=\'%s\';' % (
                    self.username, text))
            if cur.rowcount != 0:
                myPassMessageToMainSignal.myPassMessageToMainSignal.emit('The graph\'s already been created!!!!')
                return
            myPassMessageToMainSignal.myPassMessageToMainSignal.emit('Creating the graph ....')
            cur.execute(
                'INSERT INTO ' + AppInfo.DatabaseInfo.userNeo4jListDbName + ' (username,neo4jName)  '
                                                                            'VALUES(\'%s\',\'%s\');' % (
                    self.username, text))
            self.mysqlConnect.commit()
        with self.neo4jConnection.session() as cur:
            cur.run('CREATE (:user%s_%s {name:\'计算机科学与技术\'})' % (self.username, text))
        self.ui.neo4jList.addItem(text)
        self.neo4jList.append(text)

    def __bookMarkGraph(self):
        item = self.ui.neo4jList.selectedItems()[0]
        with self.mysqlConnect.cursor() as cur:
            cur.execute(
                'SELECT isBookMark from ' + AppInfo.DatabaseInfo.userNeo4jListDbName + ' where username=\'%s\' AND neo4jName=\'%s\';' % (
                    self.username, item.text()))
            result = cur.fetchall()
            result = int(result[0][0])
            if result == 0:
                myAddGraphBookMarkSignal.myAddGraphBookMarkSignal.emit(item.text())
            cur.execute(
                'UPDATE ' + AppInfo.DatabaseInfo.userNeo4jListDbName + ' SET isBookMark=1 WHERE username=\'%s\' AND neo4jName=\'%s\';' % (
                    self.username, item.text()))
            self.mysqlConnect.commit()

    def __deleteGraph(self):
        item = self.ui.neo4jList.selectedItems()[0]
        self.neo4jList.remove(item.text())
        self.ui.neo4jList.takeItem(self.ui.neo4jList.row(item))
        with self.mysqlConnect.cursor() as cur:
            cur.execute(
                'SELECT * FROM ' + AppInfo.DatabaseInfo.userNeo4jListDbName + ' WHERE isBookMark=1 AND '
                                                                                     'username=\'%s\' AND '
                                                                                     'neo4jName=\'%s\'' % (
                    self.username, item.text()))
            if cur.rowcount != 0:
                myDeleteGraphInListPageSignal.myDeleteGraphInListPageSignal.emit(item.text())
            cur.execute(
                'DELETE FROM ' + AppInfo.DatabaseInfo.userNeo4jListDbName + ' WHERE username=\'%s\' AND neo4jName=\'%s\'' % (
                    self.username, item.text()))
            self.mysqlConnect.commit()
        with self.neo4jConnection.session() as cur:
            cur.run('MATCH (n:%s) DETACH DELETE n;' % ('user' + self.username + '_' + item.text()))

    def __lookGraph(self):
        myChangeStackWidgetSignal.myChangeStackWidgetSignal.emit(AppInfo.SUB_WINDOW.GRAPH_SHOW.value)
        myPassSelectGraphSignal.myPassSelectGraphSignal.emit(
            'user' + self.username + "_" + self.ui.neo4jList.selectedItems()[0].text())

    def __searchGraphs(self):
        text = self.ui.searchGraphInput.text()
        self.ui.neo4jList.clear()
        if text == '':
            self.ui.neo4jList.addItems(self.neo4jList)
        else:
            for neo4jName in self.neo4jList:
                if neo4jName == text:
                    self.ui.neo4jList.addItem(neo4jName)
                    break

    def __enableBtns(self):
        self.ui.delGraphBtn.setEnabled(True)
        self.ui.lookGraphBtn.setEnabled(True)
        self.ui.bookMarkBtn.setEnabled(True)

    def __disableBtns(self):
        self.ui.delGraphBtn.setEnabled(False)
        self.ui.lookGraphBtn.setEnabled(False)
        self.ui.bookMarkBtn.setEnabled(False)

    def __getMysqlConnect(self):
        self.mysqlConnect = pymysql.connect(host=AppInfo.DatabaseInfo.host, user=AppInfo.DatabaseInfo.user,
                                            password=AppInfo.DatabaseInfo.password,
                                            database=AppInfo.DatabaseInfo.database)

    # def __deleteNeo4jGraph(self,name):
    #
    def __getNeo4jList(self):
        with self.mysqlConnect.cursor() as cur:
            cur.execute(
                "SELECT neo4jName FrOM {} where username='{}'".format(AppInfo.DatabaseInfo.userNeo4jListDbName,
                                                                      self.username))
            result = cur.fetchall()
            self.neo4jList = [record[0] for record in result]
            self.ui.neo4jList.addItems(self.neo4jList)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyGraphsWindow('123')
    win.show()
    sys.exit(app.exec_())
