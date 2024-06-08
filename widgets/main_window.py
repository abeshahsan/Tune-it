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
        uic.loadUi(Filepaths.MAIN_WINDOW_V3(), self)
        self.setWindowTitle('Tune-it')
        # self.setFixedSize(1200, 700)
        
        "initializing necessary objects"
        self.audio_file_path = None
        self.audio_file_selected = ValueProperty(False)
        

        """Loading necessary objects from the loaded ui."""
        self.play_pause_btn = self.findChild(QPushButton, "play_pause_btn")
        self.stop_btn = self.findChild(QPushButton, "stop_btn")
        self.volume_slider = self.findChild(QSlider, "volume_slider")
        self.volume = self.volume_slider.value()
        self.changed_volume = self.volume


        self.audio_equalizer = AudioEqualizer()


        """Some event handlers needed for different operations."""
        self.action_save_as.setEnabled(False)
        self.action_save.setEnabled(False)
        
        self.action_open.triggered.connect(self.open_file)
        self.action_save_as.triggered.connect(self.save_new_file)
        
        self.audio_file_selected.valueChanged.connect(self.load_audio)
        
        self.play_pause_btn.clicked.connect(self.play_pause_audio)
        self.stop_btn.clicked.connect(self.stop_audio)
        self.volume_slider.valueChanged.connect(lambda value: self.change_volume(value))

        
        self.process = None

        """Frequency sliders"""
        self.band_sliders = [
            self.findChild(QSlider, f"band_slider_{i}") for i in range(1, 9)
        ]
        

        for i, slider in enumerate(self.band_sliders):
            slider.valueChanged.connect(lambda : self.set_gain(self.band_sliders))

        
    
    def closeEvent(self, event):
        try:
            # print("Closing the application.")
            # self.audio_equalizer.stop_audio()
            self.stop_audio()
        except Exception as e:
            print(e)
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
                y, sr = librosa.load(self.audio_file_path)
                self.eq_y=y
                self.eq_sr=sr
                self.plot_input(y,sr)
                self.play_audio()
            except Exception as e:
                print(e)
                self.audio_file_selected.value = False
    def play_pause_audio(self):
        if self.audio_equalizer.is_playing:
            self.pause_audio()
        else:
            self.plot_output(self.eq_y,self.eq_sr)
            self.play_audio()
            
    def stop_audio(self):
        try:
            self.process.terminate()
            self.audio_equalizer.is_playing = False
            self.audio_equalizer.elapsed_time = 0
        except Exception as e:
            print(e)
            
        
    def play_audio(self):
        try:
            self.audio_equalizer.start_time = time.time()
            # self.audio_equalizer.seek(self.audio_equalizer.elapsed_time, self.changed_volume)
            self.process = Process(target=play, args=(self.audio_equalizer.audio,))
            self.process.start()
            self.audio_equalizer.is_playing = True
        except Exception as e:
            print(e)
    
    def pause_audio(self):
        try:
            self.audio_equalizer.current_time = time.time()
            self.audio_equalizer.elapsed_time += (self.audio_equalizer.current_time - self.audio_equalizer.start_time)
            self.process.terminate()
            self.audio_equalizer.is_playing = False
        except Exception as e:
            print(e)

    def change_volume(self, volume):
        if self.audio_equalizer.audio is None:
            raise Exception("Could not change volume. Audio file not loaded.")  
        try:
            self.pause_audio()  
            self.changed_volume = volume - self.volume
            print(self.volume, volume)
            self.volume = volume
            self.play_audio()
        except Exception as e:
            print(e)

    def plot_input(self,y,sr):
        try:
            
            self.plotInputAmplitude(y, sr)
            self.plotInputSpectrogram(y, sr)
            
        except Exception as e:
            print(e)
    def plot_output(self,y,sr):
        try:
            self.plotOutputAmplitude(y, sr)
            self.plotOutputSpectrogram(y, sr)
        except Exception as e:
            print(e)
    
    def plotInputAmplitude(self, y, sr):
        self.org_amplitude.clear()
        
        peak_value = np.max(np.abs(y))
        normalized_data = y / peak_value
        sampling_rate = sr
        length = normalized_data.shape[0]
        time = np.linspace(0, length, num=length)
        self.org_amplitude.plot(time, y, pen='b')

        self.org_amplitude.setLabel(axis='left', text='Amplitude',)
        self.org_amplitude.setLabel(axis='bottom', text='Time (s)',) 
        self.org_amplitude.getPlotItem().getViewBox().setYRange(1.0, -1.0)
        self.org_amplitude.getPlotItem().getViewBox().setContentsMargins(0.1, 0.5, 0.1, 0.1)
        print("y",y)



    def plotOutputAmplitude(self, eq_y, eq_sr):
        self.eq_amplitude.clear()

        peak_value = np.max(np.abs(eq_y))
        normalized_data = eq_y / peak_value
        sampling_rate = eq_sr
        length = normalized_data.shape[0]
        time = np.linspace(0, length, num=length)
        self.eq_amplitude.plot(time, eq_y, pen='b')

        self.eq_amplitude.setLabel(axis='left', text='Amplitude')
        self.eq_amplitude.setLabel(axis='bottom', text='Time (s)') 
        self.eq_amplitude.getPlotItem().getViewBox().setYRange(1.0, -1.0)
        self.eq_amplitude.getPlotItem().getViewBox().setContentsMargins(0.1, 0.1, 0.1, 0.1)
        print("eq_y",eq_y)

    def plotInputSpectrogram(self, y, sr):
        self.org_spectrogram.canvas.axes.clear()
        peak_value = np.max(np.abs(y))
        normalized_data = y / peak_value
        length = normalized_data.shape[0]
        nfft_log=np.floor(np.log2(length))+1
        nfft_val=int(2**nfft_log)
        # Computes FFT and plots the spectrogram
        Pxx, freqs, bins, im = self.org_spectrogram.canvas.axes.specgram(y, Fs=sr)

        self.org_spectrogram.canvas.axes.set_xlabel('Time [s]')
        self.org_spectrogram.canvas.axes.set_ylabel('Frequency [Hz]')

        plt.colorbar(im, ax=self.org_spectrogram.canvas.axes)
        plt.tight_layout()

        self.org_spectrogram.canvas.draw()

    def plotOutputSpectrogram(self, eq_y, eq_sr):
        self.eq_spectrogram.canvas.axes.clear()
        length=eq_y.shape[0]
        nfft_log=np.floor(np.log2(length))+1
        nfft_val=int(2**nfft_log)
        # Computes FFT and plots the spectrogram
        Pxx, freqs, bins, im = self.eq_spectrogram.canvas.axes.specgram(eq_y, Fs=eq_sr)

        self.eq_spectrogram.canvas.axes.set_xlabel('Time [s]')
        self.eq_spectrogram.canvas.axes.set_ylabel('Frequency [Hz]')

        plt.colorbar(im, ax=self.eq_spectrogram.canvas.axes)
        plt.tight_layout()

        self.eq_spectrogram.canvas.draw()
    def set_gain(self, band_sliders):
        self.pause_audio()
        factors = []
        for i in range(len(band_sliders)):
            factors.append(band_sliders[i].value())
        
        print(factors)
        self.audio_equalizer.apply_gain(factors)
        self.play_audio()