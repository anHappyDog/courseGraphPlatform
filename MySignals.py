from PyQt5.QtCore import pyqtSignal, QObject


class MyNodeResultSignal(QObject):
    myNodeResultSignal = pyqtSignal(str)


class MyChangeStackedWidgetSignal(QObject):
    myChangeStackWidgetSignal = pyqtSignal(int)


class MyPassSelectGraphSignal(QObject):
    myPassSelectGraphSignal = pyqtSignal(str)


class MyDeleteGraphInListPageSignal(QObject):
    myDeleteGraphInListPageSignal = pyqtSignal(str)


class MyAddGraphBookMarkSignal(QObject):
    myAddGraphBookMarkSignal = pyqtSignal(str)


class MyPassMessageToMainSignal(QObject):
    myPassMessageToMainSignal = pyqtSignal(str)


myPassSelectGraphSignal = MyPassSelectGraphSignal()
myNodeResultSignal = MyNodeResultSignal()
myChangeStackWidgetSignal = MyChangeStackedWidgetSignal()
myDeleteGraphInListPageSignal = MyDeleteGraphInListPageSignal()
myAddGraphBookMarkSignal = MyAddGraphBookMarkSignal()
myPassMessageToMainSignal = MyPassMessageToMainSignal()