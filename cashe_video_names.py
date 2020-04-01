import argparse
from imutils.paths import list_files
import json
import os

def get_folder_videos(folder):
    VALID_EXTENSIONS = (".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv",".webm")
    return list(list_files(folder, validExts=VALID_EXTENSIONS))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d","--dataset", required=True,
        help="path to dataset folder")
    ap.add_argument("-o","--output", default="",
        help="path to dataset folder")
    args = vars(ap.parse_args())

    dataset_videos = get_folder_videos(args["dataset"])
    video_names = [os.path.basename(v).rsplit(".", 1)[0] for v in dataset_videos]
    with open(os.path.join(args["output"], "video_names.json"),"w") as outfile:
        json.dump({"video_names": video_names}, outfile, indent=2)