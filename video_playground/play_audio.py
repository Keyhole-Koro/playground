import pygame
import threading
from pydub import AudioSegment
import os
import math
import time

pygame.init()


def audio_playground(audio_path):
	py_music = pygame.mixer.music
	py_music.load(audio_file)
	start_time = 10
	py_music.play()
	py_music.set_pos(start_time)
	py_music.set_volume(1)
	pygame.time.wait(5000)
	py_music.set_pos(start_time)
	py_music.set_volume(0.5)
	pygame.time.wait(5000)
	#py_music.get_busy()->bool
	py_music.pause()
	pygame.time.wait(5000)
	py_music.unpause()
	pygame.time.wait(5000)
	pygame.quit()

def play_split_audios():
	py_music = pygame.mixer.music
	for n in range(1, 21):
		path = f'C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/video_playground/audio_segments/segment_{n}.wav'
		py_music.load(path)
		py_music.play()
		pygame.time.wait(10000)

def playback_audio():
	pygame.init()
	# List of audio files (3-second duration each)
	audio_files = ["C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/video_playground/output_segments/segment_1.wav", "C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/video_playground/output_segments/segment_2.wav", "C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/video_playground/output_segments/segment_3.wav"]

	# Iterate over each audio file
	for audio_file in audio_files:

		pygame.mixer.music.load(audio_file)

		pygame.mixer.music.play()

		start_time = time.time()

		while pygame.mixer.music.get_busy():
			current_time = time.time()
			

		pygame.mixer.music.stop()

	pygame.quit()
# Usage example
audio_file = "audio.wav"
output_folder = "audio_segments"
segment_duration = 10000  # Duration of each segment in milliseconds
extension = audio_file.split('.')[-1]
playback_audio()
#split_audio(audio_file, output_folder, segment_duration, extension)
