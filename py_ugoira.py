#!/bin/usr/env python

import argparse
import json
import os
import re
import shlex
import subprocess
import urllib.request
import zipfile


def fetch_ugoira(pixiv_id, video_type, ffmpeg_path, ffmpeg_args):
    pixiv_url = f'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={pixiv_id}'

    req = urllib.request.Request(pixiv_url)
    res = urllib.request.urlopen(req)
    pixiv_data_line = None

    for line in res.readlines():
        line = line.decode('utf-8')

        if 'pixiv.context.ugokuIllustData' in line:
            pixiv_data_line = line
            break

    if pixiv_data_line:
        pixiv_data_line = re.sub(r'^.+?pixiv\.context\.ugokuIllustData\s+=', '', pixiv_data_line)
        pixiv_data_line = re.sub(r';<\/script>.*?$', '', pixiv_data_line)

        ugoira_data = json.loads(pixiv_data_line)
        ugoira_url = re.sub(r'ugoira\d+x\d+', 'ugoira1920x1080', ugoira_data['src'])

        req = urllib.request.Request(ugoira_url)
        req.add_header('Referer', pixiv_url)

        ugoira_file = f'ugoira_{pixiv_id}.zip'
        ugoira_folder = f'ugoira_{pixiv_id}'
        chunk_size = 4 * 1024

        with urllib.request.urlopen(req) as res, open(ugoira_file, 'wb') as out_file:
            while True:
                chunk = res.read(chunk_size)
                if chunk:
                    out_file.write(chunk)
                else:
                    break

        with zipfile.ZipFile(ugoira_file, 'r') as zip_ref:
            zip_ref.extractall(ugoira_folder)

        os.remove(ugoira_file)

        # https://superuser.com/questions/617392/ffmpeg-image-sequence-with-various-durations
        ffconcat_file = os.path.join(ugoira_folder, 'ffconcat.txt')
        with open(ffconcat_file, 'w') as out_file:
            out_file.write('ffconcat version 1.0\n')

            # https://video.stackexchange.com/questions/20588/ffmpeg-flash-frames-last-still-image-in-concat-sequence
            last_frame = ugoira_data['frames'][-1].copy()
            last_frame['delay'] = 1
            ugoira_data['frames'].append(last_frame)

            for frame in ugoira_data['frames']:
                frame_file = frame['file']
                frame_duration = frame['delay'] / 1000
                frame_duration = round(frame_duration, 4)

                out_file.write(
                    f'file {frame_file}\n'
                    f'duration {frame_duration}\n'
                )

        call_stack = []
        call_stack += shlex.split(
            f'{ffmpeg_path} -hide_banner -y '
            '-i ffconcat.txt '
            # '-filter:v "minterpolate=\'fps=60\'" '
        )
        call_stack += shlex.split(ffmpeg_args)
        call_stack += shlex.split(
            f'output.{video_type}'
        )

        print(call_stack)
        subprocess.call(
            call_stack,
            cwd=os.path.abspath(ugoira_folder),
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            'ugoira to webm'
        )
    )
    parser.add_argument(
        '--id', type=int, required=True, dest='pixiv_id',
        help='pixiv id',
    )
    parser.add_argument(
        '--video_type', type=str, required=False, default='webm',
        help='video file type',
    )
    parser.add_argument(
        '--ffmpeg_path', type=str, required=False, default='ffmpeg',
        help='path to ffmpeg',
    )
    parser.add_argument(
        '--ffmpeg_args', type=str, required=False,
        default='-c:v libvpx -crf 10 -b:v 2M -an',
        help='args for ffmpeg',
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    args = vars(args)

    fetch_ugoira(**args)
