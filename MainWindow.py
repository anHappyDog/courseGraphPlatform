# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 611)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphListBtn = QtWidgets.QPushButton(self.centralwidget)
        self.graphListBtn.setObjectName("graphListBtn")
        self.verticalLayout.addWidget(self.graphListBtn)
        self.bookMarkBtn = QtWidgets.QPushButton(self.centralwidget)
        self.bookMarkBtn.setObjectName("bookMarkBtn")
        self.verticalLayout.addWidget(self.bookMarkBtn)
        self.graphShowBtn = QtWidgets.QPushButton(self.centralwidget)
        self.graphShowBtn.setObjectName("graphShowBtn")
        self.verticalLayout.addWidget(self.graphShowBtn)
        self.nodeResultBtn = QtWidgets.QPushButton(self.centralwidget)
        self.nodeResultBtn.setObjectName("nodeResultBtn")
        self.verticalLayout.addWidget(self.nodeResultBtn)
        self.userInfoBtn = QtWidgets.QPushButton(self.centralwidget)
        self.userInfoBtn.setObjectName("userInfoBtn")
        self.verticalLayout.addWidget(self.userInfoBtn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.horizontalLayout_2)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.graphListBtn.setText(_translate("MainWindow", "我的图谱"))
        self.bookMarkBtn.setText(_translate("MainWindow", "我的书签"))
        self.graphShowBtn.setText(_translate("MainWindow", "图谱展示"))
        self.nodeResultBtn.setText(_translate("MainWindow", "查询结果"))
        self.userInfoBtn.setText(_translate("MainWindow", "个人中心"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
