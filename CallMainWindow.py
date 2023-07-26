import sys
from enum import Enum

from PyQt5.QtWidgets import QMainWindow, QApplication

from CallGraphicWindow import MyGraphicWidget
from CallNodeResultWindow import MyNodeResultWindow
from CallUserWindow import MyUserWindow
from CallBookMarkWindow import MyBookMarkWindow
from MainWindow import Ui_MainWindow
from CallGraphsWindow import MyGraphsWindow
from AppInfo import AppInfo
from MySignals import myChangeStackWidgetSignal
from MySignals import myPassMessageToMainSignal

class MyMainWindow(QMainWindow):

    def __init__(self, username):
        self.username = username
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.addWidget(MyGraphsWindow(self.username))
        self.ui.stackedWidget.addWidget(MyBookMarkWindow(self.username))
        self.ui.stackedWidget.addWidget(MyGraphicWidget())
        self.ui.stackedWidget.addWidget(MyNodeResultWindow())
        self.ui.stackedWidget.addWidget(MyUserWindow(self.username))
        self.ui.graphListBtn.clicked.connect(lambda: self.changeSubWindow(AppInfo.SUB_WINDOW.GRAPH_LIST.value))
        self.ui.bookMarkBtn.clicked.connect(lambda: self.changeSubWindow(AppInfo.SUB_WINDOW.BOOK_MARK.value))
        self.ui.graphShowBtn.clicked.connect(lambda: self.changeSubWindow(AppInfo.SUB_WINDOW.GRAPH_SHOW.value))
        self.ui.nodeResultBtn.clicked.connect(lambda: self.changeSubWindow(AppInfo.SUB_WINDOW.NODE_RESULT.value))
        self.ui.userInfoBtn.clicked.connect(lambda: self.changeSubWindow(AppInfo.SUB_WINDOW.USER_INFO.value))
        myChangeStackWidgetSignal.myChangeStackWidgetSignal.connect(self.changeSubWindow)
        myPassMessageToMainSignal.myPassMessageToMainSignal.connect(self.printStatusMessage)

    def printStatusMessage(self, text):
        self.ui.statusbar.showMessage(text, 5000)

    def changeSubWindow(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)
        # for i in range(self.ui.stackedWidget.count()):
        #     window = self.ui.widget(i)
        #     print("Window {} content: {}".format(i, window.layout().itemAt(0).widget().text()))

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = MyMainWindow()
#     mainWindow.showMaximized()
#     sys.exit(app.exec_())
