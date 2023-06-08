import cv2

def extract_video_part(input_file, output_file, start_time, end_time):
	# Open the video file
	video = cv2.VideoCapture(input_file)

	# Get the frame rate of the video
	fps = video.get(cv2.CAP_PROP_FPS)

	# Calculate the start and end frame indices
	start_frame = int(start_time * fps)
	end_frame = int(end_time * fps)

	# Set the current frame index
	video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

	# Initialize an empty list to store frames
	frames = []

	# Read frames until the end frame is reached
	while video.isOpened() and video.get(cv2.CAP_PROP_POS_FRAMES) <= end_frame:
		ret, frame = video.read()
		if ret:
			frames.append(frame)
		else:
			break

	# Release the video capture
	video.release()

	# Write the extracted frames to a new video file
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	height, width, _ = frames[0].shape
	out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
	for frame in frames:
		out.write(frame)
	out.release()

	# Display the extracted video part
	for frame in frames:
		cv2.imshow("Video Part", frame)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break
	cv2.destroyAllWindows()

# Example usage
input_file = "C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/playground/received_video2.mp4"
output_file = "C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/playground/empty.mp4"
start_time = 10  # Start time in seconds
end_time = 30  # End time in seconds

extract_video_part(input_file, output_file, start_time, end_time)
