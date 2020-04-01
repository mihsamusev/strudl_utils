import json
import strudl_config as config
from annotation_interface import AnnotationInterface

if __name__ == "__main__":
    ai = AnnotationInterface(config.api_host)

    # load cashe and mapping files
    with open(config.project_cashe,"r") as infile:
        project_cashe = json.load(infile)

    with open(config.video_mapping,"r") as infile:
        server2original_video_map = json.load(infile)

    # loop over the project datasets
    project_annotations = {}
    for k, v in project_cashe["datasets"].items():
        dataset_annotations = ai.get_all_annotation_data(k)
        project_annotations[k] = dataset_annotations

        # remap hashed names to original names
        for d in project_annotations[k]:
            d["video_name"] = server2original_video_map[k][d["video_name"]]

    with open(config.project_annotations,"w") as outfile:
        json.dump(project_annotations, outfile, indent=2)
