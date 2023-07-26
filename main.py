import sys

from PyQt5.QtWidgets import QApplication

from CallStartWindow import MyStartWindow
from CallMainWindow import MyMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    startWindow = MyStartWindow()
    startWindow.show()
    sys.exit(app.exec_())
