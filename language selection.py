from enum import Enum
from English import ImageGenerator
from Arabic import ArabicImageGenerator

# Enum to represent the supported languages
class Languages(str, Enum):
    ARABIC = "ARABIC"
    ENGLISH = "ENGLISH"

# Class to handle image generation based on the selected language
class ImageGeneratorService:
    def __init__(self, language: Languages, name: str, profession: str, title_rank: str):
        self.language = language
        self.name = name
        self.profession = profession
        self.title_rank = title_rank
        self.image_generator = None
        self.output_file_path = ""
    #language definition
    def select_language(self):
        # Configure for the selected language
        if self.language == Languages.ARABIC:
            self.image_generator = ArabicImageGenerator(
                template_path='C:/Users/MSI/Desktop/ar-template.png',
                overlay_path='C:/Users/MSI/Desktop/gg.png',
                font_bold_path='C:/Users/MSI/Desktop/NotoSansArabic-Bold.ttf',
                font_regular_path='C:/Users/MSI/Desktop/NotoSansArabic-Regular.ttf'
            )
            self.output_file_path = 'C:/Users/MSI/Desktop/result_image_arabic.jpeg'
        elif self.language == Languages.ENGLISH:
            self.image_generator = ImageGenerator(
                template_path='C:/Users/MSI/Desktop/template.png',
                overlay_path='C:/Users/MSI/Desktop/gg.png',
                font_bold_path='C:/Users/MSI/Desktop/Inter_18pt-SemiBold.ttf',
                font_regular_path='C:/Users/MSI/Desktop/Inter_18pt-Regular.ttf'
            )
            self.output_file_path = 'C:/Users/MSI/Desktop/result_image_english.jpeg'
        else:
            raise ValueError("Invalid language selection. Choose either 'ARABIC' or 'ENGLISH'.")

    def generate_image(self):
        # Configure the image generator
        self.select_language()

        # Generate the image using the configured generator
        self.image_generator.generate_image(
            name=self.name,
            profession=self.profession,
            title_rank=self.title_rank,
            output_path=self.output_file_path
        )
        print(f"Image generated and saved to {self.output_file_path}")

# Example usage:
service_arabic = ImageGeneratorService(language=Languages.ARABIC, name='محمد العلي', profession='مهندس برمجيات', title_rank='مطور أول')
service_arabic.generate_image()

#service_english = ImageGeneratorService(language=Languages.ENGLISH, name='John Doe', profession='Software Engineer', title_rank='Senior Developer')
#service_english.generate_image()
