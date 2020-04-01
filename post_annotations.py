import json
from copy import copy
import strudl_config as config
from annotation_interface import AnnotationInterface

if __name__ == "__main__":
    ai = AnnotationInterface(config.api_host)

    # load cashe and mapping files
    with open(config.project_cashe,"r") as infile:
        project_cashe = json.load(infile)

    with open(config.project_annotations,"r") as infile:
        project_annotations = json.load(infile)

    with open(config.video_mapping,"r") as infile:
        server2original_video_map = json.load(infile)
    original2server_video_map = copy(server2original_video_map)
    for k, videos in original2server_video_map.items():
        original2server_video_map[k] = dict((v, k) for k, v in videos.items())

    # loop over project datasets
    for k, v in project_cashe["datasets"].items():
        for a in project_annotations[k]:
            server_video_name = original2server_video_map[k][a["video_name"]]
            ai.post_annotation(anno_json=a["annotation"], dataset_name=k,
            video_name=server_video_name,image_number=int(a["id"]))