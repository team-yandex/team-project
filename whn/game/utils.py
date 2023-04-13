import moviepy.editor


def get_trimmed_video(video_path, to_second):
    video = moviepy.editor.VideoFileClip(video_path)
    trimmed_video = video.subclip(0, to_second)
    return trimmed_video.reader
