from pydub import AudioSegment
import numpy as np

# import widgets

class audio_equalizer:
    def __init__(self):

        self.audio_file_path = "D:/Songs/Justin-Bieber-Ghost.mp3"
        self.channels = None
        self.frame_rate = None
        self.sample_width = None

    def audio_to_numpy(self):
        # Load the audio file
        audio = AudioSegment.from_file(self.audio_file_path, format="mp3")
        
        self.channels = audio.channels
        self.frame_rate = audio.frame_rate
        self.sample_width = audio.sample_width

        # Convert audio to raw PCM data (16-bit signed integers)
        raw_audio_data = audio.raw_data

        # Convert raw audio data to NumPy array
        self.audio_array = np.frombuffer(raw_audio_data, dtype=np.int16)

        print("Shape of audio array:", self.audio_array.shape)
   

    def numpy_to_audio(self):
        # Create an AudioSegment object from the audio array
        audio = AudioSegment(self.audio_array.tobytes(), self.frame_rate, self.sample_width, self.channels)

        # Export the audio to a file
        audio.export("output_audio.mp3", format="mp3")

    
a = audio_equalizer()
a.audio_to_numpy()
a.numpy_to_audio()