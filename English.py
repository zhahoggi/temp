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
max_width = 600  #

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
