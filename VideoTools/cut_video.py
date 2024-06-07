# -*- coding: utf-8 -*-
# @Time    : 2023/10/26 14:06
# @Author  : Kenny Zhou
# @FileName: cut_video.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import os
import subprocess
import argparse

def split_videos(input_folder, output_folder, segment_duration):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有视频文件
    video_files = [f for f in os.listdir(input_folder) if f.endswith('.mp4')]

    for video_file in video_files:
        input_path = os.path.join(input_folder, video_file)
        output_subfolder = os.path.join(output_folder, os.path.splitext(video_file)[0])
        os.makedirs(output_subfolder, exist_ok=True)

        # 使用FFmpeg进行切分，指定硬件加速
        command = f'ffmpeg -hwaccel videotoolbox -i "{input_path}" -c:v h264_videotoolbox -b:v 1024k -c:a aac -strict -2 -f segment -segment_time {segment_duration} -reset_timestamps 1 "{output_subfolder}/%04d.mp4"'
        subprocess.run(command, shell=True)

    print("切分完成")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频切分工具")
    parser.add_argument("-i", dest="input_folder", required=True, help="输入文件夹路径")
    parser.add_argument("-o", dest="output_folder", required=True, help="输出文件夹路径")
    parser.add_argument("--segment_duration", type=int, default=2, help="切分秒数")

    args = parser.parse_args()

    split_videos(args.input_folder, args.output_folder, args.segment_duration)


