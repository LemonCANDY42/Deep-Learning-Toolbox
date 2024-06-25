# -*- coding: utf-8 -*-
# @Time    : 2024/06/21 17:40
# @Author  : Kenny Zhou
# @FileName: auto_cut.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

"""
给定一张本地图像和目标比例（如16:9），点击图像上的任意点，将其作为新图像中三分法九宫格线的一个交点（选择距离原图最近的模板点），并按该比例裁剪出最大图像。

"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 记录点击点的全局变量
click_point = []

# 预设三分法的四个交叉点归一化坐标
thirds_points = [(1 / 3, 1 / 3), (2 / 3, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 2 / 3)]

# 输入的图像比例
R = [16, 9] # h，w
R.reverse()

# 打开图像并显示
def open_image(image_path):
    img = Image.open(image_path)
    img_width, img_height = img.size
    print(f"img_width：{img_width},img_height:{img_height}")
    fig, ax = plt.subplots()
    ax.imshow(img)

    # 绘制九宫格线
    draw_thirds_lines(ax, img_width, img_height)

    cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, img))
    plt.show()


# 处理点击事件
def onclick(event, img):
    click_point = (event.xdata, event.ydata)
    if click_point[0] is not None and click_point[1] is not None:
        print(f"Clicked at: {click_point}")
        process_click(click_point, img)


# 处理点击事件，计算并切出新图
def process_click(click, img):
    img_width, img_height = img.size
    click_x, click_y = click
    click_x_norm = click_x / img_width
    click_y_norm = click_y / img_height

    # 找到最近的九宫格点
    distances = [((click_x_norm - px) ** 2 + (click_y_norm - py) ** 2) ** 0.5 for px, py in thirds_points]
    closest_index = distances.index(min(distances))
    target_point = thirds_points[closest_index]

    target_x, target_y = target_point

    # 计算点击点到图像边缘的距离
    w_d = min(click_x, img_width - click_x)
    h_d = min(click_y, img_height - click_y)

    if w_d == click_x:
        w_max = w_d / target_x
    else:
        w_max = w_d / (1 - target_x)

    if h_d == click_y:
        h_max = h_d / target_y
    else:
        h_max = h_d / (1 - target_y)

    print(f"click_x:{click_x},click_y:{click_y},w_max:{w_max},h_max:{h_max}")

    h_new,w_new = 0,0

    w_max_R = h_max * R[0] / R[1] # 新图的最高的大小
    h_max_R = w_max * R[1] / R[0] # 新图的最宽的大小

    if img_width < w_max_R and img_height < h_max_R:
        w_new = w_max
        h_new = h_max
        print(1)
    elif img_width >= w_max_R and img_height < h_max_R:
        print(2)
        h_new = h_max
        w_new = h_new * R[0] / R[1]
        if h_max>img_height:
            if h_d != click_y:
                h_new = click_y/target_y
                w_new = h_new * R[0] / R[1]
                print("2-0")
            else:
                h_new = (img_height-click_y)/(1-target_y)
                w_new = h_new * R[0] / R[1]
                print("2-1")

    elif img_width < w_max_R and img_height >= h_max_R:
        w_new = w_max
        h_new = w_new * R[1] / R[0]
        if w_max>img_width:
            if w_d != click_x:
                w_new = click_x/target_x
                h_new = w_new * R[1] / R[0]
                print("3-0")
            else:
                w_new = (img_width-click_x)/(1-target_x)
                h_new = w_new * R[1] / R[0]
                print("3-1")


        print(3)
    else:
        w_new = w_max
        h_new = w_new * R[1] / R[0]
        print(4)
        print(h_max_R > h_max,w_max_R>w_max)
        if h_max_R > h_max:
            h_new = h_max
            w_new = h_new * R[0] / R[1]
        elif w_max_R>w_max:
            w_new = w_max
            h_new = w_new * R[1] / R[0]
        else:
            print("???")


    N_x = click_x - w_new * target_x
    N_y = click_y - h_new * target_y

    print("N_y",N_y)

    # 修正坐标，使其在图像范围内
    # if N_x < 0:
    #     N_x = 0
    # if N_y < 0:
    #     N_y = 0
    # if (N_x + w_new) > img_width:
    #     N_x = img_width - w_new
    # if (N_y + h_new) > img_height:
    #     N_y = img_height - h_new

    left = N_x
    upper = N_y
    right = N_x + w_new
    lower = N_y + h_new

    if left >= right or upper >= lower:
        print("Error: Invalid crop coordinates.")
        return

    new_img = img.crop((left, upper, right, lower))

    draw_grid_and_click(img, new_img, (left, upper, right, lower), click, w_new, h_new)


# 在原图和新图上绘制九宫格和点击点
def draw_grid_and_click(img, new_img, bbox, click, w_new, h_new):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # 绘制原图
    ax1.imshow(img)
    ax1.plot(click[0], click[1], 'ro')
    rect = plt.Rectangle((bbox[0], bbox[1]), w_new, h_new, edgecolor='blue', facecolor='none')
    ax1.add_patch(rect)
    draw_thirds_lines(ax1, img.width, img.height)
    ax1.set_title("Original Image")

    # 绘制新图
    ax2.imshow(new_img)
    new_click_x = (click[0] - bbox[0]) * new_img.width / w_new
    new_click_y = (click[1] - bbox[1]) * new_img.height / h_new
    ax2.plot(new_click_x, new_click_y, 'ro')
    draw_thirds_lines(ax2, new_img.width, new_img.height)
    ax2.set_title("Cropped Image")

    plt.show()


def draw_thirds_lines(ax, width, height):
    thirds_x = [width / 3, 2 * width / 3]
    thirds_y = [height / 3, 2 * height / 3]

    for x in thirds_x:
        ax.axvline(x=x, color='yellow', linestyle='--')
    for y in thirds_y:
        ax.axhline(y=y, color='yellow', linestyle='--')


# 绑定点击事件并打开图片
fig, ax = plt.subplots()
image_path = '/Users/kennymccormick/Pictures/PhotosExprot/IMG_2765.jpeg'
open_image(image_path)
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

