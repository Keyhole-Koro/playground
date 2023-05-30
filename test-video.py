#with open("C:/Users/kiho/Downloads/20.ts", 'rb')as v:
#	print(v.read())
#	print(type(v.read()))
import cv2
import sounddevice as sd

# Define the video file path
video_path = 'your_video.mp4'

# Open the video file using cv2.VideoCapture
cap = cv2.VideoCapture(video_path)

# Get the video properties
fps = cap.get(cv2.CAP_PROP_FPS)

# Read the audio from the video using sounddevice
audio, sample_rate = sd.read(video_path, dtype='float32')

# Create an audio playback stream
stream = sd.OutputStream(channels=audio.shape[1], samplerate=sample_rate)

# Start the audio playback
stream.start()

# Read and display frames from the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Display the frame using cv2.imshow
    cv2.imshow('Video', frame)
    
    # Check for keyboard events and quit if 'q' is pressed
    if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
        break

# Release the video capture and stop the audio stream
cap.release()
stream.stop()

# Close all OpenCV windows
cv2.destroyAllWindows()
