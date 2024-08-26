from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

class EnglishImageGenerator:
    def __init__(self, template_path, avatar_path, font_bold_path, font_regular_path):
        self.TEMPLATE_PATH = template_path
        self.AVATAR_PATH = avatar_path
        self.FONT_BOLD_PATH = font_bold_path
        self.FONT_REGULAR_PATH = font_regular_path
        self.MAX_TEXT_WIDTH = 600  # Maximum text width

    def truncate_text(self, draw, text, font):
        text_bbox = draw.textbbox((0, 0), text, font=font)
        if text_bbox[2] - text_bbox[0] > self.MAX_TEXT_WIDTH:
            while text_bbox[2] - text_bbox[0] > self.MAX_TEXT_WIDTH:
                text = text[:-1]
                text_bbox = draw.textbbox((0, 0), text + '...', font=font)
            text = text.strip() + '...'
        return text

    def generate_image(self, name, company, position, output_path):
        # Uploading and preparing the image
        BACKGROUND_IMAGE = cv2.imread(self.TEMPLATE_PATH)
        BACKGROUND_PIL = Image.fromarray(cv2.cvtColor(BACKGROUND_IMAGE, cv2.COLOR_BGR2RGB))

        # Uploading and resizing an avatar (logo or other image)
        AVATAR_IMAGE = Image.open(self.AVATAR_PATH)
        AVATAR_IMAGE = AVATAR_IMAGE.resize((200, 200), Image.Resampling.LANCZOS)

        # Position for avatar insertion
        AVATAR_POSITION = (50, 400)
        BACKGROUND_PIL.paste(AVATAR_IMAGE, AVATAR_POSITION, AVATAR_IMAGE)

        # Font customization
        FONT_NAME = ImageFont.truetype(self.FONT_BOLD_PATH, 50)
        FONT_COMPANY = ImageFont.truetype(self.FONT_REGULAR_PATH, 30)
        FONT_POSITION = ImageFont.truetype(self.FONT_REGULAR_PATH, 35)

        # Creating an object for drawing
        DRAW = ImageDraw.Draw(BACKGROUND_PIL)

        # Processing text for placement on an image
        NAME = self.truncate_text(DRAW, name, FONT_NAME)
        COMPANY = self.truncate_text(DRAW, company, FONT_COMPANY)
        POSITION = self.truncate_text(DRAW, position, FONT_POSITION)

        # Overlaying text on top of an image
        DRAW.text((270, 415), NAME, font=FONT_NAME, fill=(255, 255, 255))
        DRAW.text((270, 487), COMPANY, font=FONT_COMPANY, fill=(169, 169, 165))
        DRAW.text((270, 540), POSITION, font=FONT_POSITION, fill=(255, 255, 255))

        # Convert the image back to OpenCV format and save it
        RESULT_IMAGE = cv2.cvtColor(np.array(BACKGROUND_PIL), cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, RESULT_IMAGE)
        cv2.imshow('Result', RESULT_IMAGE)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
