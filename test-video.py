#with open("C:/Users/kiho/Downloads/20.ts", 'rb')as v:
#	print(v.read())
#	print(type(v.read()))
import cv2

# Load the videos
video1 = cv2.VideoCapture("C:/Users/kiho/Downloads/19.ts")
video2 = cv2.VideoCapture("C:/Users/kiho/Downloads/20.ts")
video_paths = ["C:/Users/kiho/Downloads/19.ts", "C:/Users/kiho/Downloads/20.ts"]

# Open the video capture object for the continuous video
continuous_video = cv2.VideoCapture('continuous_video.mp4')

# Get the video dimensions of the continuous video
width = int(continuous_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(continuous_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a VideoWriter object to save the merged video
merged_video = cv2.VideoWriter('merged_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

# Iterate over each video file path
for video_path in video_paths:
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Loop until the continuous video ends
    while continuous_video.isOpened():
        # Read the next frame from the continuous video
        ret_continuous, frame_continuous = continuous_video.read()
        
        # Check if the frame is read successfully
        if not ret_continuous:
            break
        
        # Display the frame from the continuous video
        cv2.imshow('Merged Video', frame_continuous)
        
        # Write the frame from the continuous video to the merged video
        merged_video.write(frame_continuous)
        
        # Read the next frame from the video being merged
        ret, frame = video.read()
        
        # Check if the frame is read successfully
        if not ret:
            break
        
        # Resize the frame to match the dimensions of the continuous video
        frame = cv2.resize(frame, (width, height))
        
        # Display the frame from the video being merged
        cv2.imshow('Video Being Merged', frame)
        
        # Write the frame from the video being merged to the merged video
        merged_video.write(frame)
        
        # Delay for 30 milliseconds to maintain the video playback speed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    # Release the video object
    video.release()

# Release the continuous video and merged video objects
continuous_video.release()
merged_video.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()