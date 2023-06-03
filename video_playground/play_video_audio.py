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

class player:
	def __init__(self, video_info, audio_info, volume, speed):
		self.video_info = video_info
		self.audio_info = audio_info
		self.video_parts = video_info['num_parts']
		self.audio_parts = audio_info['num_parts']
		self.fps = video_info['fps']
		self.length = video_info['length']
		self.title = video_info['title']
		self.volume = volume
		self.speed = speed
		self.current_playtime = 0
		self.chosen_playtime = 0
		self.seek_bar = 0
		self.value_label = None
		
		all_frames = []
		"""
		for n in range(1, 21):
			path = f'C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/video_playground/output/part{n}.mp4'
			print(path)
			all_frames = create_frame_lists(path, all_frames)
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

		#cv2.destroyAllWindows()
	def play_audio(self):
		#https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.get_endevent
		pass
	def seek_bar_gui(self):
		window = tk.Tk()
		window.title(self.title)

		# Create a seek bar widget
		self.seek_bar = tk.Scale(window, from_=0, to=self.lengt, orient=tk.HORIZONTAL, command=self.update_value)
		self.seek_bar.pack()

		# Create a label to display the current value of the seek bar
		self.value_label = tk.Label(window, text="Value: " + str(self.seek_bar.get()))
		self.value_label.pack()

		# Start the Tkinter event loop
		window.mainloop()
	def update_value(self, value):
		self.value_label.config(text="Value: " + str(self.seek_bar.get()))
video_info = {
	'title': 'test',
	'fps' : 24,
	'num_parts' : 20,
	'length' : 193,
}
player(0,0,0,0).seek_bar_gui()