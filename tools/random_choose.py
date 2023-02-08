
import pathlib as plb
import random
import shutil

import tqdm
from loguru import logger
kChooseNum = 30000

data_root = plb.Path("/datatmp/Datasets/ped/train/GTAV_visDrone/")

label_files = (data_root / "Annotations").rglob("*.txt")
img_path = (data_root / "Images")
new_dir = data_root / "choosed"

if not new_dir.is_dir():
    new_dir.mkdir(parents=True)

label_files_list = list(label_files)
num_items = len(label_files_list)
print(num_items)

choosed_file_idx = random.sample(range(num_items), kChooseNum)

for s_idx in tqdm.tqdm(choosed_file_idx):
    s_label_file = label_files_list[s_idx]
    s_img_file = img_path / (s_label_file.stem + ".jpg")
    if not s_img_file.is_file():
        logger.warning("{} is not found".format(s_img_file))
        continue
    s_new_lable = new_dir / s_label_file.name
    s_new_img = new_dir / s_img_file.name

    shutil.move(s_label_file, s_new_lable)
    shutil.move(s_img_file, s_new_img)
