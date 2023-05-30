import cv2
import pyaudio
import wave
import threading
import time
import sys

flag = True

# Buffer size in bytes
buffer_size = 1024 * 1024  # 1 MB

# Create a buffer to store the video data
buffer = bytearray()

audio_file = "audio.wav"
video_file = "video.mp4"

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

# Function to fill the buffer with video data
def fill_buffer():
	with open(video_file, "rb") as file:
		while True:
			chunk = file.read(buffer_size)
			if not chunk:
				break
			buffer.extend(chunk)

paths = []
for n in range(1, 21):
	paths.append(f'C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/video_playground/output/part{n}.mp4')

def play_video(path):
	global flag
	is_playing = True
	n = 0
	while True:
		if len(paths) <= n:
			print('break')
			break
		cap = cv2.VideoCapture(paths[n])
		
		while True:
			start = time.time()
			fps = cap.get(cv2.CAP_PROP_FPS)

			ret, frame = cap.read()
			
			if ret:
				cv2.imshow('Video', frame)
				
			# Check for keyboard events and quit if 'q' is pressed
			if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
				break

			elapsed_time = time.time() - start
			video_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps

			# Wait until the current video is fully played
			if elapsed_time < video_duration:
				if cv2.waitKey(1) & 0xFF == ord('q'):
					is_playing = False
					break
				else:
					continue
			# Check if the video playback was interrupted
			
			
			if not is_playing:
				break

			n = n + 1


fill_buffer()

thread1 = threading.Thread(target=play_audio, args=[audio_file])
thread2 = threading.Thread(target=play_video, args=[video_file])
thread1.start()
thread2.start()
thread1.join()
thread2.join()