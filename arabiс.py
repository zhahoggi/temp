from PIL import Image, ImageDraw, ImageFont
import cv2
import arabic_reshaper
from bidi.algorithm import get_display
import numpy as np

class ArabicImageGenerator:
    def __init__(self, template_path, overlay_path, font_bold_path, font_regular_path):
        self.template_path = template_path
        self.overlay_path = overlay_path
        self.font_bold_path = font_bold_path
        self.font_regular_path = font_regular_path

    def truncate_text(self, text, max_chars=27):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        if len(bidi_text) > max_chars:
            bidi_text = '...' + bidi_text[-max_chars:]
        return bidi_text

    def wrap_text(self, draw, text, font, max_width):
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

    def add_arabic_text(self, draw, text, font, initial_y_position, fill_color, image_width, text_offset=270):
        max_width = image_width - text_offset - 30
        lines = self.wrap_text(draw, text, font, max_width)
        y_position = initial_y_position
        line_height = draw.textbbox((0, -20), "A", font=font)[3]

        for line in lines:
            truncated_text = self.truncate_text(line)
            text_bbox = draw.textbbox((0, 0), truncated_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_position = (image_width - text_width - text_offset, y_position)
            draw.text(text_position, truncated_text, font=font, fill=fill_color)
            y_position += line_height + 5

    def generate_image(self, name, profession, title_rank, output_path):
        background_image = cv2.imread(self.template_path)
        background_pil = Image.fromarray(cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB))

        overlay_image = Image.open(self.overlay_path).resize((200, 200), Image.Resampling.LANCZOS)
        background_pil.paste(overlay_image, (980, 400), overlay_image)

        font_name = ImageFont.truetype(self.font_bold_path, 50)
        font_profession = ImageFont.truetype(self.font_regular_path, 30)
        font_title_rank = ImageFont.truetype(self.font_regular_path, 35)
        draw = ImageDraw.Draw(background_pil)

        image_width = background_pil.width
        if len(name) < 22:
            name_y_position = 400
            profession_y_position = 480
            title_rank_y_position = 530
        else:
            name_y_position = 370
            profession_y_position = 490
            title_rank_y_position = 530

        self.add_arabic_text(draw, name, font_name, name_y_position, (255, 255, 255), image_width)
        self.add_arabic_text(draw, profession, font_profession, profession_y_position, (169, 169, 165), image_width)
        self.add_arabic_text(draw, title_rank, font_title_rank, title_rank_y_position, (255, 255, 255), image_width)

        result_image = cv2.cvtColor(np.array(background_pil), cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, result_image)
        cv2.imshow('Result', result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
