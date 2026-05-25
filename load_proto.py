from PIL import Image
import numpy as np


def simple_digit_processing_quick(image_path):
    """快速修复透明PNG问题"""

    img = Image.open(image_path)

    # 处理透明背景：用白色填充
    if img.mode in ('RGBA', 'LA', 'P'):
        # 创建白色背景
        background = Image.new('RGBA', img.size, (255, 255, 255, 255))

        # 确保是RGBA模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 合并图片和背景
        img = Image.alpha_composite(background, img)

    # 转换为RGB
    img = img.convert('RGB')

    # 计算灰度
    img_array = np.array(img)
    gray_array = np.dot(img_array[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)

    # 调整大小
    img_gray = Image.fromarray(gray_array)
    img_resized = img_gray.resize((28, 28), Image.Resampling.LANCZOS)
    img_array_28 = np.array(img_resized)

    # 确保黑底白字
    if img_array_28.mean() > 128:
        img_array_28 = 255 - img_array_28

    # 归一化
    if img_array_28.max() > 0:
        img_array_28 = (img_array_28 - img_array_28.min()) / (img_array_28.max() - img_array_28.min()) * 255

    img_array_28 = img_array_28.astype(np.uint8)
    pixels = img_array_28.flatten()

    return pixels

# 使用
# pixels = simple_digit_processing_quick('识别.png')
# print(f"像素范围: [{pixels.min()}, {pixels.max()}]")
