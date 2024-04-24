from pygame import mixer, sndarray, time
import os
import numpy as np

# Starting the mixer 
mixer.init() 

# Loading the song 
mixer.music.load("H:/UNI_STUFF/6th Sem/DSP Lab/Project/Tune-it/input_audio.mp3") 

# Setting the volume 
mixer.music.set_volume(0.7) 

# Start playing the song
mixer.music.play() 


# Get the audio data as a numpy array
sound = mixer.Sound("H:/UNI_STUFF/6th Sem/DSP Lab/Project/Tune-it/input_audio.mp3")
array = sndarray.array(sound)

# Print the numpy array
# Get the duration of the audio in seconds
duration = sound.get_length()

# Get the number of samples
num_samples = len(sound.get_raw())

# Calculate the frequency
frequency = num_samples / duration

# Print the frequency
print("Frequency:", frequency, "Hz")

# infinite loop 
while True: 
	
	print("Press 'p' to pause, 'r' to resume") 
	print("Press 'e' to exit the program") 
	query = input(" ") 
	
	if query == 'p': 

		# Pausing the music 
		mixer.music.pause()	 
	elif query == 'r': 

		# Resuming the music 
		mixer.music.unpause() 
	elif query == 'e': 

		# Stop the mixer 
		mixer.music.stop() 
		break

from scipy.io.wavfile import write

# Function to convert a numpy array to a WAV file
def numpy_array_to_wav(array, filename, sample_rate):
    # Normalize the array to the range [-32768, 32767] for 16-bit PCM audio
    normalized_array = np.int16(array * 32767)
    # Write the array to a WAV file
    write(filename, sample_rate, array)


# Sample rate and duration for the audio
sample_rate = int(np.ceil(frequency / 10))  # Hz

audio_data = array

# Convert the numpy array to a WAV file
numpy_array_to_wav(audio_data, 'output.wav', sample_rate)

# Load the WAV file using Pygame
mixer.init()
mixer.music.load('output.wav')

# Play the loaded WAV file
mixer.music.play()

# infinite loop 
while True: 
	print("Press 'p' to pause, 'r' to resume") 
	print("Press 'e' to exit the program") 
	query = input(" ") 
	
	if query == 'p': 

		# Pausing the music 
		mixer.music.pause()	 
	elif query == 'r': 

		# Resuming the music 
		mixer.music.unpause() 
	elif query == 'e': 

		# Stop the mixer 
		mixer.music.stop() 
		break

