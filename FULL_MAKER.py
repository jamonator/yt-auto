# FULL VIDEO MAKER

import praw
import os
from colorama import Fore, Style, Back
from redvid import Downloader
import pyautogui
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ColorClip, CompositeAudioClip, AudioFileClip
import random
import shutil
from moviepy.audio.fx.all import audio_fadeout
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

print(Fore.GREEN + "[+] Started!")

print(Fore.GREEN + "[+] " + Fore.RESET + "Grabbing oAPI inf")
reddit = praw.Reddit(client_id='nhwS_8hLu9WOa45BUeZyLw',
                     client_secret='twh3hGnB--2e2RjQ9Zpfm6pqQvBjhg',
                     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
print(Fore.BLUE + "[*] " + Fore.RESET + "Grabbed API info")

print(Fore.GREEN + "[*] " + Fore.RESET + "Running setup...")

print(Fore.BLUE + "[*] " + Fore.RESET + "Define the alternative subreddits")
Meme_subreddits = ['okbuddyretard', 'dankmemes', 'doodoofard', 'wholesomememes', 'shitposting', 'holesome', 'whenthe', 'Offensive_Memes', 'MemeVideos', 'discordVideos']

print(Fore.GREEN + "[+] " + Fore.RESET + "Cleaning up...")
shutil.rmtree("downloaded")
print(Fore.BLUE + "[*] " + Fore.RESET + "Cleaned!")

print(Fore.GREEN + "[+] " + Fore.RESET + "Loading varibles...")
min_duration = 5  # Minimum duration in seconds for videos
max_duration = 15  # Maximum duration in seconds for videos
used_memes_file = 'used_posts.txt'
loop_count = 0  # Variable to keep track of the loop count
video_counter = 0
print(Fore.BLUE + "[*] " + Fore.RESET + "Loaded!")

print(Fore.GREEN + "[+] " + Fore.RESET + "Making temp folder...")
os.mkdir("downloaded")
print(Fore.BLUE + "[*] " + Fore.RESET + "Made temp download folder!")

print("")
print(Fore.GREEN + "[+] " + Fore.RESET + "Starting loop...")

# Define a function to check the audio level of a clip
def is_silent(clip):
    audio = clip.audio
    if audio is None:
        return True
    audio.write_audiofile("temp_audio.wav")
    audio_segment = AudioSegment.from_wav("temp_audio.wav")
    silent_ranges = detect_nonsilent(audio_segment)
    if len(silent_ranges) == 0:
        return True
    return False

while loop_count < 10:
    try:
        loop_count += 1  # Increment the loop count
        subred = random.choice(Meme_subreddits)
        subreddit = reddit.subreddit(subred)
        print(Fore.GREEN + "[*] " + Fore.RESET + "Selected sub: " + subred)
        
        # Load used posts from the text document
        with open(used_memes_file, 'r') as file:
            used_memes = file.read().splitlines()
        print(Fore.BLUE + "[*] " + Fore.RESET + "Gathering Posts!")
        top_posts = []
        for submission in subreddit.top(limit=500):
            if submission.over_18:
                continue
            if submission.is_video and submission.media and 'reddit_video' in submission.media and 'duration' in submission.media['reddit_video']:
                video_duration = submission.media['reddit_video']['duration']
                if min_duration <= video_duration <= max_duration and submission.id not in used_memes:
                    top_posts.append(submission)
                    used_memes.append(submission.id)
                    if len(top_posts) == 10:
                        break

        print(Fore.GREEN + "[+] " + Fore.RESET + "Pulled posts!")
        # Check if the number of top posts is less than 10
        if len(top_posts) < 10:
            print(Fore.RED + "[!] " + Fore.RESET + "Sub leached, picking new one:")
            loop_count -= 1
            continue
            
        # Append new posts to the text document
        with open(used_memes_file, 'a') as file:
            for post in top_posts:
                print(Fore.GREEN + "[+] " + Fore.RESET + "Writing post ID to used_posts: " + Fore.BLUE + post.id)
                file.write(post.id + '\n')


        # Print top posts with score and color
        print(Fore.GREEN + "[$] " + Fore.RESET + "Top Rated Memes: ")
        for i, post in enumerate(top_posts):
            score = post.score
            if score < 100:
                score_color = Fore.RED
            elif score < 250:
                score_color = Fore.YELLOW
            elif score < 500:
                score_color = Fore.LIGHTYELLOW_EX
            elif score < 1000:
                score_color = Fore.LIGHTGREEN_EX
            else:
                score_color = Fore.GREEN

            print(f"{i+1}.| Sub: {subred} | Post: {post.title} | Score = {score_color}{score}{Style.RESET_ALL}")

        print(Fore.GREEN + "[+] " + Fore.RESET + "Starting downloads...")
        # Download the top posts using redvid
        reddit_downloader = Downloader()
        reddit_downloader.path = "downloaded"
        clips = []
        durations = []
        for post in top_posts:
            reddit_downloader.url = post.url
            video_path = reddit_downloader.download()
            pyautogui.typewrite('1')
            time.sleep(0.2)
            pyautogui.press("enter")
            time.sleep(0.2)
            print(Fore.BLUE + "[*] " + Fore.RESET + "Downloaded!")

            if isinstance(video_path, str) and os.path.isfile(video_path):
                try:
                    clip = VideoFileClip(video_path)
                    print(Fore.GREEN + "[+] " + Fore.RESET + "Making video file...")
                    # Calculate the desired height while maintaining the aspect ratio
                    target_height = 720  # Adjust the target height as needed
                    target_width = clip.size[0] * target_height // clip.size[1]
       
                    bg_music = AudioFileClip("background_vids/background_music.mp3")
                    if clip.audio is None:
                    # Set the duration of the background music to the duration of the current clip
                        bg_music_clip = bg_music.subclip(0, clip.duration)
                        clip = clip.set_audio(bg_music_clip)
                        # Add letterboxing to fill the remaining space
                        clip = clip.set_position(('center', 'center')).on_color(size=(bg_width, bg_height), color=(0, 0, 0), pos=('center', 'center'))
                        clips.append(clip)

                    # Resize the clip to fit the screen from top to bottom and adjust width
                    resized_clip = clip.resize(height=target_height, width=target_width)
                    clips.append(resized_clip)
                    durations.append(resized_clip.duration)
                    print(Fore.BLUE + "[*] " + Fore.RESET + "File generated!")

                except OSError as e:
                    print(f"Error loading video: {e}")
            else:
                print(f"Invalid video path: {video_path}")

        final_duration = sum(durations)

        print(Fore.GREEN + "[+] " + Fore.RESET + "Creating background...")

        # Load the background video
        bg_color = (0, 0, 0)  # RGB values for black color
        minecraft_bg = ColorClip(size=(1920, 1080), color=bg_color, duration=final_duration)
        minecraft_bg = minecraft_bg.set_duration(final_duration)

        print(Fore.BLUE + "[*] " + Fore.RESET + "Background made!")

        # Concatenate the clips and overlay them on the Minecraft background
        print(Fore.GREEN + f"[+] " + Fore.RESET + "Creating clip comp...")
        print(Fore.GREEN + "[+] " + Fore.RESET + "Stitching...")
        final_clip = concatenate_videoclips(clips)
        print(Fore.BLUE + "[*] " + Fore.RESET + "Stitched!")
        print(Fore.GREEN + "[+] " + Fore.RESET + "Composeing comp...")
        final_clip = CompositeVideoClip([minecraft_bg.set_position(('center', 'center')), final_clip.set_position(('center', 'center'))])
        print(Fore.BLUE + "[*] " + Fore.RESET + "Composed!")
        output_path = f"COMPILER/comp_{loop_count}.mp4"  # Append loop count to the file name
        print(Fore.GREEN + "[+] " + Fore.RESET + "Generating video comp...")
        final_clip.write_videofile(output_path)
        print(Fore.BLUE + "[*] " + Fore.RESET + "Generated video!")

    except KeyboardInterrupt:
        # Ctrl+C was pressed, break out of the loop
        break

print(Fore.BLUE + "[+] " + Fore.RESET + "Loop complete!")
print(Fore.GREEN + "[+] " + Fore.RESET + "Starting Full Video creator...")

intro = VideoFileClip("intro.mp4")
comp1 = VideoFileClip("comp_1.mp4")
comp2 = VideoFileClip("comp_2.mp4")
comp3 = VideoFileClip("comp_3.mp4")
comp4 = VideoFileClip("comp_4.mp4")
comp5 = VideoFileClip("comp_5.mp4")
comp6 = VideoFileClip("comp_6.mp4")
comp7 = VideoFileClip("comp_7.mp4")
comp8 = VideoFileClip("comp_8.mp4")
comp9 = VideoFileClip("comp_9.mp4")
comp10 = VideoFileClip("comp_10.mp4")
outro = VideoFileClip("outro.mp4")

print(Fore.GREEN + "[+] " + Fore.RESET + "Compiling comps and intro/outro... ")

comps = [comp1, comp2, comp3, comp4, comp5, comp6, comp7, comp8, comp9, comp10]

full_comp = concatenate_videoclips(comps)

full_comp_loc = "COMPILER/Full_comp.mp4"

full_comp.write_videofile(full_comp_loc)

print(Fore.BLUE + "[*] " + Fore.RESET + "Compiled! ")
print(Fore.GREEN + "[+] " + Fore.RESET + "Writing full video...")

comp_lo = VideoFileClip("COMPILER/Full_comp.mp4")

vids = [intro, comp_lo, outro]
# Combine all the clips into one video
YT_vid = concatenate_videoclips(vids, method='compose')

YT_out = "UPLOAD/Finished_video.mp4"

YT_vid.write_videofile(YT_out, codec="libx264", audio_codec="mp3")
print(Fore.BLUE + "[*] " + Fore.RESET + "Written!")
print("")
print(Fore.BLUE + "[+] " + Fore.RESET + "Loop complete!")
print("")
print(Fore.GREEN + "[+] " + Fore.RESET + "Cleaning up...")
shutil.rmtree("downloaded")
print(Fore.BLUE + "[*] " + Fore.RESET + "Cleaned!")
print("")
print(Fore.GREEN + Back.LIGHTGREEN_EX + "[=====================]" + Back.RESET)
print(Fore.GREEN + Back.BLUE + "[   F I N I S H E D   ]" + Back.RESET)
print(Fore.GREEN + Back.LIGHTGREEN_EX + "[=====================]" + Back.RESET)