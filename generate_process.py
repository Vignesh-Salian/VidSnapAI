# this file look for new folder inside user uploads and convert them to reel if they are not already converted
import os
from text_to_audio import text_to_speech_file
import time
import subprocess

def text_to_audio(folder):
    print("TEXT_TO_AUDIO - ",folder)
    with open(f"user_uploads/{folder}/desc.txt", encoding="utf-8") as f:
        text=f.read()
    print(text,folder)
    if not text or not text.strip():
        print(f"Skipping TTS for {folder}: empty text")
        return False
    text_to_speech_file(text, folder)
    return True


def create_reel(folder, has_audio):
    os.makedirs("static/reels", exist_ok=True)
    if has_audio:
        command = (
            f'ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt '
            f'-i user_uploads/{folder}/audio.mp3 -vf '
            f'"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" '
            f'-c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'
        )
    else:
        command = (
            f'ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -vf '
            f'"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" '
            f'-c:v libx264 -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'
        )
    subprocess.run(command, shell=True, check=True)
    print("CREATE_REEL - ", folder)

if __name__=="__main__":
    while True:
        print("processing queue....")
        if not os.path.exists("done.txt"):
            open("done.txt", "w").close()
            
        with open("done.txt", "r") as f:
            done_folders=f.readlines()
    
        done_folders = [f.strip() for f in done_folders]
        if not os.path.exists("user_uploads"):
            os.makedirs("user_uploads", exist_ok=True)
            
        folders=os.listdir("user_uploads")
        print(folders, done_folders)
        for folder in folders: 
            if(folder not in done_folders):
                try:
                    has_audio = text_to_audio(folder)
                    create_reel(folder, has_audio)
                except Exception as e:
                    print(f"Error processing {folder}: {e}")
                    
                with open("done.txt", "a") as f:
                    f.write(folder + "\n")
        time.sleep(4)