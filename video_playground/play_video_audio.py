import cv2
import pyaudio
import wave
import threading
import time
import sys
import asyncio
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import queue
import pygame
import tkinter as tk
import math

class player:
	def __init__(self, video_info, audio_info, volume, speed):
		self.video_info = video_info
		self.audio_info = audio_info
		self.video_parts = video_info['num_parts']
		self.audio_parts = audio_info['num_parts']
		self.fps = round(video_info['fps'])
		self.video_length = video_info['length']
		self.audio_length = audio_info['length']
		self.part_video_length = video_info['part_length']
		self.part_audio_length = audio_info['part_length']
		self.title = video_info['title']
		self.volume = volume
		self.speed = speed
		self.current_playtime = 0
		self.chosen_playtime = 0
		self.seek_bar = 0
		self.value_label = None
		self.audio_file_position = 0
		self.audio_start_position = 0
		self.video_file_position = 0
		self.video_start_position = 0
		
		self.is_being_changed = False
		
		self.playing_video = None
		self.playing_audio = None
		self.seek_bar_thread = None
		
		self.commander = False
		
		all_frames = []
		self.playing_audio = threading.Thread(target=self.play_audio)
		self.playing_video = threading.Thread(target=self.play_video)
		self.seek_bar_thread = threading.Thread(target=self.seek_bar_gui)
		self.playing_audio.start()
		self.playing_video.start()
		self.seek_bar_thread.start()
		
		self.commander = True
		

	"""
	def play_video(self, frame_lists):
		global flag
		fps = 24
		delay = 1/fps
		flag = True
		start = time.time()
		for f, frames in enumerate(frame_lists):
			for c, frame in enumerate(frames):
				while True:
					elapsed_time = time.time() - start
					if elapsed_time > (f + delay*(c+1)):
						key = cv2.waitKey(1)
						cv2.imshow('Video', frame)
						break
					if self.current_playtime != self.chosen_playtime and self.is_being_changed:
						break
		#cv2.destroyAllWindows()
	"""

	def play_video(self):
		video_paths = []
		for i in range(1, 21):
			video_paths.append(f"C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/video_playground/output/part{i}.mp4")
		delay = 1/self.fps
		ret = False
		while True:
			cap = cv2.VideoCapture(video_paths[self.video_file_position])
			self.video_file_position += 1
			cap.set(cv2.CAP_PROP_POS_FRAMES, self.video_start_position*self.fps)
			part_start = time.time()
			
			while not self.commander:
				pass
			
			while True:
				elapsed_time = time.time() - part_start
				current_play_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
				#print(elapsed_time, cap.get(cv2.CAP_PROP_POS_MSEC), cap.isOpened())
				if elapsed_time > (current_play_time / 1000):
					key = cv2.waitKey(1)
					ret, frame = cap.read()
					
					if ret:
						cv2.imshow('Video', frame)
					else:
						break

				key = cv2.waitKey(1)
				if key == ord('q'):
					break
				
				if self.current_playtime != self.chosen_playtime and self.is_being_changed:
					print('changed')
					self.video_file_position, self.video_start_position = self.separate(self.chosen_playtime, self.part_audio_length)
					self.commander = True
					break
		
	def play_audio(self):
		print('play_audio')
		pygame.init()
		# List of audio files (3-second duration each)
		audio_paths = []
		for i in range(1, 21):
			audio_paths.append(f"C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/video_playground/audio_segments/segment_{i}.wav")
		
		while True:

			while not self.commander:
				pass
			
			if self.audio_file_position <= self.audio_parts:
				audio_file = audio_paths[self.audio_file_position]
				pygame.mixer.music.load(audio_file)
				pygame.mixer.music.play()
				self.audio_file_position += 1
				pygame.mixer.music.set_pos(self.audio_start_position)
				self.audio_start_position = 0

			
			while pygame.mixer.music.get_busy():
				if self.current_playtime != self.chosen_playtime and self.is_being_changed:
					self.current_playtime = self.chosen_playtime
					self.audio_file_position, self.audio_start_position = self.separate(self.chosen_playtime, self.part_audio_length)
					pygame.mixer.music.stop()
					self.is_being_changed = False
					break

			#if self.audio_file_position == self.audio_parts and not pygame.mixer.music.get_busy():
			#	while self.current_playtime == self.chosen_playtime and self.is_being_changed:
			#		pass
			self.commander = True
			pygame.mixer.music.stop()

		pygame.quit()
			#https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.get_endevent
	def separate(self, chosen_playtime, part_length):
		file_position = chosen_playtime // part_length
		start_position = chosen_playtime % part_length
		positions = [file_position, start_position]
		return positions
		
	def seek_bar_gui(self):
		window = tk.Tk()
		window.title(self.title)

		self.seek_bar = tk.Scale(window, from_=0, to=self.video_length, orient=tk.HORIZONTAL, command=self.update_value)
		self.seek_bar.bind("<ButtonRelease-1>", self.on_seek_bar_release)
		self.seek_bar.pack()

		self.value_label = tk.Label(window, text="Value: " + str(self.seek_bar.get()))
		self.value_label.pack()

		window.mainloop()
	def update_value(self, value):
		self.value_label.config(text="Value: " + str(self.seek_bar.get()))

	def on_seek_bar_release(self, event):
		self.chosen_playtime = self.seek_bar.get()
		self.is_being_changed = True
		print("Seek bar value on release:", self.chosen_playtime)
		self.commander = True
		self.commander = False

video_info = {
	'title': 'test',
	'fps' : 24,
	'num_parts' : 20,
	'length' : 193,
	'part_length' : 10
}
audio_info = {
	'title': 'test',
	'fps' : 24,
	'num_parts' : 20,
	'length' : 193,
	'part_length' : 10
}
p = player(video_info, audio_info,0,0)
#p.seek_bar_gui()
#p.play_audio()