# -*- coding: utf-8 -*-
# @Time    : 2022/9/20 23:28
# @Author  : Kenny Zhou
# @FileName: visualization.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import albumentations as A
from albumentations.augmentations.functional import adjust_hue_torchvision
from PIL import Image
import numpy as np
import os
from pathlib import Path


def unit_augmentation_factor(path,factor):
    # transform = A.Compose([
    #     A.ColorJitter(p=1,always_apply=True,hue=0.2),
    # ])

    pillow_image = Image.open(path)
    image = np.array(pillow_image)
    # transformed = transform(image=image)
    # transformed_image = transformed["image"]

    return adjust_hue_torchvision(image,factor)

def unit_augmentation(path):
    transform = A.Compose([
        A.ColorJitter(brightness=0.2, contrast=0.15, saturation=0.2, hue=0.05, always_apply=False, p=0.8),
    ])

    pillow_image = Image.open(path)
    image = np.array(pillow_image)
    transformed = transform(image=image)
    transformed_image = transformed["image"]

    return transformed_image


if __name__ == "__main__":

    # base_factor = 0.1
    path = Path("/Users/kennymccormick/Downloads/下午/JiTest/SRC_20220920-105923-312.jpg")
    save_path = Path("/Users/kennymccormick/Downloads/下午/augmentation")
    # out_dir = save_path / str(path.stem)
    # os.mkdir(out_dir)
    pic = unit_augmentation(path)
    # for i in range(10):
    #     pic = unit_augmentation_factor(path,base_factor*i)
    #     pic = Image.fromarray(pic)
    #
    #     out_path = save_path / str(path.stem) / (str(path.stem) + f"_{i}.jpg")
    #     pic.save(out_path)
