from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

class EnglishImageGenerator:
    def __init__(self, template_path, avatar_path, font_bold_path, font_regular_path):
        self.template_path = template_path
        self.avatar_path = avatar_path
        self.font_bold_path = font_bold_path
        self.font_regular_path = font_regular_path
        self.max_text_width = 600  # Maximum text width

    def truncate_text(self, draw, text, font):
        text_bbox = draw.textbbox((0, 0), text, font=font)
        if text_bbox[2] - text_bbox[0] > self.max_text_width:
            while text_bbox[2] - text_bbox[0] > self.max_text_width:
                text = text[:-1]
                text_bbox = draw.textbbox((0, 0), text + '...', font=font)
            text = text.strip() + '...'
        return text

    def generate_image(self, name, company, position, output_path):
        # Uploading and preparing the image
        background_image = cv2.imread(self.template_path)
        background_pil = Image.fromarray(cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB))

        # Uploading and resizing an avatar (logo or other image)
        avatar_image = Image.open(self.avatar_path)
        avatar_image = avatar_image.resize((200, 200), Image.Resampling.LANCZOS)

        # Position for avatar insertion
        avatar_position = (50, 400)
        background_pil.paste(avatar_image, avatar_position, avatar_image)

        # Font customization
        font_name = ImageFont.truetype(self.font_bold_path, 50)
        font_company = ImageFont.truetype(self.font_regular_path, 30)
        font_position = ImageFont.truetype(self.font_regular_path, 35)

        # Creating an object for drawing
        draw = ImageDraw.Draw(background_pil)

        # Processing text for placement on an image
        name = self.truncate_text(draw, name, font_name)
        company = self.truncate_text(draw, company, font_company)
        position = self.truncate_text(draw, position, font_position)

        # Overlaying text on top of an image
        draw.text((270, 415), name, font=font_name, fill=(255, 255, 255))
        draw.text((270, 487), company, font=font_company, fill=(169, 169, 165))
        draw.text((270, 540), position, font=font_position, fill=(255, 255, 255))

        # Convert the image back to OpenCV format and save it
        result_image = cv2.cvtColor(np.array(background_pil), cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, result_image)
        cv2.imshow('Result', result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
