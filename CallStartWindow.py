import enum
import re

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from StartWindow import Ui_StartWindow
from enum import Enum
import pymysql

from CallMainWindow import MyMainWindow


class MyStartWindow(QMainWindow):
    __dbHost = '127.0.0.1'
    __dbPassowrd = 'ilikeyou2003'
    __dbName = 'test1'
    __dbUser = 'root'
    __userTable = 'user'

    class ErrorCode(Enum):
        NoSuchUser = 1
        WrongPasswd = 2
        HasBeenSignUpped = 3
        SuccessProcedure = 4
        NoSuchUserTable = 5
        WrongFormat = 6
    def __init__(self):
        super().__init__()
        self.__initUI()
        self.__connectToUserDb()

    def __initUI(self):
        self.ui = Ui_StartWindow()
        self.ui.setupUi(self)
        self.ui.passwdLineEdit.setMaxLength(9)
        self.ui.usernameLineEdit.setMaxLength(9)
        self.ui.usernameLineEdit.setPlaceholderText('1 - 9 chars and nums')
        self.ui.passwdLineEdit.setPlaceholderText('1 - 9 chars and nums')
        self.ui.passwdLineEdit.setEchoMode(QLineEdit.Password)
        self.ui.signUpBtn.clicked.connect(self.signUp)
        self.ui.signInBtn.clicked.connect(self.signIn)

    @pyqtSlot()
    def signIn(self):
        username, password = self.__getUserInfo()
        errCode = self.__isSignInSuccess(username, password)
        if errCode == self.ErrorCode.SuccessProcedure:
            self.__signInSuccess(username)
        else:
            self.__signInFailed(errCode)

    @pyqtSlot()
    def signUp(self):
        username, password = self.__getUserInfo()
        errCode = self.__isSignUpSuccess(username, password)
        if errCode == self.ErrorCode.SuccessProcedure:
            self.__signUpSuccess()
        else:
            self.__signUpFailed(errCode)

    def __connectToUserDb(self):
        self.userDb = pymysql.connect(host=self.__dbHost, user=self.__dbUser,
                                      password=self.__dbPassowrd, database=self.__dbName)

    def __getUserInfo(self):
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwdLineEdit.text()
        return username, password

    def __signUpSuccess(self):
        self.userDb.commit()
        self.ui.statusbar.showMessage('sign up successfully', 5000)


    def __isSignUpSuccess(self, username, password):
        pattern = re.compile(r'[^a-zA-Z0-9]')
        if bool(pattern.search(username)) or bool(pattern.search(password)):
            return self.ErrorCode.WrongFormat
        with self.userDb.cursor() as cur:
            cur.execute('SHOW TABLES like \'{}\';'.format(self.__userTable))
            if cur.rowcount == 0:
                return self.ErrorCode.NoSuchUserTable
            cur.execute('SELECT * FROM {} WHERE username = \'{}\';'.format(self.__userTable, username))
            if cur.rowcount != 0:
                return self.ErrorCode.HasBeenSignUpped
            cur.execute('INSERT INTO {} (username,password) VALUES(\'{}\',\'{}\') '.format(self.__userTable, username,
                                                                                           password))
            return self.ErrorCode.SuccessProcedure

    def __signUpFailed(self, errorCode):
        if errorCode == self.ErrorCode.NoSuchUserTable:
            self.ui.statusbar.showMessage('system error , please contact the programer!', 5000)
        elif errorCode == self.ErrorCode.HasBeenSignUpped:
            self.ui.statusbar.showMessage('the username has been sign-upped', 5000)
        elif errorCode == self.ErrorCode.WrongFormat:
            self.ui.statusbar.showMessage('wrong username or password format!!!',5000)
    def __isSignInSuccess(self, username, password):
        with self.userDb.cursor() as cur:
            cur.execute('SHOW TABLES like \'{}\';'.format(self.__userTable))
            if cur.rowcount == 0:
                return self.ErrorCode.NoSuchUserTable
            cur.execute('SELECT password FROM {} WHERE username = \'{}\';'.format(self.__userTable, username))
            if cur.rowcount == 0:
                return self.ErrorCode.NoSuchUser
            rightPasswd = cur.fetchone()[0]
            if rightPasswd != password:
                return self.ErrorCode.WrongPasswd
            return self.ErrorCode.SuccessProcedure

    def __signInSuccess(self, username):
        self.ui.statusbar.showMessage('sign in successfully', 5000)
        self.mainWindow = MyMainWindow(username)
        self.mainWindow.show()
        self.close()



    def __signInFailed(self, errorCode):
        if errorCode == self.ErrorCode.NoSuchUserTable:
            self.ui.statusbar.showMessage('system error , please contact the programer!', 5000)
        elif errorCode == self.ErrorCode.NoSuchUser:
            self.ui.statusbar.showMessage('no such user, please sign up first!', 5000)

        elif errorCode == self.ErrorCode.WrongPasswd:
            self.ui.statusbar.showMessage('the password is wrong!', 5000)
