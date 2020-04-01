import subprocess
import re
import json
import dateutil.parser as dp
import os
import errno
from math import log10, floor
from datetime import datetime, timedelta
from imutils.paths import list_files
import xml.etree.ElementTree as et

def get_staring_time(video_file):
    xml_name = video_file.rsplit(".", 1)[0] + ".xml"
    tree = et.parse(xml_name)
    root = tree.getroot()
    timestr = root.findall("StartTime")[0].text
    creation_time = dp.parse(timestr)
    return creation_time

def read_config(config):
    tree = et.parse(xml_name)
    root = tree.getroot()
    fps = float(root.findall("Framerate")[0].text)

def get_metadata(video_file):
    p = subprocess.Popen(["ffprobe", "-v", "quiet","-print_format", "json", "-show_format",
        "-show_streams", "-count_frames", video_file, ">", "metadata.json"],shell=True)
    p.wait()

    with open("metadata.json","r") as f:
        video_settings = json.load(f)
    
    avg_fps = int(video_settings["streams"][0]["avg_frame_rate"][:-2])
    n_frames = int(video_settings["streams"][0]["nb_read_frames"])

    # check .xml with creation time file exists
    xml_name = video_file.rsplit(".", 1)[0] + ".xml"
    if os.path.exists(xml_name):
        creation_time = get_staring_time(video_file)
    else:
        timestr = video_settings["format"]["tags"]["creation_time"]
        creation_time = dp.parse(timestr)

    os.remove("metadata.json")
    return avg_fps, n_frames, creation_time

def get_timestrings(start_time, fps, n_frames, padding_size=5):
    timestrings = []

    for i in range(n_frames):
        step = i / fps
        frame_num_string = str(i).zfill(padding_size)
        frame_time = start_time + timedelta(seconds=step)
        frame_time_string = frame_time.strftime("%Y %m %d %H:%M:%S.%f")[:-3]
        string = "{} {}".format(frame_num_string, frame_time_string)
        timestrings.append(string)

    return timestrings

if __name__ == "__main__": 
    import argparse
    ag = argparse.ArgumentParser()
    ag.add_argument("-p", "--path", required=True,
        help="path to input video file or folder containing videos")
    ag.add_argument("-c", "--config", default=None,
        help="Get global config file")
    args = vars(ag.parse_args())

    if not os.path.exists(args["path"]):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)
    
    VALID_EXTENSIONS = (".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv",".webm")

    # check if input is a video or a path
    if os.path.isfile(args["path"]):
        path_ext = "." + args["path"].rsplit(".", 1)[1].lower()
        if not path_ext in VALID_EXTENSIONS:
            raise ValueError("wrong extension", path_ext)

        videoPaths = [args["path"]]
    else:
        videoPaths = list(list_files(args["path"], validExts=VALID_EXTENSIONS))
    nVideos = len(videoPaths)

    # PROCESSING
    for i, videoPath in enumerate(videoPaths):
        print("[INFO] Working on video {}/{} - {}".format(i + 1, nVideos, videoPath))
        
        avg_fps, n_frames, start_time = get_metadata(videoPath)
        
        #print("[INFO]   Generating log...")
        timestrings = get_timestrings(start_time, avg_fps, n_frames)

        # write lines to file
        log_path = videoPath.rsplit(".", 1)[0] + ".log"
        with open(log_path,"w") as f:
            for line in timestrings:
                f.write("{}\n".format(line))