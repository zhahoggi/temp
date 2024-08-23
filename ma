# для арабского языка
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display

def truncate_text(draw, text, font, max_chars=27):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    if len(bidi_text) > max_chars:
        bidi_text = '...' + bidi_text[-(max_chars):] 
    return bidi_text

def wrap_text(draw, text, font, max_width):
    lines = []
    words = text.split()
    current_line = ''
    for word in words:
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

def add_arabic_text(draw, text, font, position, fill, image_width, offset=270):
    max_width = image_width - offset - 30
    lines = wrap_text(draw, text, font, max_width)
    y_position = position
    line_height = draw.textbbox((0, -20), "A", font=font)[3] 
    for line in lines:
        truncated_text = truncate_text(draw, line, font)
        text_bbox = draw.textbbox((0, 0), truncated_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_position = (image_width - text_width - offset, y_position)
        draw.text(text_position, truncated_text, font=font, fill=fill)
        y_position += line_height + 5 

img = cv2.imread('C:/Users/MSI/Desktop/ar-template.png')
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
overlay = Image.open("C:/Users/MSI/Desktop/gg.png").resize((200, 200), Image.Resampling.LANCZOS)
img_pil.paste(overlay, (980, 400), overlay)
font_path1 = 'C:/Users/MSI/Desktop/NotoSansArabic-Bold.ttf'
font_path2 = 'C:/Users/MSI/Desktop/NotoSansArabic-Regular.ttf'
font1 = ImageFont.truetype(font_path1, 50)
font2 = ImageFont.truetype(font_path2, 30)
font3 = ImageFont.truetype(font_path2, 35)
draw = ImageDraw.Draw(img_pil)
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


img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
cv2.imshow('Result', img)
cv2.imwrite('C:/Users/MSI/Desktop/img2.jpeg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# для английского языка
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

def truncate_text(draw, text, font, max_width=600):
    text_bbox = draw.textbbox((0, 0), text, font=font)
    if text_bbox[2] - text_bbox[0] > max_width:
        while text_bbox[2] - text_bbox[0] > max_width:
            text = text[:-1]
            text_bbox = draw.textbbox((0, 0), text + '...', font=font)
        text = text.strip() + '...'
    return text

img = cv2.imread('C:/Users/MSI/Desktop/template.png')
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
overlay = Image.open("C:/Users/MSI/Desktop/gg.png")
overlay = overlay.resize((200, 200), Image.Resampling.LANCZOS)
position = (50, 400)
img_pil.paste(overlay, position, overlay)
font_path1 = 'C:/Users/MSI/Desktop/Inter_18pt-SemiBold.ttf'
font_path2 = 'C:/Users/MSI/Desktop/Inter_18pt-Regular.ttf'
font1 = ImageFont.truetype(font_path1, 50)
font2 = ImageFont.truetype(font_path2, 30)
font3 = ImageFont.truetype(font_path2, 35)
draw = ImageDraw.Draw(img_pil)

name = input('Name: ')
profession = input('Profession: ')
title_rank = input('Title/Rank: ')
max_width = 600  

name = truncate_text(draw, name, font1, max_width)
profession = truncate_text(draw, profession, font2, max_width)
title_rank = truncate_text(draw, title_rank, font3, max_width)
draw.text((270, 415), name, font=font1, fill=(255, 255, 255))
draw.text((270, 490), profession, font=font2, fill=(169, 169, 165))
draw.text((270, 540), title_rank, font=font3, fill=(255, 255, 255))

img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
cv2.imshow('Result', img)
cv2.imwrite('C:/Users/MSI/Desktop/img2.jpeg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

