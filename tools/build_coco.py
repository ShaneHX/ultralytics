from pathlib import Path


import cv2
import argparse
import json
import numpy as np
import imagesize

#################################################
# Change the classes depend on your own dataset.#
# Don't change the list name 'Classes'          #
#################################################
def create_image_annotation(file_path: str, width: int, height: int, image_id: int):
    image_annotation = {
        "file_name": file_path,
        "height": height,
        "width": width,
        "id": image_id,
    }
    return image_annotation


def create_annotation_from_yolo_format(
    min_x, min_y, width, height, image_id, category_id, annotation_id, segmentation=True
):
    bbox = (float(min_x), float(min_y), float(width), float(height))
    area = width * height
    max_x = min_x + width
    max_y = min_y + height
    if segmentation:
        seg = [[min_x, min_y, max_x, min_y, max_x, max_y, min_x, max_y]]
    else:
        seg = []
    annotation = {
        "id": annotation_id,
        "image_id": image_id,
        "bbox": bbox,
        "area": area,
        "iscrowd": 0,
        "category_id": category_id,
        "segmentation": seg,
    }

    return annotation


# Create the annotations of the ECP dataset (Coco format)
coco_format = {"images": [{}], "categories": [], "annotations": [{}]}
classes = [
    "person",
]


def get_images_info_and_annotations(dataset_dir):
    path = Path(dataset_dir)
    annotations = []
    images_annotations = []
    if path.is_dir():
        file_paths = sorted(path.rglob("*.jpg"))
        file_paths += sorted(path.rglob("*.jpeg"))
        file_paths += sorted(path.rglob("*.png"))
    else:
        with open(path, "r") as fp:
            read_lines = fp.readlines()
        file_paths = [Path(line.replace("\n", "")) for line in read_lines]

    image_id = 0
    annotation_id = 1  # In COCO dataset format, you must start annotation id with '1'

    for file_path in file_paths:
        # Check how many items have progressed
        print("\rProcessing " + str(image_id) + " ...", end='')

        # Build image annotation, known the image's width and height
        w, h = imagesize.get(str(file_path))

        file_path_str = str(file_path).replace(dataset_dir, "")
        image_annotation = create_image_annotation(
            file_path=file_path_str, width=w, height=h, image_id=image_id
        )
        images_annotations.append(image_annotation)

        label_file_name = f"{file_path.stem}.txt"

        annotations_path = file_path.parent.parent /"Annotations"/ label_file_name

        if not annotations_path.exists():
            continue  # The image may not have any applicable annotation txt file.

        with open(str(annotations_path), "r") as label_file:
            label_read_line = label_file.readlines()

        # yolo format - (class_id, x_center, y_center, width, height)
        # coco format - (annotation_id, x_upper_left, y_upper_left, width, height)
        for line1 in label_read_line:
            label_line = line1
            category_id = (
                int(label_line.split()[0]) + 1
            )  # you start with annotation id with '1'
            x_center = float(label_line.split()[1])
            y_center = float(label_line.split()[2])
            width = float(label_line.split()[3])
            height = float(label_line.split()[4])

            float_x_center = w * x_center
            float_y_center = h * y_center
            float_width = w * width
            float_height = h * height

            min_x = int(float_x_center - float_width / 2)
            min_y = int(float_y_center - float_height / 2)
            width = int(float_width)
            height = int(float_height)

            annotation = create_annotation_from_yolo_format(
                min_x,
                min_y,
                width,
                height,
                image_id,
                category_id,
                annotation_id,
            )
            annotations.append(annotation)
            annotation_id += 1

        image_id += 1  # if you finished annotation work, updates the image id.

    return images_annotations, annotations



def get_args():
    parser = argparse.ArgumentParser("Yolo format annotations to COCO dataset format")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Absolute path for 'train.txt' or 'test.txt', or the root dir for images.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Visualize bounding box and print annotation information",
    )
    parser.add_argument(
        "--output",
        default="train_coco.json",
        type=str,
        help="Name the output json file",
    )
    parser.add_argument(
        "--yolo-subdir",
        action="store_true",
        help="Annotations are stored in a subdir not side by side with images.",
    )
    parser.add_argument(
        "--box2seg",
        action="store_true",
        help="Coco segmentation will be populated with a polygon "
        "that matches replicates the bounding box data.",
    )
    args = parser.parse_args()
    return args


def main():

    dataset_dir = "/home/xin/Dataset/person_demo/"

    output_name = "person_coco.json"
    output_path = dataset_dir + output_name
    print("Start!")


    (
        coco_format["images"],
        coco_format["annotations"],
    ) = get_images_info_and_annotations(dataset_dir)

    for index, label in enumerate(classes):
        categories = {
            "supercategory": "Defect",
            "id": index + 1,  # ID starts with '1' .
            "name": label,
        }
        coco_format["categories"].append(categories)

    with open(output_path, "w") as outfile:
        json.dump(coco_format, outfile, indent=4)

    print("Finished!")


if __name__ == "__main__":

    main()