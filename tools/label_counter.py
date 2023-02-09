import pathlib as plb
import tqdm
import cv2

dataset_dir = "/media/xin/XHLibrary/000-Dataset/Apex/Labeled/Apex0516"


kReviewCls = []

dataset_path = plb.Path(dataset_dir)

label_file_generator = dataset_path.rglob("*.txt")

label_list = list(label_file_generator)


counter_dict = dict()

def draw_bbox(img, bbox, label="", color=(128, 128, 128), txt_color=(255, 255, 255)):
    lw = 1
    p1, p2 = (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3]))
    cv2.rectangle(img, p1, p2, color, thickness=lw, lineType=cv2.LINE_AA)
    if label:
        tf = max(lw - 1, 1)  # font thickness
        w, h = cv2.getTextSize(label, 0, fontScale=lw / 3, thickness=tf)[0]  # text width, height
        outside = p1[1] - h >= 3
        p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
        cv2.rectangle(img, p1, p2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img,
                    label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                    0,
                    lw / 3,
                    txt_color,
                    thickness=tf,
                    lineType=cv2.LINE_AA)

for s_label_file in tqdm.tqdm(label_list):
    review_label_list = []
    with open(s_label_file, 'r') as f:
        label_lines = f.readlines()
        for s_line in label_lines:
            s_bbox_split = s_line.split(" ")
            if len(s_bbox_split) < 5:
                continue
            cls = int(s_bbox_split[0])
            if cls in counter_dict.keys():
                counter_dict[cls] += 1
            else:
                counter_dict[cls] = 1
            if cls in kReviewCls:
                review_label_list.append(s_bbox_split)
    if len(review_label_list) > 0:
        img_file = str(s_label_file).replace(".txt", ".jpg")
        if plb.Path(img_file).is_file():
            img = cv2.imread(img_file)
            img_w = img.shape[1]
            img_h = img.shape[0]
            for s_label_str in review_label_list:
                cls = int(s_label_str[0])
                bbox_x = float(s_label_str[1]) * img_w
                bbox_y = float(s_label_str[2]) * img_h
                bbox_w = float(s_label_str[3]) * img_w
                bbox_h = float(s_label_str[4]) * img_h
                draw_bbox(img, (bbox_x-bbox_w/2, bbox_y-bbox_h/2, bbox_x + bbox_w/2, bbox_y+bbox_h/2), str(cls) )
            cv2.imshow("ttt", img)
            cv2.waitKey()



print(counter_dict)
