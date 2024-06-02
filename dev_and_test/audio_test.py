from pydub import AudioSegment
from pydub.playback import play
import threading
import time
from pydub import playback
from multiprocessing import Process, freeze_support
import numpy as np

# class AudioPlayer:
#     def __init__(self, filename):
#         self.audio = AudioSegment.from_file(filename)
#         self.playing = False
#         self.paused = False

#     def play(self):
#         if not self.playing:
#             self.playing = True
#             self.paused = False
#             self.thread = threading.Thread(target=self._play_audio)
#             self.thread.start()

#     def pause(self):
#         self.paused = True

#     def resume(self):
#         self.paused = False

#     def _play_audio(self):
#         start_time = time.time()
#         while self.playing:
#             if not self.paused:
#                 # Calculate elapsed time
#                 elapsed_time = time.time() - start_time
#                 # Play the audio from the current position
#                 play(self.audio[self.audio.duration_seconds * (elapsed_time / self.audio.duration_seconds):])
#                 # Wait for a short duration before checking again

# # Example usage
# filename = "input_audio.mp3"
# player = AudioPlayer(filename)

# # Start playback
# player.play()

# # Wait for 2 seconds
# time.sleep(2)


# # Pause playback
# player.pause()
# print("lol")

# # Wait for 2 seconds
# time.sleep(2)

# # Resume playback
# player.resume()

# # Wait for the audio to finish playing
# time.sleep(player.audio.duration_seconds)

# # Stop playback
# player.playing = False

filename = "input_audio.mp3"
audio = AudioSegment.from_file(filename)

# Convert audio to numpy array
audio_array = np.array(audio.get_array_of_samples())

# Convert numpy array back to pydub audio
audio_from_array = AudioSegment(audio_array.tobytes(), frame_rate=audio.frame_rate, sample_width=audio.sample_width, channels=audio.channels)

# Play the audio from the numpy array
# play(audio_from_array)

# Print the shape of the audio array
# print("Shape of audio array:", audio_array.shape)

process = Process(target=play, args=(audio,))
if __name__ == "__main__":
    freeze_support()
    process.start()
    time.sleep(5)
    process.terminate()

