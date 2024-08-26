from English import ImageGenerator
from Arabic import ArabicImageGenerator

def generate_image(language):
    if language.lower() == 'arabic':
        # Create an instance class for the Arabic language
        generator = ArabicImageGenerator(
            template_path='C:/Users/MSI/Desktop/ar-template.png',
            overlay_path='C:/Users/MSI/Desktop/gg.png',
            font_bold_path='C:/Users/MSI/Desktop/NotoSansArabic-Bold.ttf',
            font_regular_path='C:/Users/MSI/Desktop/NotoSansArabic-Regular.ttf'
        )
        name = 'محمد العلي'
        profession = 'مهندس برمجيات'
        title_rank = 'مطور أول'
    elif language.lower() == 'english':
        # Create an instance class for the English language
        generator = ImageGenerator(
            template_path='C:/Users/MSI/Desktop/template.png',
            overlay_path='C:/Users/MSI/Desktop/gg.png',
            font_bold_path='C:/Users/MSI/Desktop/Inter_18pt-SemiBold.ttf',
            font_regular_path='C:/Users/MSI/Desktop/Inter_18pt-Regular.ttf'
        )
        name = 'John Doe'
        profession = 'Software Engineer'
        title_rank = 'Senior Developer'
    else:
        raise ValueError("Invalid language selection. Choose either 'Arabic' or 'English'.")

    # Generate an image by passing the necessary parameters
    generator.generate_image(
        name=name,
        profession=profession,
        title_rank=title_rank,
        output_path='C:/Users/MSI/Desktop/result_image.jpeg'
    )

# Example usage:
generate_image(language='arabic')  # Replace 'english' with 'arabic' to generate an Arabic image
