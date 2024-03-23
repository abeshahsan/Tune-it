import sys
from widgets import main_window
from PyQt6.QtWidgets import QApplication

from pydub import AudioSegment
from pydub.playback import play

AudioSegment.ffmpeg = "H:/UNI_STUFF/6th Sem/DSP Lab/Project"

def add_stylesheet_to_app(app):
    try:
        with open("styles.css", "r") as file:
            app.setStyleSheet(file.read())
    except:
        print('Could not attach the stylesheet')


def play_music(file):
    sound = AudioSegment.from_mp3(file)
    play(sound)

def main():
    app = QApplication(sys.argv)
    add_stylesheet_to_app(app)
    _main_window = main_window.UI_MainWindow()
    _main_window.show()
    app.exec()

if __name__ == "__main__":
    main()
