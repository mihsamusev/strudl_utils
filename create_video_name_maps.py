import argparse
import os
import json
from annotation_interface import AnnotationInterface

def load(project_path, target):
    try:
        with open(os.path.join(project_path, target),"r") as infile:
            return json.load(infile)
    except:
        return None

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True,
        help="path to project folder with config")
    args = vars(ap.parse_args())

    # load main dataset config and video names
    config = load(args["project"], "strudl_config.json")
    original_video_names = load(args["project"], "video_names.json")

    ai = AnnotationInterface(config["api_host"])

    server2original_video_map = {}

    server_videos = ai.get_server_videos(dataset_name=config["dataset_name"])
    server2original_video_map = dict(zip(server_videos, original_video_names["video_names"]))

    # save maps
    
    with open(os.path.join(args["project"], "server2original_video_mapping.json"),"w") as outfile:
            json.dump(server2original_video_map, outfile, indent=2)
