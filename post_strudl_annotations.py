import os
import json
import argparse
from copy import copy
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

    # load main dataset config
    config = load(args["project"], "strudl_config.json")
    ai = AnnotationInterface(config["api_host"])

    annotations = load(args["project"], "annotations.json")["annotations"]

    server2original_video_map = load(args["project"], "server2original_video_mapping.json")
    original2server_video_map = {v: k for k, v in server2original_video_map.items()}

    for a in annotations:
        server_video_name = original2server_video_map[a["video_name"]]
        ai.post_annotation(anno_json=a["annotation"], dataset_name=config["dataset_name"],
        video_name=server_video_name, image_number=int(a["id"]))