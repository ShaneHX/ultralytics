import pathlib as plb
import random
import shutil

import tqdm
from loguru import logger
import os
data_root = plb.Path("/export/fast-1/Datasets/ped/app")



for s_file in tqdm.tqdm(data_root.rglob("*.jpg")):
    
    s_label_file = str(s_file).replace("Images", "Annotations")
    s_label_file = s_label_file.replace(".jpg", ".txt")
    # print(s_label_file)
    if not plb.Path(s_label_file).is_file():
        logger.warning("{} is not found".format(s_label_file))
        os.remove(str(s_file))
    # s_new_lable = data_root / "choosed" / s_file.name
    # s_new_img = data_root / "choosed" / s_img_file.name

    # shutil.move(s_file, s_new_lable)
    # shutil.move(s_img_file, s_new_img)
    # os.system("rm -rf {}".format(s_file.parent))