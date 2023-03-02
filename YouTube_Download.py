from pytube import YouTube
import inquirer
import sys, os
# import tempfile
from moviepy.editor import *
# import ffmpeg

def on_progress(Any, bytes, ints):
    print(ints/(1024*1024))

url = sys.argv[1]
yt = YouTube(sys.argv[1], proxies={"http": "http://61.233.25.166:80"},on_progress_callback=on_progress)
titles = yt.title.replace(' ','')
title = titles.replace('|','_').replace("'","").replace('(','').replace(')','').replace('/','')
def videoInfo(url):
    videoinfos={}
    for info in yt.streams:
        if info.mime_type == 'video/mp4' :
            videoinfos[info.resolution] = info.itag
        elif info.mime_type == 'audio/mp4':
            videoinfos['audio'] = [info.itag, info.abr]
    return videoinfos

info = (videoInfo(sys.argv[1]))



current_dir = os.getcwd()
# videopath = os.path.join(tempfile.gettempdir())
# audiopath = os.path.join(tempfile.gettempdir())
questions = [
  inquirer.Checkbox('select_files',
                    message="What are you interested in?",
                    choices = [file for file in info if file != 'audio'],
                  )          
]

choose = inquirer.prompt(questions)
reso = choose['select_files']

video_stream = yt.streams.get_by_itag(info[reso[0]])
video_stream.download(output_path=current_dir, filename=f'{title}.mp4')

audio_stream = yt.streams.get_by_itag(info['audio'][0])
audio_stream.download(output_path=current_dir, filename=f'{title}.mp3')



clip = VideoFileClip(f'{title}.mp4')
audioclip = AudioFileClip(f'{title}.mp3')
videoclip = clip.set_audio(audioclip)
videoclip.write_videofile(f"{title}M.mp4", fps=24, preset='ultrafast', threads=10, codec='libx265')

if os.path.exists(current_dir+f'\{title}.mp4'):
    os.unlink(current_dir+f'\{title}.mp4')

if os.path.exists(current_dir+f'\{title}.mp3'):
    os.unlink(current_dir+f'\{title}.mp3')




# "C:\Users\sande\AppData\Local\Temp\audio.mp3"
# video = videopath+f'\{yt.title}.mp4'
# audio = audiopath+f'\{yt.title}.mp3'
# print(bool(audio))
# input_video = ffmpeg.input(videopath)
# input_audio = ffmpeg.input(audiopath)
# ffmpeg.concat(
#     input_video, input_audio, v=1, a=1).output(
#     f'{yt.title}.mp4').run(
#     overwrite_output=True, cmd=current_dir)

# "C:\Users\sande\AppData\Local\Temp\Alan Walker - Faded.mp4\Alan Walker - Faded.mp4"