from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display


# Функция для обрезки текста, если он превышает 50 символов, и добавления многоточия слева
def truncate_text(draw, text, font, max_chars=27):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    if len(bidi_text) > max_chars:
        bidi_text = '...' + bidi_text[-(max_chars):]  # Обрезаем и добавляем многоточие слева
    return bidi_text


# Функция для разбиения текста на несколько строк по ширине
def wrap_text(draw, text, font, max_width):
    lines = []
    words = text.split()
    current_line = ''

    for word in words:
        # Проверяем, влезет ли слово в текущую строку
        test_line = f'{current_line} {word}'.strip()
        text_bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


# Функция для добавления текста на изображение с учетом переноса строк
def add_arabic_text(draw, text, font, position, fill, image_width, offset=270):
    max_width = image_width - offset - 30
    lines = wrap_text(draw, text, font, max_width)
    y_position = position
    line_height = draw.textbbox((0, -20), "A", font=font)[3]  # Получаем высоту строки

    for line in lines:
        truncated_text = truncate_text(draw, line, font)
        text_bbox = draw.textbbox((0, 0), truncated_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_position = (image_width - text_width - offset, y_position)
        draw.text(text_position, truncated_text, font=font, fill=fill)
        y_position += line_height + 5  # Интервал между строками


# Загрузка изображения
img = cv2.imread('C:/Users/MSI/Desktop/ar-template.png')
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Наложение дополнительного изображения
overlay = Image.open("C:/Users/MSI/Desktop/gg.png").resize((200, 200), Image.Resampling.LANCZOS)
img_pil.paste(overlay, (980, 400), overlay)

# Настройка шрифтов
font_path1 = 'C:/Users/MSI/Desktop/NotoSansArabic-Bold.ttf'
font_path2 = 'C:/Users/MSI/Desktop/NotoSansArabic-Regular.ttf'
font1 = ImageFont.truetype(font_path1, 50)
font2 = ImageFont.truetype(font_path2, 30)
font3 = ImageFont.truetype(font_path2, 35)
draw = ImageDraw.Draw(img_pil)

# Ввод данных пользователем
name = input('Name: ')
profession = input('Profession: ')
title_rank = input('Title/Rank: ')

if len(name) < 22:
    image_width = img_pil.width
    add_arabic_text(draw, name, font1, 400, (255, 255, 255), image_width)
    add_arabic_text(draw, profession, font2, 480, (169, 169, 165), image_width)
    add_arabic_text(draw, title_rank, font3, 530, (255, 255, 255), image_width)
else:
    image_width = img_pil.width
    add_arabic_text(draw, name, font1, 370, (255, 255, 255), image_width)
    add_arabic_text(draw, profession, font2, 490, (169, 169, 165), image_width)
    add_arabic_text(draw, title_rank, font3, 530, (255, 255, 255), image_width)

# Конвертация изображения обратно в формат OpenCV и сохранение
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

cv2.imshow('Result', img)
cv2.imwrite('C:/Users/MSI/Desktop/img2.jpeg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
