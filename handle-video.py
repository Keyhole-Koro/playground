import cv2
import threading
from io import BytesIO
import base64
import tempfile
import os

video_file = "C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/files/Reol - 綺羅綺羅  GLITTER Music Video.mp4"
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

import subprocess

import cv2
from pydub import AudioSegment

def extract_audio(input_video_path, output_audio_path):
	# Read the video using cv2.VideoCapture
	video_capture = cv2.VideoCapture(input_video_path)

	# Get audio properties
	audio_fps = video_capture.get(cv2.CAP_PROP_FPS)
	audio_frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

	# Read audio frames
	audio_frames = []
	for _ in range(audio_frame_count):
		ret, frame = video_capture.read()
		if not ret:
			break
		audio_frames.append(frame.tobytes())

	# Create audio segment
	audio_segment = AudioSegment(
		data=b''.join(audio_frames),
		sample_width=video_capture.get(cv2.CAP_PROP_SAMPWIDTH),
		frame_rate=audio_fps,
		channels=video_capture.get(cv2.CAP_PROP_CHANNELS)
	)

	# Export audio segment to file
	audio_segment.export(output_audio_path, format="mp3")

	# Release video capture object
	video_capture.release()

# Example usage
input_video = "input_video.mp4"
output_audio = "output_audio.mp3"


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
	output_path = os.path.join(output_directory, f"output_{video_count}.mp4")
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
			output_path = os.path.join(output_directory, f"output_{video_count}.mp4")
			writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (int(video.get(3)), int(video.get(4))))
			frame_count = 0

	# Release the video file and the last output video
	video.release()
	writer.release()
	print("Video division completed.")

# Example usage
output_directory = "output_videos_audio"
duration = 10  # Duration of each output video in seconds

#divide_video(video_file, output_directory, duration)
#extract_audio(video_file, output_audio)

#with open("C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/files/output_videos/output_1.mp4")as f:
#	video = f.read()
#	print(video)
#	print(type(video))




# 使用方法
# $ python mp4_descripter.py [引数1] [引数2]
#
# 引数1: ファイル名
# 引数2: 内容を表示したいコンテナのインデックス

import sys
import binascii

leaf_list = ['fiel', 'mdat', 'rdrf', 'rmcd', 'rmcs', 'rmdr', 'rmqu', 'rmvc', 'wfex', 'cmvd', 'co64', 'dcom', 'elst', 'gmhd', 'hdlr', 'mdhd', 'smhd', 'stco', 'stsc', 'stsd', 'stss', 'stsz', 'stts', 'tkhd', 'vmhd']
parent_list = ['cmov', 'ctts', 'edts', 'esds', 'free', 'ftyp', 'iods', 'junk', 'mdia', 'minf', 'moov', 'mvhd', 'pict', 'pnot', 'rmda', 'rmra', 'skip', 'stbl', 'trak', 'uuid', 'wide']

def read_container(file, indent, index, end_offset, content_index):
    # read container size
    data = file.read(4)
    size = int.from_bytes(data, byteorder='big')
    if size == 0: return 0

    # read container type
    data = file.read(4)
    type = data.decode("utf-8") 
    is_leaf = (type in leaf_list)

    end = file.tell() + size - 8

    # when container size exceeds 2147483647
    if size == 1:
        file_pos = file.tell()
        data = file.read(8)
        size = int.from_bytes(data, byteorder='big')
        file.seek(file_pos, 0)

    if not is_leaf:
        file_pos = file.tell()
        file.seek(4, 1)
        next_type = ''
        try:
            next_type = file.read(4).decode("utf-8") 
        except Exception:
            next_type = 'unknown box name'
        file.seek(file_pos, 0)
        # unknown box is assumed as leaf
        if next_type not in leaf_list and next_type not in parent_list:
            is_leaf = True

    # make index string
    if index < 10:
        out_text = '0' + str(index) + ': '
    else:
        out_text = str(index) + ': '

    for i in range(indent): out_text += '   '

    if is_leaf:
        out_text += type
        out_text += '  -  '
        out_text += str(size)
        print(out_text)

        if index == int(content_index):
            # print binary data
            print('')
            print('offset:' + str(hex(file.tell() - 8)))
            data = file.read(size - 8)
            strarray = str(binascii.hexlify(data))[2:-1]
            outstr = ''
            for i in range(int(len(strarray) / 2)):
                if i % 8 == 0:
                    outstr = outstr + ' '
                if i % 16 == 0:
                    print(outstr)
                    outstr = ''
                temp = strarray[i*2:i*2+2]
                outstr = outstr + temp + ' '
            print(outstr)
            print('')
        else:
            # move to next container
            file.seek(size - 8, 1)
        return index + 1
    else:
        out_text += type
        print(out_text)
        if index == int(content_index):
            print('')
            print('offset:' + str(hex(file.tell() - 8)))
            print('no data')
            print('')
        index += 1
        while True:
            # move to children
            index = read_container(file, indent + 1, index, end, content_index)
            if file.tell() == end: break
        return index

if __name__ == '__main__':
    file = open(sys.argv[1],'r+b')

    try:
        content_index = sys.argv[2]
    except Exception:
        content_index = 0

    index = 1
    while True:
        index = read_container(file, 1, index, -1, content_index)

        # read_container returns zero when EOF
        if index == 0: break

    file.close()
            # move to next container
            file.seek(size - 8, 1)
        return index + 1
    else:
        out_text += type
        print(out_text)
        if index == int(sys.argv[2]):
            print('')
            print('offset:' + str(hex(file.tell() - 8)))
            print('no data')
            print('')
        index += 1
        while True:
            # move to children
            index = read_container(file, indent + 1, index, end)
            if file.tell() == end: break
        return index

if __name__ == '__main__':
    file = open(sys.argv[1],'r+b')
    index = 1
    index = read_container(file, 1, index, -1)
    index = read_container(file, 1, index, -1)
    file.close()
