# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GraphListWindow(object):
    def setupUi(self, GraphListWindow):
        GraphListWindow.setObjectName("GraphListWindow")
        GraphListWindow.resize(775, 300)
        self.gridLayout = QtWidgets.QGridLayout(GraphListWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.searchGraphInput = QtWidgets.QLineEdit(GraphListWindow)
        self.searchGraphInput.setObjectName("searchGraphInput")
        self.gridLayout.addWidget(self.searchGraphInput, 0, 0, 1, 1)
        self.searchGraphBtn = QtWidgets.QPushButton(GraphListWindow)
        self.searchGraphBtn.setObjectName("searchGraphBtn")
        self.gridLayout.addWidget(self.searchGraphBtn, 0, 1, 1, 1)
        self.addGraphInput = QtWidgets.QLineEdit(GraphListWindow)
        self.addGraphInput.setObjectName("addGraphInput")
        self.gridLayout.addWidget(self.addGraphInput, 1, 0, 1, 1)
        self.addGraphBtn = QtWidgets.QPushButton(GraphListWindow)
        self.addGraphBtn.setObjectName("addGraphBtn")
        self.gridLayout.addWidget(self.addGraphBtn, 1, 1, 1, 1)
        self.neo4jList = QtWidgets.QListWidget(GraphListWindow)
        self.neo4jList.setObjectName("neo4jList")
        self.gridLayout.addWidget(self.neo4jList, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line = QtWidgets.QFrame(GraphListWindow)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.bookMarkBtn = QtWidgets.QPushButton(GraphListWindow)
        self.bookMarkBtn.setObjectName("bookMarkBtn")
        self.verticalLayout.addWidget(self.bookMarkBtn)
        self.delGraphBtn = QtWidgets.QPushButton(GraphListWindow)
        self.delGraphBtn.setObjectName("delGraphBtn")
        self.verticalLayout.addWidget(self.delGraphBtn)
        self.lookGraphBtn = QtWidgets.QPushButton(GraphListWindow)
        self.lookGraphBtn.setObjectName("lookGraphBtn")
        self.verticalLayout.addWidget(self.lookGraphBtn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.retranslateUi(GraphListWindow)
        QtCore.QMetaObject.connectSlotsByName(GraphListWindow)

    def retranslateUi(self, GraphListWindow):
        _translate = QtCore.QCoreApplication.translate
        GraphListWindow.setWindowTitle(_translate("GraphListWindow", "graphsListWindow"))
        self.searchGraphBtn.setText(_translate("GraphListWindow", "搜索图谱"))
        self.addGraphBtn.setText(_translate("GraphListWindow", "添加图谱"))
        self.bookMarkBtn.setText(_translate("GraphListWindow", "设为书签"))
        self.delGraphBtn.setText(_translate("GraphListWindow", "删除图谱"))
        self.lookGraphBtn.setText(_translate("GraphListWindow", "查看图谱"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GraphListWindow = QtWidgets.QWidget()
    ui = Ui_GraphListWindow()
    ui.setupUi(GraphListWindow)
    GraphListWindow.show()
    sys.exit(app.exec_())
