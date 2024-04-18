from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from pygame import mixer 


import equlizer_operations
from filepaths import Filepaths
from utilites import *

    
class UI_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Filepaths.MAIN_WINDOW_V2(), self)
        self.setWindowTitle('Tune-it')
        # self.setFixedSize(1200, 700)
        
        "initializing necessary objects"
        self.audio_file_path = None
        self.audio_file_loaded = ValueProperty(False)
        

        """Loading necessary objects from the loaded ui."""
        self.play_pause_btn_org = self.findChild(QPushButton, "play_pause_btn_org")
        


        """Some event handlers needed for different operations."""
        self.action_save_as.setEnabled(False)
        self.action_save.setEnabled(False)
        
        self.action_open.triggered.connect(self.open_file)
        self.action_save_as.triggered.connect(self.save_new_file)
        
        self.audio_file_loaded.valueChanged.connect(self.load_audio_to_mixer)
        self.play_pause_btn_org.clicked.connect(lambda: print("pressed"))
        
        
             
        mixer.init() 
        mixer.music.set_volume(0.7)


    def choose_file(self):
        """
        Opens a file dialog. lets the user choose a file to open and returns the path of the file.
        :return: the path of the selected file.
        """
        file_dialogue = QFileDialog(self)
        filters = "Audio (*.mp3 *.wav)"
        filenames, _ = file_dialogue.getOpenFileNames(self, filter=filters)
        if not filenames:
            return None
        return filenames[0]

    def open_file(self):
        """
        Clicking 'Open' or pressing Ctrl+O \n
        Opens an audio file and loads it into the screen.\n
        * Opens a file dialog. Using the choose_file() method.
        * If you select an audio file, it loads the audio.
        :return:
        """
        audio_file_path = self.choose_file()
        self.enable_all()
        
        if audio_file_path:
            self.audio_file_path = audio_file_path
        
        self.audio_file_loaded.value = True
        

    def enable_all(self):
        self.action_save_as.setEnabled(True)
        self.action_save.setEnabled(True)
        # self.blur_select_button.setEnabled(True)
        # self.rotate_button.setEnabled(True)

    def save_new_file(self):
        """
        Clicking 'Save as' or pressing Ctrl+Shift+S. \n
        If you want to save the audio file for the first time, you need to create a file. \n
        So a file-dialogue will open to get the directory and the filename.
        :return:
        """
        file_dialogue = QFileDialog(self)
        filters = "Audio (*.mp3 *.wav)"
        file_path, _ = file_dialogue.getSaveFileName(filter=filters, parent=self)
        self.save_file_path = file_path
        if file_path:
            # save the audio file here
            pass

    def save_file(self):
        """
        Clicking 'Save' or pressing Ctrl+S. \n
        Save the file, when the save-file already exists/created,
        :return:
        """
        if self.save_file_path:
            # save the audio file here
            pass
        else:  # If the save-file is not created, call save_new_file()
            self.save_new_file()

    def load_audio_to_mixer(self):
        if self.audio_file_loaded.value:
            self.audio_file_loaded.value = False
            mixer.music.load(self.audio_file_path)
            mixer.music.play()
            
        