import requests

class AnnotationInterface():
    def __init__(self, api_host):
        self.api_host = api_host

    def ip_verify(self, ip):
        pass

    def response_print(self, r, positive_code=200, task_descr="request"):
        code_check = r.status_code == positive_code
        result = "pass" if code_check else "fail"
        print("[INFO] status [{}] {} - {}".format(r.status_code, task_descr, result))
        return code_check

    def get_server_videos(self, dataset_name):
        params = {
            "dataset_name": dataset_name
        }
        r = requests.get(url=self.api_host + "videos",
            params=params)
        if self.response_print(r, 200, "getting videos"):
            return r.json()

    def get_annotated_images(self, dataset_name, annotation_set="train"):
        params = {
            "dataset_name": dataset_name,
            "annotation_set": annotation_set
        }
        r = requests.get(url=self.api_host + "annotate/images",
            params=params)
        if self.response_print(r, 200, "getting annotated images from {}".format(dataset_name)):
            return r.json()

    def get_annotation_data(self, dataset_name, image_number, video_name,
        annotation_set="train", accept_auto=False):
        params = {
            "dataset_name": dataset_name,
            "image_number": image_number,
            "video_name": video_name,
            "annotation_set": annotation_set,
            "accept_auto": accept_auto,
            "output_format": "json"
        }

        r = requests.get(url=self.api_host + "annotate/annotation",
            params=params)
        if self.response_print(r, 200,
            "getting annotation data from dataset: {}; video: {}; image: {}".format(
                dataset_name, video_name, image_number)):
            return r.json()
        else:
            return {}

    def get_all_annotation_data(self, dataset_name, annotation_set="train", accept_auto=False):
        dict_heads = ["video_name", "id", "status"]
        data = []
        for image_data in self.get_annotated_images(dataset_name):
            # only save annotate images
            if image_data[2] == "already_annotated":
                annotation_data = dict(zip(dict_heads, image_data))
                annotation_data["annotation"] = self.get_annotation_data(dataset_name=dataset_name,
                    image_number=int(image_data[1]), video_name=image_data[0])
                data.append(annotation_data)
        return data

    def json_to_plain_annotation(self, j):
        s = "{:<2d}{:<8.5f}{:<8.5f}{:<8.5f}{:<8.5f}px:{:<7.5f},{:<7.5f},{:<7.5f},{:<8.5f}py:{:<7.5f},{:<7.5f},{:<7.5f},{:<8.5f}{}".format(
            j["class_id"],
            j["center_x"],
            j["center_y"],
            j["width"],
            j["height"],
            j["px"][0],
            j["px"][1],
            j["px"][2],
            j["px"][3],
            j["py"][0],
            j["py"][1],
            j["py"][2],
            j["py"][3],
            j["class_name"]
        )
        return s

    def post_annotation(self, anno_json, dataset_name, image_number, video_name,
        annotation_set="train"):
        params = {
            "dataset_name": dataset_name,
            "image_number": image_number,
            "video_name": video_name,
            "annotation_set": annotation_set
        }
        anno_strings = [self.json_to_plain_annotation(a) for a in anno_json]
        payload="\n".join(anno_strings) + "\n"
        r = requests.post(url=self.api_host + "annotate/annotation",
            params=params, data=payload)
        self.response_print(r, 200,"posting annotation data: {}; video: {}; image: {}".format(
                dataset_name, video_name, image_number))

    def post_all_saved_annotations(self, original2server_map):
        pass