import cv2
import threading
from io import BytesIO
import base64
import tempfile

def play_video(video_path):
	with open(video_file, 'rb') as v:
		data = v.read()
	temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
	temp_file.write(data)
	temp_file.close()

	# Read the video file using cv2.VideoCapture
	cap = cv2.VideoCapture(temp_file.name)

	while cap.isOpened():
		ret, frame = cap.read()

		if not ret:
			break

		# Display the frame
		cv2.imshow("Video", frame)

		# Delay between frames (in milliseconds)
		delay = 30  # Adjust this value to control the playback speed

		if cv2.waitKey(delay) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()

import cv2

def divide_video(video_path, output_directory, duration):
	# Open the video file
	video = cv2.VideoCapture(video_path)

	# Check if the video file was opened successfully
	if not video.isOpened():
		print("Error opening video file")
		return

	# Create the output directory if it doesn't exist
	import os
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)

	# Initialize variables
	frame_count = 0
	success = True
	video_count = 1
	frame_rate = int(video.get(cv2.CAP_PROP_FPS))

	# Create a VideoWriter object for the first output video
	output_path = os.path.join(output_directory, f"output_{video_count}.avi")
	fourcc = cv2.VideoWriter_fourcc(*"XVID")
	writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (int(video.get(3)), int(video.get(4))))

	# Read frames from the video and save them into smaller videos
	while success:
		# Read the next frame
		success, frame = video.read()

		# Write the frame to the current output video
		if success:
			writer.write(frame)
			frame_count += 1

		# Check if the duration limit has been reached
		if frame_count == duration * frame_rate:
			# Release the current output video
			writer.release()

			# Start a new output video
			video_count += 1
			output_path = os.path.join(output_directory, f"output_{video_count}.avi")
			writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (int(video.get(3)), int(video.get(4))))
			frame_count = 0

	# Release the video file and the last output video
	video.release()
	writer.release()
	print("Video division completed.")

video_file = "C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/files/Reol - 綺羅綺羅  GLITTER Music Video.mp4"

# Example usage
video_path = "path/to/video.mp4"
output_directory = "output_videos"
duration = 10  # Duration of each output video in seconds
divide_video(video_file, output_directory, duration)

