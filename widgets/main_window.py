import time
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from audio_equalizer import AudioEqualizer
from filepaths import Filepaths
from utilites import *
import os
import pyqtgraph as pg
import numpy as np
import librosa
from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from multiprocessing import Process
from utilites import *
from mplwidget import MplWidget
from pydub import playback
from pydub.playback import play
    
class UI_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Filepaths.MAIN_WINDOW(), self)
        self.setWindowTitle('Tune-it')
        # self.setFixedSize(1200, 700)
        
        "initializing necessary objects"
        self.audio_file_path = None
        self.audio_file_selected = ValueProperty(False)

        """Loading necessary objects from the loaded ui."""
        self.play_pause_btn_org = self.findChild(QPushButton, "play_pause_btn_org")
        self.play_pause_btn_edt = self.findChild(QPushButton, "play_pause_btn_edt")
        self.audio_equalizer = AudioEqualizer()

        """Some event handlers needed for different operations."""
        self.action_save_as.setEnabled(False)
        self.action_save.setEnabled(False)
        
        self.action_open.triggered.connect(self.open_file)
        self.action_save_as.triggered.connect(self.save_new_file)
        
        self.audio_file_selected.valueChanged.connect(self.load_audio)
        self.play_pause_btn_org.clicked.connect(self.play_pause_audio)
        
        self.process = None
        
    
    def closeEvent(self, event):
        # print("Closing the application.")
        # self.audio_equalizer.stop_audio()
        self.stop_audio()
        event.accept()

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
        
        if audio_file_path:
            self.audio_file_path = audio_file_path
            self.audio_file_selected.value = True
            self.enable_all()
        
        
    def enable_all(self):
        self.action_save_as.setEnabled(True)
        self.action_save.setEnabled(True)

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
            self.audio_equalizer.save_audio(file_path)

    def save_file(self):
        """
        Clicking 'Save' or pressing Ctrl+S. \n
        Save the file, when the save-file already exists/created,
        :return:
        """
        if self.save_file_path:
            self.audio_equalizer.save_audio(self.save_file_path)
        else:  # If the save-file is not created, call save_new_file()
            self.save_new_file()

    def load_audio(self):
        if self.audio_file_selected.value:
            self.audio_file_selected.value = False
            try:
                self.audio_equalizer.load(self.audio_file_path)
                self.play_audio()
                y,sr=self.plot_input()
                self.play_pause_btn_edt.clicked.connect=self.plot_output(y,sr)
            except Exception as e:
                print(e)
                self.audio_file_selected.value = False
    def play_pause_audio(self):
        if self.audio_equalizer.is_playing:
            self.pause_audio()
        else:
            self.play_audio()

    
    def plot_input(self):
        try:
            y, sr = librosa.load(self.audio_file_path)
            self.plotInputAmplitude(y, sr)
            self.plotInputSpectrogram(y, sr)
            return y,sr
        except Exception as e:
            print(e)
    def plot_output(self,y,sr):
        try:
            self.plotOutputAmplitude(y, sr)
            self.plotOutputSpectrogram(y, sr)
        except Exception as e:
            print(e)
            
    def stop_audio(self):
        self.process.terminate()
        self.audio_equalizer.is_playing = False
        self.audio_equalizer.elapsed_time = 0
        
    def play_audio(self):
        self.audio_equalizer.start_time = time.time()
        self.audio_equalizer.seek(self.audio_equalizer.elapsed_time)
        self.process = Process(target=play, args=(self.audio_equalizer.audio,))
        self.process.start()
        self.audio_equalizer.is_playing = True
    
    def pause_audio(self):
        self.audio_equalizer.current_time = time.time()
        self.audio_equalizer.elapsed_time += (self.audio_equalizer.current_time - self.audio_equalizer.start_time)
        self.process.terminate()
        self.audio_equalizer.is_playing = False

    def plotInputAmplitude(self, y, sr):
        self.InputAudioAmplitude.clear()
        
        peak_value = np.max(np.abs(y))
        normalized_data = y / peak_value
        sampling_rate = sr
        length = normalized_data.shape[0]
        time = np.linspace(0, length / sampling_rate, num=length)
        self.InputAudioAmplitude.plot(time, normalized_data, pen='b')

        self.InputAudioAmplitude.setLabel(axis='left', text='Amplitude',)
        self.InputAudioAmplitude.setLabel(axis='bottom', text='Time (s)',) 
        self.InputAudioAmplitude.getPlotItem().getViewBox().setYRange(1.0, -1.0)
        self.InputAudioAmplitude.getPlotItem().getViewBox().setContentsMargins(0.1, 0.5, 0.1, 0.1)


    def plotOutputAmplitude(self, y, sr):
        self.OutputAudioAmplitude.clear()

        peak_value = np.max(np.abs(y))
        normalized_data = y / peak_value
        sampling_rate = sr
        length = normalized_data.shape[0]
        time = np.linspace(0, length / sampling_rate, num=length)
        self.OutputAudioAmplitude.plot(time, normalized_data, pen='b')

        self.OutputAudioAmplitude.setLabel(axis='left', text='Amplitude')
        self.OutputAudioAmplitude.setLabel(axis='bottom', text='Time (s)') 
        self.OutputAudioAmplitude.getPlotItem().getViewBox().setYRange(1.0, -1.0)
        self.OutputAudioAmplitude.getPlotItem().getViewBox().setContentsMargins(0.1, 0.1, 0.1, 0.1)

    def plotInputSpectrogram(self, y, sr):
        self.InputAudioSpectrogram.canvas.axes.clear()

        # Computes FFT and plots the spectrogram
        Pxx, freqs, bins, im = self.InputAudioSpectrogram.canvas.axes.specgram(y,NFFT=1024, Fs=sr,noverlap=900)

        self.InputAudioSpectrogram.canvas.axes.set_xlabel('Time [s]')
        self.InputAudioSpectrogram.canvas.axes.set_ylabel('Frequency [Hz]')

        plt.colorbar(im, ax=self.InputAudioSpectrogram.canvas.axes)
        plt.tight_layout()

        self.InputAudioSpectrogram.canvas.draw()

    def plotOutputSpectrogram(self, y, sr):
        self.OutputAudioSpectrogram.canvas.axes.clear()

        # Computes FFT and plots the spectrogram
        Pxx, freqs, bins, im = self.OutputAudioSpectrogram.canvas.axes.specgram(y,NFFT=1024, Fs=sr,noverlap=900)

        self.OutputAudioSpectrogram.canvas.axes.set_xlabel('Time [s]')
        self.OutputAudioSpectrogram.canvas.axes.set_ylabel('Frequency [Hz]')

        plt.colorbar(im, ax=self.OutputAudioSpectrogram.canvas.axes)
        plt.tight_layout()

        self.OutputAudioSpectrogram.canvas.draw()