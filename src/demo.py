from PIL import Image, ImageDraw, ImageFont


def create_image_from_text(text, image_path):
    # 设置字体和字号
    font_size = 40
    font = ImageFont.truetype("Data/OPlusSans.ttf", font_size)

    # 计算文本的尺寸
    text_width, text_height = font.getsize(text)

    # 设置图片大小
    image_width = text_width + 20  # 加上一些额外空间
    image_height = text_height + 20

    # 创建新图像对象
    image = Image.new("RGB", (image_width, image_height), (255, 255, 255))

    # 创建绘制对象
    draw = ImageDraw.Draw(image)

    # 计算文本的位置
    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2

    # 绘制文本
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    # 保存图像文件
    image.save(image_path)


if __name__ == "__main__":
    # 获取用户输入的内容
    text = input("请输入文本内容：")

    # 将内容保存到文本文件
    file_path = "input.txt"
    with open(file_path, "w") as file:
        file.write(text)

    print("内容已保存到文件：", file_path)

    # 从文件中读取文本内容
    with open(file_path, "r") as file:
        text = file.read()

    # 生成图片
    image_path = "output.png"
    create_image_from_text(text, image_path)
    print("图像已生成：", image_path)
