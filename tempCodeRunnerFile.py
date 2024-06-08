import cmath
from pydub import AudioSegment
import numpy as np
import time
from pydub import playback
from pydub.utils import mediainfo
from multiprocessing import Process, freeze_support
from copy import deepcopy
from pydub.playback import _play_with_simpleaudio, play
from scipy.signal import butter, lfilter
from scipy.fft import fft, ifft, irfft, rfft
# from numpy import hamming

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
    
    def seek(self, time, volume=0):
        if self.audio is None:
            raise Exception("Could not seek audio. Audio file not loaded.")
        
        sample_width = self.audio.sample_width
        channels = self.audio.channels
        sample_rate = int(self.audio_metadata["sample_rate"])
        
        print(f"Sample width: {sample_width}, Channels: {channels}, Sample rate: {sample_rate}")

        # Calculate the exact position in samples
        from_sample = int(round(time * sample_rate * channels))
        print(f"Calculated from_sample before alignment: {from_sample}")

        # Make sure from_sample is a multiple of (sample_rate * channels)
        remainder = from_sample % (sample_rate * channels)
        print(f"Remainder: {remainder}")
        from_sample -= remainder
        print(f"Aligned from_sample: {from_sample}")
        
        # Check if from_sample is within the valid range
        total_samples = len(self.audio_array)
        print(f"Total samples in audio: {total_samples}")

        if from_sample >= total_samples:
            raise ValueError("Seek time is beyond the length of the audio.")

        # Debugging the slicing process
        print(f"Length of audio array before slicing: {len(self.audio_array)}")
        sliced_audio_array = self.audio_array[from_sample:]
        print(f"Length of audio array after slicing: {len(sliced_audio_array)}")

        # Update the audio array and other attributes
        self.audio = self.numpy_to_audio(sliced_audio_array, sample_rate, sample_width, channels)
        print("Audio has been successfully seeked and updated.")


            
        
    def apply_gain(self, factors):

        N = len(self.audio_array)
        fs = int(self.audio_metadata["sample_rate"])

        # getting fft of the signal and subtracting amplitudes and phases
        rfft_coeff = rfft(self.audio_array)
        signal_rfft_Coeff_abs = np.abs(rfft_coeff)
        signal_rfft_Coeff_angle = np.angle(rfft_coeff)

        # getting frequencies in range 0 to fmax to access each coeff of rfft coefficients
        frequencies = np.fft.rfftfreq(N, 1 / fs)
        # plt.plot(frequencies, signal_rfft_Coeff_abs)
        # plt.show()
        
        # The maximum frequency is half the sample rate
        points_per_freq = len(frequencies) / (fs / 2)
        
        for idx in range(len(factors)):
            low = (fs / 2)/len(factors) * idx
            # print("low: ",low)
            high = (((fs / 2)/len(factors)) * (idx + 1)) - 1
            # print("high: ",high)

            # filter that multiply frequency band (from low to high) by factor
            for f in frequencies:
                if low < f < high:
                    f_idx = int(points_per_freq * f)
                    signal_rfft_Coeff_abs[f_idx] = signal_rfft_Coeff_abs[f_idx] * factors[idx]
                else:
                    pass

        # plt.plot(frequencies, signal_rfft_Coeff_abs)    
        # plt.show()
        # constructing fft coefficients again (from amplitudes and phases) after processing the amplitudes
        new_rfft_coeff = np.zeros((len(frequencies),), dtype=complex)
        for f in frequencies:
            try:
                f_idx = int(points_per_freq * f)
                new_rfft_coeff[f_idx]= signal_rfft_Coeff_abs[f_idx]*cmath.exp(1j * signal_rfft_Coeff_angle[f_idx])
            except:
                pass

        # constructing the new signal from the fft coeffs by inverse fft
        modified_array = irfft(new_rfft_coeff).astype(np.int16)
        modified_array = np.clip(modified_array, -32768, 32767)
        sample_width = self.audio.sample_width
        channels = self.audio.channels
        sample_rate = int(self.audio_metadata["sample_rate"])

        self.audio = self.numpy_to_audio(modified_array, sample_rate, sample_width, channels)

        self.audio_array = deepcopy(modified_array)

        return modified_array, fs

    def set_gain(self, band_sliders):
        factors = []
        for i in range(len(band_sliders)):
            factors.append(band_sliders[i].value())
        
        print(factors)
        self.apply_gain(factors)

    # def get_audio_segment(self):
    #     return AudioSegment(
    #         self.audio_array.tobytes(), 
    #         frame_rate=self.audio.frame_rate,
    #         sample_width=self.audio.sample_width, 
    #         channels=self.audio.channels
    #     )
        

        
# if __name__ == "__main__":
#     a = AudioEqualizer()
#     a.load("input_audio.mp3")
#     p = Process(target=play, args=(a.audio,))
#     p.start()
#     time.sleep(5)
#     p.terminate()

if __name__ == "__main__":
    a = AudioEqualizer()
    a.load("input_audio.mp3")
    a.seek(15)
    # a.audio -= 50
    p = Process(target=play, args=(a.audio,))
    p.start()
    time.sleep(20)
    p.terminate()