import sys
from widgets import main_window
from PyQt6.QtWidgets import QApplication


def add_stylesheet_to_app(app):
    try:
        with open("styles.css", "r") as file:
            app.setStyleSheet(file.read())
    except:
        print('Could not attach the stylesheet')


def main():
    app = QApplication(sys.argv)
    add_stylesheet_to_app(app)
    _main_window = main_window.UI_MainWindow()
    _main_window.show()
    app.exec()

if __name__ == "__main__":
    main()