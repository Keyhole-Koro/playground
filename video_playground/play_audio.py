import pygame

from pydub import AudioSegment
import os
import math

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

def playback_audio(audio_path):
	audio = AudioSegment.from_file(audio_path)

	chunk_size = 1000  # Chunk size in milliseconds
	duration = len(audio)

	def play_audio():
		current_time = 0
		while current_time < duration:
			chunk = audio[current_time:current_time+chunk_size]
			q.put(chunk)
			current_time += chunk_size

		q.put(None)  # Signal the end of audio playback

	def play_chunks():
		while True:
			chunk = q.get()
			if chunk is None:
				break
			play(chunk)

	q = queue.Queue()
	play_thread = threading.Thread(target=play_audio)
	chunks_thread = threading.Thread(target=play_chunks)

	play_thread.start()
	chunks_thread.start()

	play_thread.join()
	chunks_thread.join()
	
play_split_audios()


# Usage example
audio_file = "audio.wav"
output_folder = "audio_segments"
segment_duration = 10000  # Duration of each segment in milliseconds
extension = audio_file.split('.')[-1]

#split_audio(audio_file, output_folder, segment_duration, extension)
