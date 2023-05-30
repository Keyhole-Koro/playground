
import io
import moviepy.editor as mp
import tempfile

# File path of the video
video_filepath = "C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/files/Reol - 綺羅綺羅  GLITTER Music Video.mp4"
# Buffer size in bytes
buffer_size = 1024 * 1024  # 1 MB

# Create a buffer to store the video data
buffer = bytearray()

# Function to fill the buffer with video data
def fill_buffer():
    with open(video_filepath, "rb") as file:
        while True:
            chunk = file.read(buffer_size)
            if not chunk:
                break
            buffer.extend(chunk)

# Function to play the video from the buffer with sound
def play_video_with_sound():
    # Save buffer data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(buffer)
        temp_filepath = temp_file.name

    # Create a moviepy video clip from the temporary file
    video_clip = mp.VideoFileClip(temp_filepath)

    # Play the video clip with sound
    video_clip.preview()

    # Delete the temporary file
    temp_file.close()

# Fill the buffer with video data
fill_buffer()

# Play the video from the buffer with sound
play_video_with_sound()
