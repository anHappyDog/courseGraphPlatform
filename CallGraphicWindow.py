import sys

import pymysql
from PyQt5.QtWidgets import QWidget, QApplication
from AppInfo import AppInfo
import GraphicWindow


class MyGraphicWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = GraphicWindow.Ui_Form()
        self.ui.setupUi(self)
        self.__initSetting()

    def __initSetting(self):
        self.ui.addNodeBtn.clicked.connect(self.__addNode)
        self.ui.deleteNodeBtn.clicked.connect(self.__delNode)
        with pymysql.connect(host=AppInfo.DatabaseInfo.host, user=AppInfo.DatabaseInfo.user,
                             password=AppInfo.DatabaseInfo.password,
                             database=AppInfo.DatabaseInfo.database) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT name from {};'.format(AppInfo.DatabaseInfo.courseNameDb))
                result = cur.fetchall()
                result = [t[0] for t in result]
                self.ui.comboBox.addItems(result)

    def __addNode(self):
        text = self.ui.comboBox.currentText()
        nodes = self.ui.graphicsView.nodes
        if text not in nodes.keys():
            self.ui.graphicsView.addNode(text,True)

    def __delNode(self):
        text = self.ui.comboBox.currentText()
        nodes = self.ui.graphicsView.nodes
        if text in nodes:
            self.ui.graphicsView.delNode(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyGraphicWidget()
    win.showMaximized()
    sys.exit(app.exec_())
