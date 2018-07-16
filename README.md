# py-ugoira

Requires [Python 3.6.x](https://www.python.org/) and [FFmpeg](https://www.ffmpeg.org/).

```sh
$ python py_ugoira.py -h | fold -sw 80
usage: py_ugoira.py [-h] [--pixiv_id PIXIV_ID] [--frames_path FRAMES_PATH]
                    [--process {all,getframes,convertframes}]
                    [--video_output VIDEO_OUTPUT] [--interpolate]
                    [--ffmpeg_path FFMPEG_PATH] [--ffmpeg_args FFMPEG_ARGS]
                    [-v]

Python script to download and convert an ugoira animation on Pixiv, and
convert it to a video via FFmpeg.

optional arguments:
  -h, --help            show this help message and exit
  --pixiv_id PIXIV_ID   The pixiv ID for the ugoira illustration. Required if
                        the --process argument is "all" or "getframes".
  --frames_path FRAMES_PATH
                        The path to where the image frames and ffconcat.txt
                        is. Required if the --process argument is
                        "convertframes".
  --process {all,getframes,convertframes}
                        The process that should take place. "all" will execute
                        both "getframes" and "convertframes". "getframes" will
                        only obtain the ugoira frames, and generate a FFmpeg
                        concat demuxer file. "convertframes" will only convert
                        the ugoira frames into a video type of your choice
                        through FFmpeg.
  --video_output VIDEO_OUTPUT
                        The output filename for the converted video. Defaults
                        to "output.webm".
  --interpolate         Attempts to interpolate the frames to 60 frames per
                        second. Note, it only works well with some ugoira, and
                        would take a longer time to finish conversion. Use
                        with care.
  --ffmpeg_path FFMPEG_PATH
                        The path to the FFmpeg executable.
  --ffmpeg_args FFMPEG_ARGS
                        The arguments for FFmpeg. Defaults to "-c:v libvpx
                        -crf 10 -b:v 2M -an", which is VP8 WEBM with a
                        variable bitrate of 2 MBit/s, with no audio.
  -v, --verbose         Forces the system to print out verbose process
                        messages.
```


### Example usage

```sh
# convert illustration ID 69689053 to webm
python py_ugoira.py --pixiv_id 69689053

# fetch the frames for illustration ID 69689053
python py_ugoira.py --pixiv_id 69689053 --process getframes

# convert the fetched frames earlier to mp4 with verbose info
python py_ugoira.py --frames_path ./ugoira_69689053 --process convertframes \
    --video_output cute_69689053.mp4 \
    --ffmpeg_path "C:\ffmpeg\ffmpeg.exe" \
    --ffmpeg_args "-c:v libx264 -profile:v baseline -pix_fmt yuv420p -an" \
    --verbose
```


### License

GPLv3
