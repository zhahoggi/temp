from English import ImageGenerator
from Arabic import ArabicImageGenerator

language_selection = input("Choose language (Arabic/English): ")

if language_selection == 'Arabic':
    generator = ArabicImageGenerator(
        template_path='C:/Users/MSI/Desktop/ar-template.png',
        overlay_path='C:/Users/MSI/Desktop/gg.png',
        font_bold_path='C:/Users/MSI/Desktop/NotoSansArabic-Bold.ttf',
        font_regular_path='C:/Users/MSI/Desktop/NotoSansArabic-Regular.ttf'
    )
elif language_selection == 'English':
    generator = ImageGenerator(
        template_path='C:/Users/MSI/Desktop/template.png',
        overlay_path='C:/Users/MSI/Desktop/gg.png',
        font_bold_path='C:/Users/MSI/Desktop/Inter_18pt-SemiBold.ttf',
        font_regular_path='C:/Users/MSI/Desktop/Inter_18pt-Regular.ttf'
    )
else:
    print("Invalid language selection.")
    exit()

generator.generate_image(
    name='John Doe' if language_selection == 'English' else 'محمد العلي',
    profession='Software Engineer' if language_selection == 'English' else 'مهندس برمجيات',
    title_rank='Senior Developer' if language_selection == 'English' else 'مطور أول',
    output_path='C:/Users/MSI/Desktop/result_image.jpeg'
)
