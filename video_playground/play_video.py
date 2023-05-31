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
	is_playing = True
	n = 0
	beginnig = time.time()
	l_entire_frame = []
	l_indi_frame = []
	l_entire_frame.append(l_indi_frame)
	fps = 0  # Variable to store the frames per second
	
	while True:
		if len(paths) <= n:
			print('break')
			break

		print('changed video')
		cap = cv2.VideoCapture(paths[n])
		fps = cap.get(cv2.CAP_PROP_FPS)
		print(n, fps)
		frame_duration = 1 / fps
		start = time.time()
		elapsed_time = 0.0
		once_sec_start = time.time()
		while True:
			ret, frame = cap.read()

			if ret:
				cv2.imshow('Video', frame)

			# Check for keyboard events and quit if 'q' is pressed
			if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
				break

			# Add the frame to the current second's list
			l_indi_frame.append(frame)
			#print('l_indi_frame',len(l_indi_frame))
			
			#one_sec = time.time() - once_sec_start
			one_sec = len(l_indi_frame) * frame_duration
			# Update the elapsed time
			elapsed_time = time.time() - start

			# If one second has passed, store the frames and reset the list
			if one_sec >= 1.0:
				l_entire_frame.append(l_indi_frame)
				del l_indi_frame
				l_indi_frame = []
				once_sec_start = time.time()  # Reset the start time
				print(len(l_entire_frame))

			# Check if the video playback was interrupted
			if elapsed_time >= cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps:
				n += 1
				print(len(l_entire_frame))
				break

		if not is_playing:
			break
		print(time.time()-beginnig)
			

"""
def play_video(path):
	cap = cv2.VideoCapture(path)
	fps = cap.get(cv2.CAP_PROP_FPS)
	total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			break

		cv2.imshow('Video', frame)
		if cv2.waitKey(30) & 0xFF == ord('q'):
			break

		current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
		elapsed_time = current_frame / fps
		print('Elapsed Time:', elapsed_time, 's')

		if current_frame >= total_frames:
			break

	cap.release()
	cv2.destroyAllWindows()"""
fill_buffer()

thread1 = threading.Thread(target=play_audio, args=[audio_file])
thread2 = threading.Thread(target=play_video, args=[video_file])
thread1.start()
thread2.start()
thread1.join()
thread2.join()