# -*- coding: utf-8 -*-
# @Time    : 2023/5/18 18:41
# @Author  : Kenny Zhou
# @FileName: hsv_color_name.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

# 导入opencv库
import cv2
import numpy as np

# 定义一个函数，用于输入RGB数值并转换为HSV数值
def rgb_to_hsv(r, g, b):
    # 将RGB数值转换为numpy数组，并调整维度为(1, 1, 3)
    rgb = np.array([[[r, g, b]]], dtype=np.uint8)
    # 使用opencv的函数将RGB数组转换为HSV数组
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    # 返回HSV数组中的第一个元素，即HSV数值
    return hsv[0][0]

# 定义一个函数，用于根据HSV数值判断颜色名称
def hsv_to_color(h, s, v):
    # 定义一个HSV颜色值对照表的字典，键是颜色名称，值是HSV数值的范围
    hsv_dict = {"黑": [(0, 0, 0), (180, 255, 46)],
                "灰": [(0, 0, 46), (180, 43, 220)],
                "白": [(0, 0, 221), (180, 30, 255)],
                "红": [(0, 43, 46), (10, 255, 255)],
                "橙": [(11, 43, 46), (25, 255, 255)],
                "黄": [(26, 43, 46), (34, 255, 255)],
                "绿": [(35, 43, 46), (77, 255, 255)],
                "青": [(78, 43, 46), (99, 255, 255)],
                "蓝": [(100, 43, 46), (124, 255, 255)],
                "紫": [(125, 43, 46), (155, 255, 255)]}
    # 遍历字典中的每个键值对
    for color_name in hsv_dict:
        # 获取颜色名称对应的HSV数值范围
        hsv_range = hsv_dict[color_name]
        # 判断输入的HSV数值是否在该范围内
        if h >= hsv_range[0][0] and h <= hsv_range[1][0] and s >= hsv_range[0][1] and s <= hsv_range[1][1] and v >= hsv_range[0][2] and v <= hsv_range[1][2]:
            # 如果是，则返回颜色名称
            return color_name
    # 如果没有匹配到任何颜色名称，则返回"未知"
    return "未知"

# 定义一个主函数，用于执行程序的逻辑
def main():

    while True:
        # 输入RGB数值，使用逗号分隔，并转换为整数列表
        rgb_list = list(map(int,input("请输入R,G,B数值（0-255），用逗号分隔：").split(",")))
        # 调用rgb_to_hsv函数，得到HSV数值
        hsv = rgb_to_hsv(rgb_list[0],rgb_list[1],rgb_list[2])
        # 打印HSV数值
        print("HSV数值为：", hsv)

        # 调用hsv_to_color函数，得到颜色名称
        color_name = hsv_to_color(hsv[0],hsv[1],hsv[2])
        # 打印颜色名称
        print("颜色名称为：", color_name,f"\n{hsv[0],hsv[1],hsv[2]}")



# 判断是否是主模块，如果是，则调用主函数
if __name__ == "__main__":
    main()