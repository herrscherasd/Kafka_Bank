from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi
import sqlite3
import time
import sys

class StartDB():
    def __init__(self):
        self.connect = sqlite3.connect('bank.db')
        self.connect.execute("""
        CREATE TABLE IF NOT EXISTS users(
        login VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        mail VARCHAR(255) NOT NULL UNIQUE,
        created VARCHAR(100)
        );
        """)
        self.connect.commit()
        
class SignUp(QWidget):
    def __init__(self):
        super(SignUp, self).__init__()
        loadUi('signup.ui', self)
        self.hide_error()
        self.db = StartDB()
        self.signup.clicked.connect(self.register)

    def hide_error(self):
        self.error.hide()

    def show_error(self):
        self.error.show()

    def register(self):
        login = self.login.text()
        password = self.password.text()
        mail = self.mail.text()
        self.show_error()
        cursor = self.db.connect.cursor()
        try:
            cursor.execute(f"INSERT INTO users VALUES ('{login}', '{password}', '{mail}', '{time.ctime()}');")
            self.error.setText("Успешно")
        except sqlite3.IntegrityError as s:
            print(s.args)
            if s.args == "('UNIQUE constraint failed: users.login',)":
                self.error.setText("Логин уже занят.")
            elif s.args == ('UNIQUE constraint failed: users.mail',):
                self.error.setText("Почта уже занята.")
            else:
                self.error.setText("Логин занят.")
        self.db.connect.commit()

class Bank(QMainWindow):
    def __init__(self):
        super(Bank, self).__init__()
        loadUi('Bank.ui', self)
        self.hide_error()
        self.signin.clicked.connect(self.check_login)
        self.class_signup = SignUp()
        self.signup.clicked.connect(self.show_signup)

    def show_signup(self):
        self.class_signup.show()

    def hide_error(self):
        self.error.hide()

    def show_error(self):
        self.error.show()

    def check_login(self):
        login = self.login.text()
        password = self.password.text()
        if login == 'geeks' and password == 'geeks2023':
            self.show_error()
            self.error.setText('Ok')
        else:
            self.show_error()
            self.error.setText("Неправильные данные")

app = QApplication(sys.argv)
bank = Bank()
bank.show()
app.exec_()