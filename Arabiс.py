from PIL import Image, ImageDraw, ImageFont
import cv2
import arabic_reshaper
from bidi.algorithm import get_display
import numpy as np

class ArabicImageGenerator:
    def __init__(self, template_path, avatar_path, font_bold_path, font_regular_path):
        # Initialize paths for the template, avatar, and fonts
        self.TEMPLATE_PATH = template_path
        self.AVATAR_PATH = avatar_path
        self.FONT_BOLD_PATH = font_bold_path
        self.FONT_REGULAR_PATH = font_regular_path

    # Method to truncate text if it's too long
    def truncate_text(self, text, max_chars=27):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        if len(bidi_text) > max_chars:
            bidi_text = '...' + bidi_text[-max_chars:]
        return bidi_text

    # Method to wrap text into multiple lines if it exceeds the maximum width
    def wrap_text(self, draw, text, font, max_width):
        lines = []  # List to hold lines of text
        words = text.split()  # Split text into words
        current_line = ''

        for word in words:
            test_line = f'{current_line} {word}'.strip()
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)  # If not, add the current line to lines
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    # Method to add Arabic text to the image at specified positions
    def add_arabic_text(self, draw, text, font, initial_y_position, fill_color, image_width, text_offset=270):
        MAX_WIDTH = image_width - text_offset - 30
        lines = self.wrap_text(draw, text, font, MAX_WIDTH)
        y_position = initial_y_position
        LINE_HEIGHT = draw.textbbox((0, -20), "A", font=font)[3]

        for line in lines:
            truncated_text = self.truncate_text(line)
            text_bbox = draw.textbbox((0, 0), truncated_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_position = (image_width - text_width - text_offset, y_position)
            draw.text(text_position, truncated_text, font=font, fill=fill_color)
            y_position += LINE_HEIGHT + 5  # Move to the next line

    # Main method to generate the image with the provided details
    def generate_image(self, name, company, position, output_path):
        BACKGROUND_IMAGE = cv2.imread(self.TEMPLATE_PATH)
        BACKGROUND_PIL = Image.fromarray(cv2.cvtColor(BACKGROUND_IMAGE, cv2.COLOR_BGR2RGB))

        # Load and resize the avatar image (e.g., a logo)
        AVATAR_IMAGE = Image.open(self.AVATAR_PATH).resize((200, 200), Image.Resampling.LANCZOS)
        BACKGROUND_PIL.paste(AVATAR_IMAGE, (980, 400), AVATAR_IMAGE)

        # Set up fonts for name, company, and position
        FONT_NAME = ImageFont.truetype(self.FONT_BOLD_PATH, 50)
        FONT_COMPANY = ImageFont.truetype(self.FONT_REGULAR_PATH, 30)
        FONT_POSITION = ImageFont.truetype(self.FONT_REGULAR_PATH, 35)
        draw = ImageDraw.Draw(BACKGROUND_PIL)

        IMAGE_WIDTH = BACKGROUND_PIL.width
        # Adjust text position based on the length of the name
        if len(name) < 22:
            NAME_Y_POSITION = 400
            COMPANY_Y_POSITION = 480
            POSITION_Y_POSITION = 530
        else:
            NAME_Y_POSITION = 370
            COMPANY_Y_POSITION = 490
            POSITION_Y_POSITION = 530

        # Add the text to the image
        self.add_arabic_text(draw, name, FONT_NAME, NAME_Y_POSITION, (255, 255, 255), IMAGE_WIDTH)
        self.add_arabic_text(draw, company, FONT_COMPANY, COMPANY_Y_POSITION, (169, 169, 165), IMAGE_WIDTH)
        self.add_arabic_text(draw, position, FONT_POSITION, POSITION_Y_POSITION, (255, 255, 255), IMAGE_WIDTH)

        # Convert the image back to OpenCV format and save it
        RESULT_IMAGE = cv2.cvtColor(np.array(BACKGROUND_PIL), cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, RESULT_IMAGE)
        cv2.imshow('Result', RESULT_IMAGE)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
