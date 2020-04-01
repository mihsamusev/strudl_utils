import os
import json
import requests
import argparse
from imutils.paths import list_files
from dataset_interface import DatasetInterface
        code_check = r.status_code == positive_code
        result = "pass" if code_check else "fail"
        print("[INFO] status [{}] {} - {}".format(r.status_code, task_descr, result))
        return code_check

def load(project_path, target):
    try:
        with open(os.path.join(project_path, target),"r") as infile:
            return json.load(infile)
    except:
        return None

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "project", required=True,
        help="path to project folder with config")
    args = vars(ap.parse_args())

    # load main dataset config
    config = load(args["project"], "strudl_config.json")
    di = DatasetInterface(config)

    # load cache
    project_cashe = load(args["project"], "strudl_cashe.json")
    if project_cashe is None:
        project_cashe = {}
    
    # START POSTING
    # /datasets/post
    res = di.post_dataset(config["api_host"], config["dataset_name"],
        config["class"]["names"], config["class"]["names"])
    project_cashe["/datasets"] = res

    # /dataset/masks/post
    mask_name = get_folder_mask(args["dataset"], ending="_mask.png")
    mask_path = os.path.join(args["dataset"], mask_name)
    res = post_mask(config["api_host"], config["dataset_name"], mask_path)
    project_cashe["/dataset/masks"] = res

    # /datasets/config/post
    settings = {
        "annotation_train_split": config["annotation"]["split"],
        "images_to_annotate": config["annotation"]["total"],
        "images_to_annotate_per_video": config["annotation"]["per_video"],
        "point_track_resolution": "(320,240)",
        "video_fps": config["video"]["fps"],
        "video_resolution": "({},{},3)".format(
            config["video"]["width"], config["video"]["height"])
    }
    res = post_config(config["api_host"], config["dataset_name"], settings)
    project_cashe["/datasets/config"] = res

    #/jobs/import_videos
    if "/jobs/import_videos" not in project_cashe.keys():
        server_video_paths = config["server_path"] + config["dataset_name"] + "/*." + config["video"]["format"]
        res = post_import_videos(config["api_host"], config["dataset_name"], server_video_paths)
        project_cashe["/jobs/import_videos"] = res

    # /jobs/prepare_annotation
    res = post_prepare_annotation(config["api_host"], config["dataset_name"])
    project_cashe["/jobs/prepare_annotation"] = res

    # /runs/point_tracks
    if "/runs/point_tracks" not in project_cashe.keys():
        res = post_point_tracks(config["api_host"], config["dataset_name"], visualize=True)
        project_cashe["/runs/point_tracks"] = res

    # save cashe
    with open(config.project_cashe,"w") as outfile:
        json.dump(project_cashe, outfile, indent=2)