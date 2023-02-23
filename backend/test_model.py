import glob

import utils_draw_polygons
from config import (
    DEVICE, NUM_CLASSES, TEST_DIR,
    IMAGE_SIZE, BEST_MODEL_DIR, PREDICTION_DIR
)
import random
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import numpy as np
import cv2
import torchvision.models.segmentation
import torch


def analyse_image(image_name):
    test_images = glob.glob(f"{TEST_DIR}/{image_name}")
    print(f"Test instances: {len(test_images)}")

    model = torchvision.models.detection.maskrcnn_resnet50_fpn(
        pretrained=True)  # load an instance segmentation model pre-trained on COCO
    in_features = model.roi_heads.box_predictor.cls_score.in_features  # get number of input features for the classifier
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features,
                                                      NUM_CLASSES)  # replace the pre-trained head with a new one
    model.load_state_dict(torch.load(BEST_MODEL_DIR, map_location=torch.device('cpu')))
    model.to(DEVICE)  # move model to the right device
    model.eval()
    polygon_list = []
    for i in range(len(test_images)):

        image_name = test_images[i].split('/')[-1].split('.')[0]
        image_name = image_name.split('/')[-1]
        image = cv2.imread(test_images[i])
        orig_image = image.copy()
        images = cv2.resize(orig_image, IMAGE_SIZE, cv2.INTER_LINEAR)
        images = torch.as_tensor(images, dtype=torch.float32).unsqueeze(0)
        images = images.swapaxes(1, 3).swapaxes(2, 3)
        images = list(image.to(DEVICE) for image in images)

        with torch.no_grad():
            pred = model(images)

        im = images[0].swapaxes(0, 2).swapaxes(0, 1).detach().cpu().numpy().astype(np.uint8)
        im2 = im.copy()
        im3 = im.copy()
        im4 = im.copy()
        scr = 0
        pred_count = 5

        for i in range(len(pred[0]['masks'])):
            msk = pred[0]['masks'][i, 0].detach().cpu().numpy()
            msk[msk >= 0.65] = 1
            msk[msk < 0.65] = 0
            scr = pred[0]['scores'][i].detach().cpu().numpy()
            if scr > 0.65:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)

                polygons, polygons2 = utils_draw_polygons.mask_to_polygons(msk)
                msk2 = utils_draw_polygons.polygons_to_mask(polygons)
                msk3 = utils_draw_polygons.polygons_to_mask_fill(polygons)
                msk4 = utils_draw_polygons.polygons_to_mask_thick(polygons)
                polygon_list.append([utils_draw_polygons.rgb_to_hex((r,g,b)),polygons2])
                #polygon_list[utils_draw_polygons.rgb_to_hex((r,g,b))]= polygons2

                im2[:, :, 0][msk2 > 0.5] = b
                im2[:, :, 1][msk2 > 0.5] = g
                im2[:, :, 2][msk2 > 0.5] = r

                im3[:, :, 0][msk3 > 0.5] = b
                im3[:, :, 1][msk3 > 0.5] = g
                im3[:, :, 2][msk3 > 0.5] = r

                im4[:, :, 0][msk4 > 0.5] = b
                im4[:, :, 1][msk4 > 0.5] = g
                im4[:, :, 2][msk4 > 0.5] = r
                pred_count = pred_count + 1

        im2 = cv2.resize(im2, (orig_image.shape[-2], orig_image.shape[-3]), cv2.INTER_NEAREST_EXACT)
        cv2.imwrite(PREDICTION_DIR + "/" + image_name + ".png", im2)

        im3 = cv2.resize(im3, (orig_image.shape[-2], orig_image.shape[-3]), cv2.INTER_NEAREST_EXACT)
        cv2.imwrite(PREDICTION_DIR + "/filled_" + image_name + ".png", im3)

        im4 = cv2.resize(im4, (orig_image.shape[-2], orig_image.shape[-3]), cv2.INTER_NEAREST_EXACT)
        cv2.imwrite(PREDICTION_DIR + "/thick_" + image_name + ".png", im4)

        f = open(PREDICTION_DIR + "/" + image_name + ".json", "w")
        f.write(str(polygon_list).replace("\'", "\""))
        f.close()

        return polygon_list


if __name__ == "__main__":
    analyse_image("field.png")