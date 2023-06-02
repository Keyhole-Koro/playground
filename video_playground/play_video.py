import cv2
import pyaudio
import wave
import threading
import time
import sys



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


def divide(video):
	cap = cv2.VideoCapture(video)
	total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	fps = cap.get(cv2.CAP_PROP_FPS)
	beginning_time = time.time()
	segment_duration = 1
	segments = []
	position = 0
	while position < total_frames:
		cap.set(cv2.CAP_PROP_POS_FRAMES, position)
		segment_frames = []
		segment_end = position + round(segment_duration * cap.get(cv2.CAP_PROP_FPS))
		print(segment_end, len(segments), time.time()-beginning_time, position, segment_end)
		while position < segment_end:
			ret, frame = cap.read()
			
			if ret:
				segment_frames.append(frame)
				#print(len(segments))
				#print('segment_frames', len(segment_frames))
				position += 1
			else:
				break
		segments.append(segment_frames)
	cap.release()
	cv2.destroyAllWindows()
	thread1 = threading.Thread(target=play_audio, args=[audio_file])
	thread2 = threading.Thread(target=play_video, args=[segments])
	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()


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
				pass
				#cv2.imshow('Video', frame)
			
			# Check for keyboard events and quit if 'q' is pressed
			if cv2.waitKey(round(1000 / fps)) & 0xFF == ord('q'):
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
				print(len(l_entire_frame), time.time()-beginnig, len(l_entire_frame)-(time.time()-beginnig), time.time()-beginnig, one_sec)

			# Check if the video playback was interrupted
			if elapsed_time >= cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps:
				n += 1
				print(len(l_entire_frame))
				break

		if not is_playing:
			break
		print(time.time()-beginnig)
			


def play_video2(segments):
	fps = len(segments[0])
	print('fps', fps)
	adjusted_fps = fps + 1
	n_seg = 0
	changed = time.time()
	delayment = 1000/adjusted_fps
	beginning = time.time()
	while True:
		changed = time.time()
		segments[n_seg].append(segments[n_seg][-1])
		print(len(segments[n_seg]))
		print(time.time()-beginning)
		for seg in segments[n_seg]:
			cv2.imshow('Video', seg)
			if cv2.waitKey(int(delayment)) & 0xFF == ord('q'):
				break
		n_seg += 1


	cap.release()
	cv2.destroyAllWindows
	
paths = []
for n in range(1, 21):
	paths.append(f'C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/video_playground/output/part{n}.mp4')

def on_trackbar_move(position, cap):
	cap.set(cv2.CAP_PROP_POS_FRAMES, position)

def play_video():
	global flag
	window_name = "PlayVideoAudio"
	frames = []  # List to store frames
	n = 0
	flag = True

	while True:
		cap = cv2.VideoCapture(paths[n])
		start = time.time()
		fps = cap.get(cv2.CAP_PROP_FPS)

		if not cap.isOpened():
			sys.exit()

		cv2.namedWindow(window_name)
		#cv2.createTrackbar('Position', window_name, 0, 1, lambda x: on_trackbar_move(x, cap))

		while True:
			elapsed_time = (time.time() - start) * 1000
			play_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))

			if elapsed_time < play_time:
				key = cv2.waitKey(1)
				if key == 1:
					break
				else:
					continue
			else:
				print(elapsed_time, play_time)
				ret, frame = cap.read()

			if ret:
				frames.append(frame)  # Store the actual frame
				cv2.imshow(window_name, frame)
				#cv2.setTrackbarPos('Position', window_name, 0)
			else:
				n += 1
				cap = cv2.VideoCapture(paths[n])
				start = time.time()
				fps = cap.get(cv2.CAP_PROP_FPS)

	flag = False
	cap.release()
	cv2.destroyAllWindows()


thread1 = threading.Thread(target=play_audio, args=[audio_file])
thread2 = threading.Thread(target=play_video, args=[])
thread1.start()
thread2.start()
thread1.join()
thread2.join()
