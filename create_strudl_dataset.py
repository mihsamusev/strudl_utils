import os
import subprocess
import json
import requests
import strudl_config as config
from imutils.paths import list_files

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

def get_metadata(video_file):
    p = subprocess.Popen(["ffprobe", "-v", "quiet","-print_format", "json", "-show_format",
        "-show_streams", video_file, ">", "metadata.json"],shell=True)
    p.wait()

    with open("metadata.json","r") as f:
        video_settings = json.load(f)

    avg_fps = int(video_settings["streams"][0]["avg_frame_rate"][:-2])
    resolution = (video_settings["streams"][0]["width"], video_settings["streams"][0]["height"])

    os.remove("metadata.json")
    return avg_fps, resolution

def post_config(api_host, dataset_name, settings): 
    r = requests.post(url=api_host + "datasets/config",
        params={"dataset_name": dataset_name}, json=settings)

    if r.status_code == 200:
        print("[INFO] status [{}] adding config to '{}' - pass".format(r.status_code, dataset_name))
        return True
    else:
        print("[INFO] status [{}] adding config to '{}' - fail".format(r.status_code, dataset_name))
        return False

def get_common_metadata(video_files):
    fps_list = []
    res_list = []
    for video in video_files:
        fps, res = get_metadata(video)
        fps_list.append(fps)
        res_list.append(res)

    if (len(set(fps_list)) != 1) or (len(set(res_list)) != 1):
        return None
    else:
        return fps, res

def get_folder_videos(folder):
    VALID_EXTENSIONS = (".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv",".webm")
    return list(list_files(folder, validExts=VALID_EXTENSIONS))

def get_folder_mask(folder, ending="_mask.png"):
    files = next(os.walk(folder))[2]
    for f in files:
        if f.endswith(ending):
            return f

def print_info(message):
    print("[INFO] {}".format(message))

def videos_already_imported(api_host, dataset_name, video_names):
    r = requests.get(api_host + "videos", params={"dataset_name": dataset_name})
    
    video_names = [os.path.basename(v).rsplit(".", 1)[0] for v in dataset_videos]
    if r.status_code == 404:
        return [False for v in video_names]
    else:
        imported_videos = r.json()
        return [True if v in imported_videos else False for v in video_names]

# jobs

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

if __name__ == "__main__":
    dataset_names = next(os.walk(config.datasets_pc_path))[1]

    try:
        with open(config.project_cashe,"r") as infile:
            project_cashe = json.load(infile)
    except:
        project_cashe = {}
        project_cashe["datasets"] = {}
        for d in dataset_names:
            project_cashe["datasets"][d] = {}

    # get paths

    for dataset_name in dataset_names:
        # this folder
        dataset_path = os.path.join(config.datasets_pc_path, dataset_name)
        # dataset init
        post_dataset(config.api_host, dataset_name, config.class_names, config.class_heights)
        project_cashe["datasets"][dataset_name]["class_names"] = config.class_names
        project_cashe["datasets"][dataset_name]["class_heights"] = config.class_heights

        # config
        dataset_videos = get_folder_videos(dataset_path)
        fps, res = get_common_metadata(dataset_videos)
        settings = {
            "annotation_train_split": config.train_test_split,
            "images_to_annotate": config.annotate_total,
            "images_to_annotate_per_video": config.annotate_per_video,
            "point_track_resolution": "(320,240)",
            "video_fps": fps,
            "video_resolution": "({},{},3)".format(res[0], res[1])
        }
        post_config(config.api_host, dataset_name, settings)
        project_cashe["datasets"][dataset_name]["config"] = settings

        #mask
        mask_path = get_folder_mask(dataset_path, ending="_mask.png")
        mask_path = os.path.join(dataset_path, mask_path)
        post_mask(config.api_host, dataset_name, mask_path)
        project_cashe["datasets"][dataset_name]["mask"] = mask_path

        #POST videos if have not posted yet
        if "videos" not in project_cashe["datasets"][dataset_name].keys():
            video_format = [os.path.basename(v).rsplit(".", 1)[1] for v in dataset_videos]
            server_video_path = config.datasets_server_path + dataset_name + "/*." + video_format[0]
            post_import_videos(config.api_host, dataset_name, server_video_path)
            project_cashe["datasets"][dataset_name]["videos"] = [os.path.basename(v).rsplit(".", 1)[0] for v in dataset_videos]

        # extract images for annotations
        post_prepare_annotation(config.api_host, dataset_name)

        # calculate point tracks if not done before
        if "point_tracks" not in project_cashe["datasets"][dataset_name].keys():
            post_point_tracks(config.api_host, dataset_name, visualize=True)
            project_cashe["datasets"][dataset_name]["videos"] = True

    # save cashe
    with open(config.project_cashe,"w") as outfile:
        json.dump(project_cashe, outfile, indent=2)





