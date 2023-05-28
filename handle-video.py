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

def separate_video(video_path, output_directory):
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

	# Read frames from the video and save them as images
	while success:
		# Read the next frame
		success, frame = video.read()

		# Save the frame as an image
		if success:
			frame_path = os.path.join(output_directory, f"frame_{frame_count}.jpg")
			cv2.imwrite(frame_path, frame)
			frame_count += 1

	# Release the video file
	video.release()
	print("Video separation completed.")

# Example usage
video_path = "path/to/video.mp4"
output_directory = "output_frames"
video_file = "C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/files/Reol - 綺羅綺羅  GLITTER Music Video.mp4"
separate_video(video_file, output_directory)

# Usage example
input_file = "input_video.mp4"
output_prefix = "output_segment"
segment_duration = 10  # Duration of each segment in seconds

#split_video(video_file, output_prefix, segment_duration)
