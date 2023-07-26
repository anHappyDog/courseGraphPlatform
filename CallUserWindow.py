import sys

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QPushButton
from UserWindow import Ui_Form


class MyUserWindow(QWidget):
    def __init__(self, userName):
        super().__init__()
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.resize(400, 300)
        self.ui.lineEdit.setText(userName)
        self.ui.signOutBtn.clicked.connect(self.__signOut)

    def __signOut(self):
        QApplication.exit(0)


    #
    # def closeEvent(self, a0: QCloseEvent) -> None:
    #     print('sad')

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     t = MyUserWindow()
#     t.show()
#     sys.exit(app.exec_())
