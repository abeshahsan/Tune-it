from pydub import AudioSegment
import numpy as np
import time
from pydub import playback
from pydub.utils import mediainfo
from multiprocessing import Process, freeze_support
from copy import deepcopy
from pydub.playback import _play_with_simpleaudio, play
from scipy.signal import butter, lfilter

class AudioEqualizer:
    def __init__(self):
        
        self.is_playing = False
        self.full_audio_array = None
        self.audio_file_path = None
        self.audio_array = None
        self.audio = None
        self.process = None
        self.start_time = None
        self.current_time = None
        self.elapsed_time = 0
        self.playing_audio = None
        self.gains = [0] * 8  # Initialize gains for 8 bands
        
        freeze_support()
    
    
    def load(self, audio_file_path):
        if not audio_file_path:
            raise Exception("Audio file path is empty.")
        self.audio = AudioSegment.from_file(audio_file_path, format="mp3")
        self.audio_metadata = mediainfo(audio_file_path)
        self.audio_array = np.frombuffer(self.audio.raw_data, dtype=np.int16)
        self.full_audio_array = deepcopy(self.audio_array)
        self.audio_array = self.audio_to_numpy(self.audio)


    def audio_to_numpy(self, audio):
        if audio is None:
            raise Exception("self.audio is None. Audio file not loaded.")
        return np.frombuffer(self.audio.raw_data, dtype=np.int16)
            

    def numpy_to_audio(self, audio_array, frame_rate, sample_width, channels):
        if audio_array is None:
            raise Exception("Could not convert to audio .self.audio_array is None.")
        
        self.audio = AudioSegment(audio_array.tobytes(), 
                             frame_rate = frame_rate, 
                             sample_width = sample_width, 
                             channels = channels)
        
        return self.audio
        
    def save_audio(self, file_name=None):
        if self.audio is None:
            raise Exception("Could not save audio. self.audio is None.")
        if file_name is None: 
            file_name = f"tune-it--{self.audio_file_path}"
        self.audio.export(file_name, format="mp3")
    
    # def play_audio(self):
    #     if self.audio is None:
    #         raise Exception("Could not play audio. self.audio is None.")
        
    #     self.seek(self.elapsed_time) #to resume from where it was paused
    #     self.playing_audio = _play_with_simpleaudio(self.audio)
    #     self.start_time = time.time()
        
    # def stop_audio(self):
    #     self.playing_audio.stop()
    
    # def pause_audio(self):
    #     try:
    #         self.playing_audio.stop()
    #         self.current_time = time.time()
    #         self.elapsed_time += (self.current_time - self.start_time)
    #         # print(f"Audio paused at {self.elapsed_time} seconds.")
    #     except Exception as e:
    #         print(e)
            
    def change_volume(self, gain=-2):
        if self.audio is None:
            raise Exception("Could not change volume. Audio file not loaded.")    
        self.audio += gain
    
    def seek(self, time):
        if self.audio is None:
            raise Exception("Could not seek audio. Audio file not loaded.")
        
        total_samples = len(self.audio_array)
        sample_width = self.audio.sample_width
        channels = self.audio.channels
        sample_rate = int(self.audio_metadata["sample_rate"])

        # Calculate the exact position in samples
        from_sample = int(time * sample_rate * sample_width)

        # Make sure from_sample is a multiple of (sample_width * channels)
        remainder = (total_samples - from_sample) % (sample_width * channels)
        
        self.audio = self.numpy_to_audio(np.pad(self.audio_array[from_sample:], (0, remainder), mode='constant'),
                                         sample_rate, sample_width, channels)
        


    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def apply_gain(self, band, gain):
        fs = self.audio.frame_rate
        band_filters = [
            (20, 60), (60, 170), (170, 310), (310, 600), 
            (600, 1000), (1000, 3000), (3000, 6000), (6000, 20000)
        ]
        low, high = band_filters[band]
        b, a = self.butter_bandpass(low, high, fs)
        filtered = lfilter(b, a, self.audio_array).astype(np.int16)
        self.audio_array = deepcopy(self.full_audio_array)
        self.audio_array += gain * filtered

        sample_width = self.audio.sample_width
        channels = self.audio.channels
        sample_rate = int(self.audio_metadata["sample_rate"])
        
        self.audio = self.numpy_to_audio(self.audio_array,
                                         sample_rate, sample_width, channels)
  

    def set_gain(self, band, gain):
        self.gains[band] = gain
        self.apply_gain(band, gain)

    # def get_audio_segment(self):
    #     return AudioSegment(
    #         self.audio_array.tobytes(), 
    #         frame_rate=self.audio.frame_rate,
    #         sample_width=self.audio.sample_width, 
    #         channels=self.audio.channels
    #     )


        
if __name__ == "__main__":
    a = AudioEqualizer()
    a.load("input_audio.mp3")
    p = Process(target=play, args=(a.audio,))
    p.start()
    time.sleep(5)
    p.terminate()