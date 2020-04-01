import os

# server and file locations
api_host = "http://192.168.137.124/"
datasets_pc_path = [
    "C:/Users/msa/Documents/strudl transfer learning/datasets/rgb",
    "C:/Users/msa/Documents/strudl transfer learning/datasets/rgb_night"]

dateset_names = [
    "test_set1",
    "test_set2"]

datasets_server_path = [
    "/usb/KINGSTON/strudl/datasets/rgb",
    "/usb/KINGSTON/strudl/datasets/rgb_night"]

# video info
video_format = "mkv"
video_fps = 25
video_resolution = (640, 480)

# annotation
train_test_split = 1
annotate_total = 500
annotate_per_video = 100

# detector properties
class_names = ["car","bus","truck","other"]
class_heights = [1.5, 3, 3, 2]

project_folder = "./test_project"
project_cashe = os.path.join(project_folder, "strudl_cashe.json")
video_mapping = os.path.join(project_folder, "server2original_video_mapping.json")
project_annotations = os.path.join(project_folder, "project_annotations.json")

