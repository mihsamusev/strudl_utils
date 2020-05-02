import os
import json
import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True,
        help="path to project folder with config")
    args = vars(ap.parse_args())

    # create folder
    if not os.path.exists(args["folder"]):
        os.makedirs(args["folder"])
    else:
        raise ValueError("Folder already exists",args["folder"])

    example_config = {
        "api_host": "http://192.168.137.124/",
        "dataset_name": "test_set_1",
        "server_path": "/usb/KINGSTON/strudl/datasets/rgb_night",
        "annotation":{
            "split": 1.0,
            "total": 500,
            "per_video": 100
        },
        "class":{
            "names": ["car","bus","truck","other"],
            "heights": [1.5, 3, 3, 2]
        },
        "video":{
            "format": "mkv",
            "fps": 25,
            "width": 1024,
            "height": 640
        }
    }

    with open(os.path.join(args["folder"], "strudl_config.json"),"w") as outfile:
        json.dump(example_config, outfile, indent=2)