from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import math


def split_audio(audio_file, output_folder, segment_duration, extension):
	audio = AudioSegment.from_file(audio_file)

	total_duration = len(audio)

	num_segments = total_duration // segment_duration

	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	for i in range(math.ceil(num_segments)):
		start_time = i * segment_duration
		end_time = (i + 1) * segment_duration
		segment = audio[start_time:end_time]

		output_file = os.path.join(output_folder, f"segment_{i+1}.{extension}")
		segment.export(output_file, format=extension)

	print(f"{num_segments} segments have been created.")


def split_video(input_file, output_folder, segment_duration):

	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	video_duration = get_video_duration(input_file)

	num_segments = video_duration // segment_duration

	for i in range(math.ceil(num_segments)):
		start_time = i * segment_duration
		end_time = (i + 1) * segment_duration
		output_file = os.path.join(output_folder, f"segment_{i+1}.mp4")

		ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)

	print(f"{num_segments} segments have been created.")

def get_video_duration(file_path):
	video = moviepy.editor.VideoFileClip(file_path)
	duration = video.duration
	video.close()
	return duration

