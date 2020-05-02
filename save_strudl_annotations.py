import json
import argparse
import os
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
    video_names = load(args["project"], "video_names.json")["video_names"]
    server2original_video_map = load(args["project"], "server2original_video_mapping.json")

    ai = AnnotationInterface(config["api_host"])
    annotations = ai.get_all_annotation_data(dataset_name=config["dataset_name"])

    # remap hashed names to original names
    for a in annotations:
        a["video_name"] = server2original_video_map[a["video_name"]]

    with open(os.path.join(args["project"], "annotations.json"),"w") as outfile:
        json.dump({"annotations": annotations}, outfile, indent=2)

