from PIL import Image, ImageDraw, ImageFont  
import cv2  
import arabic_reshaper  
from bidi.algorithm import get_display  
import numpy as np  
class ArabicImageGenerator:
    def __init__(self, template_path, overlay_path, font_bold_path, font_regular_path):
        # Initialize paths for the template, overlay, and fonts
        self.template_path = template_path
        self.overlay_path = overlay_path
        self.font_bold_path = font_bold_path
        self.font_regular_path = font_regular_path

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
            y_position += line_height + 5  # Move to the next line

    # Main method to generate the image with the provided details
    def generate_image(self, name, profession, title_rank, output_path):
        background_image = cv2.imread(self.template_path)  
        background_pil = Image.fromarray(cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)) 

        # Load and resize the overlay image (e.g., a logo)
        overlay_image = Image.open(self.overlay_path).resize((200, 200), Image.Resampling.LANCZOS)
        background_pil.paste(overlay_image, (980, 400), overlay_image)  

        # Set up fonts for name, profession, and title rank
        font_name = ImageFont.truetype(self.font_bold_path, 50)
        font_profession = ImageFont.truetype(self.font_regular_path, 30)
        font_title_rank = ImageFont.truetype(self.font_regular_path, 35)
        draw = ImageDraw.Draw(background_pil)

        image_width = background_pil.width
        # Adjust text position based on the length of the name
        if len(name) < 22:
            name_y_position = 400
            profession_y_position = 480
            title_rank_y_position = 530
        else:
            name_y_position = 370
            profession_y_position = 490
            title_rank_y_position = 530

        # Add the text to the image
        self.add_arabic_text(draw, name, font_name, name_y_position, (255, 255, 255), image_width)
        self.add_arabic_text(draw, profession, font_profession, profession_y_position, (169, 169, 165), image_width)
        self.add_arabic_text(draw, title_rank, font_title_rank, title_rank_y_position, (255, 255, 255), image_width)

        # Convert the image back to OpenCV format and save it
        result_image = cv2.cvtColor(np.array(background_pil), cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, result_image)
        cv2.imshow('Result', result_image)  
        cv2.waitKey(0)  
        cv2.destroyAllWindows()  
