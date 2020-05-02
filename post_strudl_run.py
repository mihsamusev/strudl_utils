import os
import json
import requests
import argparse


def load(project_path, target):
    try:
        with open(os.path.join(project_path, target),"r") as infile:
            return json.load(infile)
    except:
        return None

def post_run(api_host, dataset_name, run_name, config):
    r = requests.post(url=api_host + "runs/config",
        params={"dataset_name": dataset_name, "run_name": run_name}, json=config)

    if r.status_code == 200:
        print("[INFO] status [{}] creating run for '{}' - pass".format(r.status_code, dataset_name))
        return True
    else:
        print("[INFO] status [{}] creating run for '{}' - fail".format(r.status_code, dataset_name))
        return False

def post_train_detector(api_host, dataset_name, run_name, epochs=70):
    r = requests.post(url=api_host + "jobs/train_detector",
      params={"dataset_name": dataset_name, "run_name": run_name,
        "epochs":epochs})

    if r.status_code == 202:
        print("[INFO] status [{}] starting to train on '{}' - pass".format(r.status_code, dataset_name))
        return True
    else:
        print("[INFO] status [{}] starting to train on '{}' - fail".format(r.status_code, dataset_name))
        return False

def post_detect_objects(api_host, dataset_name, run_name):
    r = requests.post(url=api_host + "jobs/detect_objects",
      params={"dataset_name": dataset_name, "run_name": run_name})

    if r.status_code == 202:
        print("[INFO] status [{}] detecting objects '{}' - pass".format(r.status_code, dataset_name))
        return True
    else:
        print("[INFO] status [{}] detecting objects '{}' - fail".format(r.status_code, dataset_name))
        return False

def post_visualize_detections(api_host, dataset_name, run_name, coords="pixels"):
    r = requests.post(url=api_host + "jobs/visualize_detections",
      params={"dataset_name": dataset_name, "run_name": run_name, "coords": coords})

    if r.status_code == 202:
        print("[INFO] status [{}] creating visualization '{}' - pass".format(r.status_code, dataset_name))
        return True
    else:
        print("[INFO] status [{}] creating visualization '{}' - fail".format(r.status_code, dataset_name))
        return False

def post_detection_to_world(api_host, dataset_name, run_name, make_videos=True):
    r = requests.post(url=api_host + "jobs/detections_to_world_coordinates",
        params={"dataset_name": dataset_name,"run_name": run_name, "make_videos": make_videos})

    if r.status_code == 202:
        print("[INFO] status [{}] detections to world coordinates '{}' - pass".format(r.status_code, dataset_name))
        return True
    else:
        print("[INFO] status [{}] detections to world coordinates '{}' - fail".format(r.status_code, dataset_name))
        return False

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--project", required=True,
        help="path to project folder with config")
    args = vars(ap.parse_args())

    config = load(args["project"], "strudl_config.json")

    settings = {
        "confidence_threshold": 0.6,
        "detection_batch_size": 64,
        "detection_training_batch_size": 32,
        "detector_resolution": "(320,240,3)"
    }

    run_name = "run3"
    #post_run(config["api_host"], config["dataset_name"], run_name, config=settings)
    #post_train_detector(config["api_host"], config["dataset_name"], run_name, epochs=70)

    #post_detect_objects(config["api_host"], config["dataset_name"], run_name)
    #post_visualize_detections(config["api_host"], config["dataset_name"], run_name)

    post_detection_to_world(config["api_host"], config["dataset_name"], run_name, make_videos=True)

    