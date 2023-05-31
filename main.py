import sys

from server.ui import UI

from PyQt5.QtWidgets import QMainWindow, QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    ui = UI()
    ui.setupUi(MainWindow)
    ui.init_connect()

    MainWindow.show()

    sys.exit(app.exec())
