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
        login VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        mail VARCHAR(255) UNIQUE,
        created VARCHAR(100), 
        balance INTEGER
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
            cursor.execute(f"INSERT INTO users VALUES ('{login}', '{password}', '{mail}', '{time.ctime()}', 0);")
            self.error.setText("Успешно")
        except sqlite3.IntegrityError as s:
            if s.args == "('UNIQUE constraint failed: users.login',)":
                self.error.setText("Логин уже занят.")
            elif s.args == ('UNIQUE constraint failed: users.mail',):
                self.error.setText("Почта уже занята.")
            else:
                self.error.setText("Логин занят.")
        self.db.connect.commit()

class Personal(QWidget):
    def __init__(self, login):
        super(Personal, self).__init__()
        self.login = login
        loadUi('personal.ui', self)
        self.username.setText(login)
        self.db = StartDB()
        cursor = self.db.connect.cursor()
        result = cursor.execute(f"SELECT balance FROM users WHERE login = '{login}';")
        self.balance.setText(f"{result.fetchall()[0][0]} KGS")
        self.make.clicked.connect(self.make_money)
        self.hide_transfer()
        self.transfer.clicked.connect(self.user_transfer)
        self.send.clicked.connect(self.user_transfer)
        self.db.connect.commit()

    def hide_transfer(self):
        self.login.hide()
        self.amount.hide()
        self.send.hide()
        self.result.hide()

    def show_transfer(self):
        self.login.show()
        self.amount.show()
        self.send.show()
        self.result.show()

    def update_balance(self):
        cursor = self.db.connect.cursor()
        result = cursor.execute(f"SELECT balance FROM users WHERE login = '{self.login}';")
        self.balance.setText(f"{result.fetchall()[0][0]} KGS")
        self.db.connect.commit()

    def make_money(self):
        cursor = self.db.connect.cursor()
        cursor.execute(f"UPDATE users SET balance = balance + {10} WHERE login = '{self.login}';")
        self.db.connect.commit()
        self.update_balance()
        
    def user_transfer(self):
        self.show_transfer()
        login = self.login.text()
        amount = self.amount.text()
        print(login, amount)
        cursor = self.db.connect.cursor()
        cursor.execute(f"SELECT login FROM users WHERE login = '{login}';")
        result = cursor.fetchmany()
        if result != []:
            cursor.execute(f"SELECT balance FROM users WHERE login = '{self.login}';")
            users_balance = cursor.fetchall()[0][0]
            
            if users_balance >= int(amount):
                print('OK')
            else:
                print('Ne OK')
        self.db.connect.commit()

class Bank(QMainWindow):
    def __init__(self):
        super(Bank, self).__init__()
        loadUi('Bank.ui', self)
        self.hide_error()
        self.signin.clicked.connect(self.check_login)
        self.class_signup = SignUp()
        self.signup.clicked.connect(self.show_signup)
        self.db = StartDB()

    def show_signup(self):
        self.class_signup.show()

    def hide_error(self):
        self.error.hide()

    def show_error(self):
        self.error.show()

    def check_login(self):
        login = self.login.text()
        password = self.password.text()
        cursor = self.db.connect.cursor()
        cursor.execute(f"SELECT * FROM users WHERE login = '{login}' AND password = '{password}';")
        result = cursor.fetchall()
        if result != []:
            self.show_error()
            self.error.setText('Ok')
            self.personal = Personal(login)
            self.personal.show()
        else:
            self.show_error()
            self.error.setText("Неправильные данные")

app = QApplication(sys.argv)
bank = Bank()
bank.show()
app.exec_()