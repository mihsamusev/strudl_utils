import os
import requests
from imutils.paths import list_files

class DatasetInterface:
    def __init__(self, config):
        self.config = config

    def verify_config(self, config):
        pass

    def post_mask(api_host, dataset_name, mask_path):
        files = [('mask_image_file', open(mask_path,'rb'))]
        r = requests.post(url=api_host + "datasets/masks",
        params={"dataset_name": dataset_name}, files=files)

        if r.status_code == 200:
            print("[INFO] status [{}] uploading image mask to '{}' - pass".format(r.status_code, dataset_name))
            return True
        else:
            print("[INFO] status [{}] uploading image mask '{}' - fail".format(r.status_code, dataset_name))
            return False

    def post_dataset(api_host, dataset_name, class_names, class_heights):
        r = requests.post(url=api_host + "datasets",
        params={
            "dataset_name": dataset_name,
            "class_names": ",".join(class_names),
            "class_heights": ','.join(map(str, class_heights))})

        if r.status_code == 200:
            print("[INFO] status [{}] creating dataset '{}' - pass".format(r.status_code, dataset_name))
            return True
        else:
            print("[INFO] status [{}] creating dataset '{}' - fail".format(r.status_code, dataset_name))
            return False

    def post_config(api_host, dataset_name, settings): 
        r = requests.post(url=api_host + "datasets/config",
            params={"dataset_name": dataset_name}, json=settings)

        if r.status_code == 200:
            print("[INFO] status [{}] adding config to '{}' - pass".format(r.status_code, dataset_name))
            return True
        else:
            print("[INFO] status [{}] adding config to '{}' - fail".format(r.status_code, dataset_name))
            return False

    def get_folder_mask(folder, ending="_mask.png"):
        files = next(os.walk(folder))[2]
        for f in files:
            if f.endswith(ending):
                return f

    def post_import_videos(api_host, dataset_name, server_video_path):
        params = {
            "dataset_name": dataset_name,
            "path": server_video_path,
            "method": "handbrake"
        }
        r = requests.post(url=api_host + "jobs/import_videos",
            params=params)

        if r.status_code == 202:
            print("[INFO] status [{}] adding videos to '{}' - pass".format(r.status_code, dataset_name))
            return True
        else:
            print("[INFO] status [{}] adding videos to '{}' - fail".format(r.status_code, dataset_name))
            return False

    def post_prepare_annotation(api_host, dataset_name):
        r = requests.post(url=api_host + "jobs/prepare_annotation",
        params={"dataset_name": dataset_name, "less_night": False})
        if r.status_code == 202:
            print("[INFO] status [{}] extract frames to annotate for '{}' - pass".format(r.status_code, dataset_name))
            return True
        else:
            print("[INFO] status [{}] extract frames to annotate for '{}' - fail".format(r.status_code, dataset_name))
            return False

    def post_point_tracks(api_host, dataset_name, visualize=True):
        r = requests.post(url=api_host + "jobs/point_tracks",
        params={
            "dataset_name": dataset_name,
            "visualize": visualize,
            "overwrite": True})

        if r.status_code == 202:
            print("[INFO] status [{}] generating KLT point tracks for videos in '{}' - pass".format(r.status_code, dataset_name))
            return True
        else:
            print("[INFO] status [{}] generating KLT point tracks for videos in '{}' - fail".format(r.status_code, dataset_name))
            return False

    def response_print(self, r, positive_code=200, task_descr="request"):