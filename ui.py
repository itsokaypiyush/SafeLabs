from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

class SafeLog(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.timeout.connect(self.lock_screen)
        self.reset_timer()

    def initUI(self):
        self.setWindowTitle("SafeLog - Secure Auto Logout")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: white;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #bb86fc;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #bb86fc;
                border-radius: 8px;
                background-color: #2c2c3e;
                color: white;
            }
            QPushButton {
                background-color: #6200ea;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3700b3;
            }
        """)

        self.label = QLabel("🔒 Welcome to SafeLog", self)
        self.label.setFont(QFont("Arial", 16))

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login", self)
        self.login_btn.clicked.connect(self.check_password)

        self.logout_btn = QPushButton("Logout", self)
        self.logout_btn.clicked.connect(self.logout)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.logout_btn)

        self.setLayout(layout)

    def check_password(self):
        password = self.password_input.text()
        if password == "test123":  # TODO: Replace with real authentication
            self.label.setText("✅ Login Successful")
            self.reset_timer()
        else:
            self.label.setText("❌ Invalid Password")

    def reset_timer(self):
        self.inactivity_timer.start(120000)  # 2-minute auto logout

    def lock_screen(self):
        self.label.setText("🔒 Session Locked! Enter password to continue.")
        self.password_input.clear()

    def logout(self):
        self.label.setText("🔓 You have been logged out!")
        self.password_input.clear()

if __name__ == "__main__":
    app = QApplication([])
    window = SafeLog()
    window.show()
    app.exec_()
