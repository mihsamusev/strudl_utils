import json
import strudl_config as config
from annotation_interface import AnnotationInterface

if __name__ == "__main__":
    ai = AnnotationInterface(config.api_host)

    with open(config.project_cashe,"r") as infile:
        project_cashe = json.load(infile)

    server2original_video_map = {}

    for k, v in project_cashe["datasets"].items():
        server_videos = ai.get_server_videos(k)
        server2original_video_map[k] = dict(zip(server_videos, v["videos"]))

    # save maps
    with open(config.video_mapping,"w") as outfile:
            json.dump(server2original_video_map, outfile, indent=2)
