# DIRECT DOWNLOAD FROM YOUTUBE - VIDEO TO IMAGE CONVERTER 
"""
Usage - Single-GPU training:
    $ python3 vid2imgconv.py --url https://www.youtube.com/shorts/_j-jkkR-Ovw --fps 1 (recommended)
    $ python3 vid2imgconv.py --url https://www.youtube.com/shorts/_j-jkkR-Ovw --fps 1 --start 17  #extracting image from a particular second of the video


Sample Videos:            downloaded_videos/
Sample Extracted Images:  extracted_images/
"""


import os
import cv2
import argparse
import urllib.error
from pytube import YouTube

def download_video(url, save_path):
    try:
    # Log in to YouTube
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path=save_path)
        print("Video downloaded successfully.")
    except Exception as e:
        print("Error:", e)

def convert_to_images(video_path, output_folder, frame_rate=3, start_frame=0, end_frame=None):
    try:
        video_capture = cv2.VideoCapture(video_path)
        frame_count = 0

        # Get the video file name without extension
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                break
            if frame_count % (int(video_capture.get(cv2.CAP_PROP_FPS)) // frame_rate) == 0:
                if start_frame <= frame_count and (end_frame is None or frame_count <= end_frame):
                    image_filename = f"{video_name}_frame_{frame_count}.jpg"
                    image_path = os.path.join(output_folder, image_filename)
                    cv2.imwrite(image_path, frame)
            frame_count += 1
        video_capture.release()
        print("Video converted to images successfully.")
    except urllib.error.URLError as e:
        print("Error:", e)

def main():
    parser = argparse.ArgumentParser(description="Download YouTube video, crop, and convert to images.")
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--fps", type=int, default=3, help="Frame rate for image extraction")
    parser.add_argument("--start", type=int, default=0, help="Start frame (in seconds)")
    parser.add_argument("--end", type=int, default=None, help="End frame (in seconds, default: last frame)")
    args = parser.parse_args()

    download_folder = "downloaded_videos"
    images_folder = "extracted_images"

    os.makedirs(download_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)

    download_video(args.url, download_folder)

    downloaded_files = os.listdir(download_folder)
    if downloaded_files:
        for video_file in downloaded_files:
            video_path = os.path.join(download_folder, video_file)
            # Convert end_frame value to frames directly
            end_frame = None if args.end is None else int(args.end * args.fps)
            convert_to_images(video_path, images_folder, args.fps, args.start * args.fps, end_frame)
    else:
        print("No video downloaded!")
        
     # Process only the newly downloaded video
    new_downloaded_files = [f for f in os.listdir(download_folder) if f not in already_downloaded]
    if new_downloaded_files:
        for video_file in new_downloaded_files:
            video_path = os.path.join(download_folder, video_file)
            # Convert end_frame value to frames directly
            end_frame = None if args.end is None else int(args.end * args.fps)
            convert_to_images(video_path, images_folder, args.fps, args.start * args.fps, end_frame)
    else:
        print("No new videos downloaded!")

if __name__ == "__main__":
    already_downloaded = set(os.listdir("downloaded_videos"))
    main()