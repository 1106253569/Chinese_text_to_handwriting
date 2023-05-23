import re
from PIL import Image, ImageDraw, ImageFont


def split_text_by_language(text, max_chars_per_line):
    '''
    使用了正则表达式模式 [\u4e00-\u9fa5] 来匹配中文字符
    对于每个英文字符,将字符计数+0.5
    对于每个中文字符,将字符计数+1
    根据字符计数来判断是否超过每行的最大字符数，进行分割。
    '''
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')

    lines = []
    current_line = ""
    char_count = 0

    for char in text:
        # 判断字符是否是中文字符
        if chinese_pattern.match(char):
            char_count += 1
        else:
            char_count += 0.5

        current_line += char

        # 如果当前行的字符数超过了指定的每行字符数，则将该行保存
        if char_count >= max_chars_per_line:
            lines.append(current_line.strip())
            current_line = ""
            char_count = 0

    # 将剩余的行保存
    if current_line.strip() != "":
        lines.append(current_line.strip())

    return lines


def estimate_character_size(font_file, font_size):
    '''估算特定字体和字号下字符的大致像素宽度和高度'''
    font = ImageFont.truetype(font_file, font_size)
    character = "来"  # 选择一个具有代表性的字符
    left, top, right, bottom = font.getbbox(character)
    width = abs(right - left) + 0.5
    height = abs(bottom - top) + 0.5
    return width, height


def calculate_length(element):
    '''
    计算每个元素的长度
    使用正则表达式模式[\u4e00-\u9fa5]来匹配中文字符
    根据中英文字符的不同对长度进行累加
    '''
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')
    length = 0
    for char in element:
        if chinese_pattern.match(char):
            length += 1
        else:
            length += 0.5
    return length


def find_longest_length(array):
    '''
    遍历数组中的每个元素,调用calculate_length函数计算元素的长度,并记录最长长度
    '''
    longest_length = 0
    for element in array:
        length = calculate_length(element)
        if length > longest_length:
            longest_length = length
    return longest_length


def generate_text_image(input_file,
                        output_file,
                        font_file='Data/OPlusSans.ttf',
                        max_chars_per_line=40):
    '''
    按段落读取一个txt文本,存储为一个字符数组
    默认字体文件路径为Data/OPlusSans.ttf
    默认为40的每行字符数量进行换行
    且根据行数以及每行字符数量设定图片大小
    接下来，根据以上的数组生成一个文本图片，
    '''
    # 加载字体
    font_size = 24
    font = ImageFont.truetype(font_file, font_size)

    # 读取txt文件内容
    with open(input_file, 'r') as txt_file:
        text = txt_file.read()

    # 计算文本行数和图片大小
    lines = []
    for line in text.split('\n'):
        for temp in split_text_by_language(line, max_chars_per_line):
            lines.append(temp)
    print(lines)
    num_lines = len(lines)
    print(num_lines)

    max_line_length = find_longest_length(lines)
    font_width, font_height = estimate_character_size(font_file, font_size)
    image_width = int(max_line_length * (font_width + 4))  # 假设每个字符占用20个像素的宽度
    image_height = int(num_lines * (font_height + 8))  # 假设每行文本占用40个像素的高度

    # 创建空白图片
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)

    # 在图片上绘制文本,设置5%的上边距
    y = image_height * 0.05
    for line in lines:
        x = image_width * 0.05
        draw.text((x, y), line, font=font, fill='black')
        y += font_size + 4  # 行间距设为4个像素

    # 保存图片
    image.save(output_file)
    print("图片成功生成")


if __name__ == '__main__':
    # 示例用法
    Input_file = 'input.txt'
    Output_file = 'output.png'
    generate_text_image(Input_file, Output_file)
