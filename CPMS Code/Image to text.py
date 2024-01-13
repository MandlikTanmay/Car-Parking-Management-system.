# from PIL import Image
# import pytesseract

# # Set the path to the Tesseract executable (modify this based on your installation)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def image_to_text(image_path):
#     # Open the image file
#     img = Image.open(image_path)

#     # Perform OCR on the image
#     text = pytesseract.image_to_string(img)

#     return text

# # Specify the path to your image file
# image_path = 'Number Plate_3.png'

# # Convert image to text
# result_text = image_to_text(image_path)

# # Print the result
# print("Extracted Text:")
# print(result_text)
import easyocr

def image_to_text(image_path, language='en'):
    # Create an OCR reader
    reader = easyocr.Reader([language])

    # Read text from the image
    result = reader.readtext(image_path)

    # Extract text from the result
    text = ' '.join([entry[1] for entry in result])

    return text

# Specify the path to your image file
image_path = 'Number Plate_3.png'

# Convert image to text
result_text = image_to_text(image_path)

# Print the result
print("Extracted Text:")
print(result_text)
