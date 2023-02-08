import pathlib as plb
import shutil
from loguru import logger
import tqdm

data_root = plb.Path("/export/fast-1/Datasets/ped/app_val")



for label_path in data_root.rglob("**/Annotations/"):
    label_generator = label_path.rglob("*.txt")

    temp_label_path = plb.Path("~/temp")
    if not label_path.is_dir():
        logger.error("fail to load label from {}".format(label_path))
        exit()

    if not temp_label_path.is_dir():
        temp_label_path.mkdir(parents=True)


    def clamp(target, min_v, max_v):
        if target < min_v:
            return min_v
        elif target > max_v:
            return max_v
        else:
            return target

    for s_label in tqdm.tqdm(label_generator):
        new_label_info_list = list()
        with open(str(s_label), 'r') as f:
            label_list = f.readlines()

            for s_label_info in label_list:
                s_label_info_splited = s_label_info.split(" ")
                if len(s_label_info_splited) != 5:
                    continue
                new_label_info_list.append("{} {:.4} {:.4} {:.4} {:.4}\n".format(0,
                                                                   clamp(float(s_label_info_splited[1]), 0, 1.0),
                                                                   clamp(float(s_label_info_splited[2]), 0, 1.0),
                                                                   clamp(float(s_label_info_splited[3]), 0, 1.0),
                                                                   clamp(float(s_label_info_splited[4]), 0, 1.0)))
        if len(new_label_info_list) > 0:
            new_label_file = str(temp_label_path / s_label.name)

            with open(new_label_file, 'w') as f:
                f.writelines(new_label_info_list)


    new_label_generator = temp_label_path.rglob("*.txt")

    for s_new_label in new_label_generator:
        replace_path = label_path / s_new_label.name
        shutil.move(str(s_new_label), str(replace_path))

    shutil.rmtree(str(temp_label_path))
