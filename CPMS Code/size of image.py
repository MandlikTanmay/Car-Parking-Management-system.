from PIL import Image
from PIL import Image, ImageFilter
import os

def resize_and_save(input_path, output_path, target_size_kb=100):
    # Open the image file
    with Image.open(input_path) as img:
        # Resize the image while maintaining the aspect ratio
        img.thumbnail((650, 700))
        
        # Save the image with compression to reduce file size
        img.save(output_path, quality=95)

def main():
    input_folder = 'Input'  # Change this to the path of your input folder
    output_folder = 'Output'  # Change this to the path of your output folder

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Resize and save the image
            resize_and_save(input_path, output_path)
def maximize_image_sharpness(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Open the image
            image = Image.open(input_path)

            # Apply maximum sharpening filter
            sharpened_image = image.filter(ImageFilter.SHARPEN)

            # Save the sharpened image
            sharpened_image.save(output_path, quality=95)  # Adjust quality as needed

# Example usage
input_folder_path = 'Output'
output_folder_path = 'Final_Output'



if __name__ == "__main__":
    main()
    maximize_image_sharpness(input_folder_path, output_folder_path)






# "C:\Users\Dell\AppData\Local\Programs\Microsoft VS Code\Code.exe"