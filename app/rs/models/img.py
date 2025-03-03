from PIL import Image
import os

class Imgr:

    def __init__(self, max_width=3000, max_height=3000):
        self.max_width = max_width
        self.max_height = max_height

    def rewrite_img(self, img_path):
        try:
            # Open image
            with Image.open(img_path) as img:
                # Get the current image dimensions
                width, height = img.size

                # Checking if the dimensions need to be changed
                if width > self.max_width or height > self.max_height:
                    # Вычисляем соотношение для уменьшения
                    scale = min(self.max_width / width, self.max_height / height)
                    new_width = int(width * scale)
                    new_height = int(height * scale)

                    # Reduce the image and resave
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Save the image with the same name
                img.save(img_path)

            # Return the path to the file if successful
            return img_path

        except Exception as e:
            # В случае ошибки удаляем файл и возвращаем False
            print(f"Error processing image {img_path}: {e}")
            if os.path.exists(img_path):
                os.remove(img_path)
            return False
