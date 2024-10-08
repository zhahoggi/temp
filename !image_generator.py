from enum import Enum
from English import EnglishImageGenerator
from Arabic import ArabicImageGenerator

# Constants for file paths
AR_TEMPLATE_PATH = './ar-template.png'
EN_TEMPLATE_PATH = './template.png'
AVATAR_PATH = './gg.png'
AR_FONT_BOLD_PATH = './NotoSansArabic-Bold.ttf'
AR_FONT_REGULAR_PATH = './NotoSansArabic-Regular.ttf'
EN_FONT_BOLD_PATH = './Inter_18pt-SemiBold.ttf'
EN_FONT_REGULAR_PATH = './Inter_18pt-Regular.ttf'
OUTPUT_FILE_PATH = './result_image.jpeg'

# Enum to represent the supported languages
class Languages(str, Enum):
    ARABIC = "ARABIC"
    ENGLISH = "ENGLISH"

# Class to handle image generation based on the selected language
class ImageGenerator:
    def __init__(self, language: Languages, name: str, company: str, position: str):
        self.language = language
        self.name = name
        self.company = company
        self.position = position

    # Language definition
    def select_language(self):
        # Configure for the selected language
        if self.language == Languages.ARABIC:
            self.image_generator = ArabicImageGenerator(
                template_path=AR_TEMPLATE_PATH,
                avatar_path=AVATAR_PATH,
                font_bold_path=AR_FONT_BOLD_PATH,
                font_regular_path=AR_FONT_REGULAR_PATH
            )
        elif self.language == Languages.ENGLISH:
            self.image_generator = EnglishImageGenerator(
                template_path=EN_TEMPLATE_PATH,
                avatar_path=AVATAR_PATH,
                font_bold_path=EN_FONT_BOLD_PATH,
                font_regular_path=EN_FONT_REGULAR_PATH
            )
        else:
            raise ValueError("Invalid language selection. Choose either 'ARABIC' or 'ENGLISH'.")

    def generate_image(self):
        # Configure the image generator
        self.select_language()
        # Generate the image using the configured generator
        self.image_generator.generate_image(
            name=self.name,
            company=self.company,
            position=self.position,
            output_path=OUTPUT_FILE_PATH
        )

# Example usage:
service_arabic = ImageGenerator(language=Languages.ARABIC, name='محمد العلي', company='شركة البرمجيات', position='مطور أول')
service_arabic.generate_image()

# service_english = ImageGenerator(language=Languages.ENGLISH, name='John Doe', company='Tech Corp', position='Senior Developer')
# service_english.generate_image()
