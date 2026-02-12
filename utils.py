import yt_dlp
import os
from shazamio import Shazam



def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            size = info.get('filesize') or info.get('filesize_approx') or 0
            return {
                'title': info.get('title'),
                'size_mb': round(size / (1024 * 1024), 2)
            }
    except:
        return None


def download_video(url, quality):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'merge_output_format': 'mp4'
    }

    if quality == "audio":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    else:
        # 🔥 MP4 format majburiy
        ydl_opts['format'] = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
        ydl_opts['merge_output_format'] = 'mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return os.path.splitext(filename)[0] + ".mp4"
    except Exception as e:
        print("Download Error:", e)
        return None


def download_social_video(url):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except:
        return None


async def identify_track(file_path):
    shazam = Shazam()
    try:
        result = await shazam.recognize(file_path)

        if result and "track" in result:
            return {
                "title": result["track"].get("title"),
                "author": result["track"].get("subtitle"),
                "image": result["track"].get("images", {}).get("coverarthq")
            }
    except:
        return None

def download_audio_by_title(title):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    search_query = f"ytsearch1:{title}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            video = info['entries'][0]
            filename = ydl.prepare_filename(video)
            return os.path.splitext(filename)[0] + ".mp3"
    except Exception as e:
        print("Audio Search Error:", e)
        return None
