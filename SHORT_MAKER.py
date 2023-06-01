# SHORT VIDEO MAKER

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
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

print(Fore.GREEN + "[+] Started!")
print("")
print(Fore.GREEN + "[+] " + Fore.RESET + "Running setup...")
print("")
print(Fore.GREEN + "[+] " + Fore.RESET + "Grabbing API info...")

reddit = praw.Reddit(client_id='nhwS_8hLu9WOa45BUeZyLw',
                     client_secret='twh3hGnB--2e2RjQ9Zpfm6pqQvBjhg',
                     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')

print(Fore.BLUE + "[*] " + Fore.RESET + "Grabbed API info!")

print(Fore.GREEN + "[+] " + Fore.RESET + "Cleaning up...")
shutil.rmtree("downloaded")
print(Fore.BLUE + "[*] " + Fore.RESET + "Cleaned!")

print(Fore.BLUE + "[*] " + Fore.RESET + "Define the alternative subreddits")
Meme_subreddits = ['okbuddyretard', 'dankmemes', 'doodoofard', 'wholesomememes', 'shitposting', 'holesome', 'whenthe', 'Offensive_Memes', 'MemeVideos', 'discordVideos']

print(Fore.GREEN + "[+] " + Fore.RESET + "Loading variables...")
min_duration = 3  # Minimum duration in seconds for videos
max_duration = 10  # Maximum duration in seconds for videos
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


while loop_count < 7:
    try:
        loop_count += 1  # Increment the loop count
        subred = random.choice(Meme_subreddits)
        subreddit = reddit.subreddit(subred)
        print(Fore.GREEN + "[*] " + Fore.RESET + "Selected sub: " + Fore.BLUE + subred + Fore.RESET)
        
        # Load used posts from the text document
        with open(used_memes_file, 'r') as file:
            used_memes = file.read().splitlines()
        print(Fore.GREEN + "[+] " + Fore.RESET + "Gathering Posts...")
        top_posts = []
        for submission in subreddit.hot(limit=500):
            if submission.over_18:
                continue
            if submission.is_video and submission.media and 'reddit_video' in submission.media and 'duration' in submission.media['reddit_video']:
                video_duration = submission.media['reddit_video']['duration']
                if min_duration <= video_duration <= max_duration and submission.id not in used_memes:
                    top_posts.append(submission)
                    used_memes.append(submission.id)
                    if len(top_posts) == 3:
                        break

        print(Fore.BLUE + "[*] " + Fore.RESET + "Pulled posts!")
        # Check if the number of top posts is less than 10
        if len(top_posts) < 3:
            print("")
            print(Fore.RED + "[!] " + Fore.RESET + "Sub leached, picking new one:")
            loop_count -= 1
            continue
            
        # Append new posts to the text document
        with open(used_memes_file, 'a') as file:
            for post in top_posts:
                print(Fore.GREEN + "[+] " + Fore.RESET + "Writing post ID to used_posts: " + Fore.BLUE + post.id)
                file.write(post.id + '\n')

        print("")
        # Print top posts with score and color
        print(Fore.GREEN + "[$] Top Rated Memes: " + Fore.RESET)
        print("=====================================")
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
        print("")

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

            print(Fore.GREEN + "[+] " + Fore.RESET + "Loading the background videos...")
            bg1 = ("background_vids/bg1.mp4")
            bg2 = ("background_vids/bg2.mp4")
            bg3 = ("background_vids/bg3.mp4")
            bg4 = ("background_vids/bg4.mp4")
            bg5 = ("background_vids/bg5.mp4")
            bg6 = ("background_vids/bg6.mp4")
            print(Fore.BLUE + "[*] " + Fore.RESET + "Loaded!")
            bg_opts = [bg1, bg2, bg3, bg4, bg5, bg6]
            print(Fore.BLUE + "[*] " + Fore.RESET + "Turned options to a list!")
            print(Fore.GREEN + "[+] " + Fore.RESET + "Picking random one...")
            mcbg = random.choice(bg_opts)
            print(Fore.BLUE + "[*] " + Fore.RESET + "Picked background: " + Fore.BLUE + mcbg + Fore.RESET)

            # Load the Minecraft background video
            minecraft_bg = VideoFileClip(mcbg)

            # Get the dimensions of the Minecraft background video
            bg_width, bg_height = minecraft_bg.size

            if isinstance(video_path, str) and os.path.isfile(video_path):
                try:
                    clip = VideoFileClip(video_path)
                    # Resize the clip while preserving its aspect ratio
                    clip = clip.resize((bg_width, int(clip.size[1] * bg_width / clip.size[0])))


                    bg_music = AudioFileClip("background_vids/background_music.mp3")
                    if clip.audio is None:
                    # Set the duration of the background music to the duration of the current clip
                        bg_music_clip = bg_music.subclip(0, clip.duration)
                        clip = clip.set_audio(bg_music_clip)
                        # Add letterboxing to fill the remaining space
                        clip = clip.set_position(('center', 'center')).on_color(size=(bg_width, bg_height), color=(0, 0, 0), pos=('center', 'center'))
                        clips.append(clip)



                    # Add letterboxing to fill the remaining space
                    clip = clip.set_position(('center', 'center')).on_color(size=(bg_width, bg_height),
                                                                            color=(0, 0, 0), pos=('center', 'center'))

                    clips.append(clip)
                    durations.append(clip.duration)
                except OSError as e:
                    print(f"Error loading video: {e}")
            else:
                print(f"Invalid video path: {video_path}")

        final_duration = sum(durations)

        print(Fore.GREEN + "[+] " + Fore.RESET + "Creating background...")

        # Resize the Minecraft background video to match the dimensions of the clips
        minecraft_bg = minecraft_bg.resize(minecraft_bg.size)

        # Set durations
        minecraft_bg = minecraft_bg.set_duration(final_duration)

        print(Fore.BLUE + "[*] " + Fore.RESET + "Background made!")
        print("")
        print(Fore.GREEN + f"[+] " + Fore.RESET + "Creating clip comp...")
        print(Fore.BLUE + "[+] " + Fore.RESET + "Stitching...")

        # Concatenate the clips
        final_clip = concatenate_videoclips(clips, method="compose")

        print(Fore.BLUE + "[*] " + Fore.RESET + "Stitched!")
        print(Fore.BLUE + "[+] " + Fore.RESET + "Composeing comp...")

        # Set the durations of the clips
        final_clip = final_clip.set_duration(final_duration)

        # Overlay the clips on the Minecraft background
        final_clip = CompositeVideoClip([minecraft_bg.set_position(('center', 'center')),
                                         final_clip.set_position(('center', 'center'))])

        print(Fore.BLUE + "[*] " + Fore.RESET + "Composed!")

        print(Fore.GREEN + "[+] " + Fore.RESET + "Generating video comp...")
        output_path = f"comp_{loop_count}.mp4"  # Append loop count to the file name
        final_clip.write_videofile(output_path)
        print(Fore.BLUE + "[*] " + Fore.RESET + "Generated video!")
        print("")

    except KeyboardInterrupt:
        # Ctrl+C was pressed, break out of the loop
        break

print(Fore.BLUE + "[+] " + Fore.RESET + "Loop complete!")
print("")
print(Fore.GREEN + Back.LIGHTGREEN_EX + "[=====================]" + Back.RESET)
print(Fore.GREEN + Back.BLUE + "[   F I N I S H E D   ]" + Back.RESET)
print(Fore.GREEN + Back.LIGHTGREEN_EX + "[=====================]" + Back.RESET)
