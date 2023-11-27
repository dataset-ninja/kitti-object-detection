# https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d

import os
import numpy as np
import supervisely as sly
from supervisely.io.fs import (
    get_file_name_with_ext,
    get_file_name,
    get_file_ext,
    file_exists,
    get_file_size,
)
from dotenv import load_dotenv

import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
import shutil

from tqdm import tqdm


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_nam]e = "KITTI object detection"
    train_images_path = "/home/grokhi/rawdata/KITTI/training/image_2"
    test_images_path = "/home/grokhi/rawdata/KITTI/testing/image_2"
    anns_path = "/home/grokhi/rawdata/KITTI/training/label_2"
    batch_size = 30
    images_ext = ".png"
    ann_ext = ".txt"

    ds_name_to_data = {"train": (train_images_path, anns_path), "test": (test_images_path, None)}

    test = []

    def create_ann(image_path):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        ann_path = os.path.join(bboxes_path, get_file_name(image_path) + ann_ext)

        if file_exists(ann_path):
            with open(ann_path) as f:
                content = f.read().split("\n")

                for curr_data in content:
                    if len(curr_data) != 0:
                        class_name = curr_data.split(" ")[0]
                        coords = list(map(float, curr_data.split(" ")[4:8]))
                        obj_class = name_to_class[class_name]

                        occlusion_value = idx_to_occlusion[int(curr_data.split(" ")[2])]
                        occlusion = sly.Tag(occlusion_meta, value=occlusion_value)

                        angle_value = float(curr_data.split(" ")[3])
                        angle = sly.Tag(angle_meta, value=angle_value)

                        dimensions_value = " ".join(curr_data.split(" ")[8:11])
                        dimensions = sly.Tag(dimensions_meta, value=dimensions_value)

                        location_value = " ".join(curr_data.split(" ")[11:14])
                        location = sly.Tag(location_meta, value=location_value)

                        rotation_value = float(curr_data.split(" ")[14])
                        rotation = sly.Tag(rotation_meta, value=rotation_value)

                        left = coords[0]
                        right = coords[2]
                        top = coords[1]
                        bottom = coords[3]
                        rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
                        label = sly.Label(
                            rectangle,
                            obj_class,
                            tags=[occlusion, angle, dimensions, location, rotation],
                        )
                        labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    car = sly.ObjClass("car", sly.Rectangle)
    dontcare = sly.ObjClass("dont care", sly.Rectangle)
    truck = sly.ObjClass("truck", sly.Rectangle)
    van = sly.ObjClass("van", sly.Rectangle)
    pedestrian = sly.ObjClass("pedestrian", sly.Rectangle)
    misc = sly.ObjClass("misc", sly.Rectangle)
    cyclist = sly.ObjClass("cyclist", sly.Rectangle)
    sitting = sly.ObjClass("person sitting", sly.Rectangle)
    tram = sly.ObjClass("tram", sly.Rectangle)

    name_to_class = {
        "Car": car,
        "DontCare": dontcare,
        "Truck": truck,
        "Van": van,
        "Pedestrian": pedestrian,
        "Misc": misc,
        "Cyclist": cyclist,
        "Person_sitting": sitting,
        "Tram": tram,
    }

    occlusion_meta = sly.TagMeta("occlusion state", sly.TagValueType.ANY_STRING)
    angle_meta = sly.TagMeta("observation angle", sly.TagValueType.ANY_NUMBER)
    dimensions_meta = sly.TagMeta("dimensions", sly.TagValueType.ANY_STRING)
    location_meta = sly.TagMeta("location", sly.TagValueType.ANY_STRING)
    rotation_meta = sly.TagMeta("rotation y", sly.TagValueType.ANY_NUMBER)

    idx_to_occlusion = {
        0: "fully visible",
        1: "partly occluded",
        2: "largely occluded",
        3: "unknown",
        -1: "unknown",
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=list(name_to_class.values()),
        tag_metas=[occlusion_meta, angle_meta, dimensions_meta, location_meta, rotation_meta],
    )
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, ds_data in ds_name_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_path, bboxes_path = ds_data

        images_names = os.listdir(images_path)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = [
                os.path.join(images_path, image_name) for image_name in images_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            if bboxes_path is not None:
                anns = [create_ann(image_path) for image_path in img_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))
    return project
