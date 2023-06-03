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

# Buffer size in bytes
buffer_size = 1024 * 1024  # 1 MB

# Create a buffer to store the video data
buffer = bytearray()

audio_file = "audio.wav"
video_file = "video.mp4"

flag = False
def play_audio(fname):
	wf = wave.open(fname, "rb")
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(), output=True)
	chunk = 1024
	data = wf.readframes(chunk)

	#flagがFalseになるとループを抜ける
	while data != '' and flag:
		#ここで再生している
		stream.write(data)
		data = wf.readframes(chunk)

	stream.stop_stream()
	stream.close()
	p.terminate()

def playback_audio(audio_path):
	audio = AudioSegment.from_file(audio_path)
	interval = 1000
	duration = len(audio)

	current_time = 0#control
	while current_time < duration:
		segment = audio[current_time:current_time+interval]
		play(segment)
		current_time += interval

def on_trackbar_move(position, cap):
	cap.set(cv2.CAP_PROP_POS_FRAMES, position)
			
def create_frame_lists(video_path, all_frames):
	interval = 1
	cap = cv2.VideoCapture(video_path)
	frame_rate = cap.get(cv2.CAP_PROP_FPS)
	frame_count = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	duration = frame_count / frame_rate
	save_interval = round(frame_rate * interval)

	current_frame = 0
	while current_frame < frame_count:
		frames = []
		for _ in range(save_interval):
			ret, frame = cap.read()
			if not ret:
				break
		
			frames.append(frame)
			current_frame += 1
		if frames:
			all_frames.append(np.array(frames))

	cap.release()
	return all_frames

def play_video(frame_lists):
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

	cv2.destroyAllWindows()
	
		
if __name__ == '__main__':
	all_frames = []
	for n in range(1, 21):
		path = f'C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/video_playground/output/part{n}.mp4'
		print(path)
		all_frames = create_frame_lists(path, all_frames)
	print(len(all_frames))
	for f in all_frames:
		print(len(f))
	#thread1 = threading.Thread(target=play_audio, args=[audio_file])
	thread2 = threading.Thread(target=play_video, args=[all_frames])
	#thread1.start()
	thread2.start()
	#thread1.join()
	thread2.join()
"""
	thread1 = threading.Thread(target=play_audio, args=[audio_file])
	thread2 = threading.Thread(target=play_video, args=[])
	arrange_data_thread = threading.Thread(target=arrange_frames)
	thread1.start()
	thread2.start()
	arrange_data_thread.start()
	thread1.join()
	thread2.join()
	arrange_data_thread.join()
"""