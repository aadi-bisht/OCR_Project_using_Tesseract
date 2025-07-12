import os
import pytesseract
from PIL import Image


def main():
    image_paths = []
    folder_path = "./images"

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".jpg"):
            file_path = os.path.join(folder_path, filename)
            image_paths.append(file_path)


    for i, img_path in enumerate(image_paths):
        image = Image.open(img_path)
        text = pytesseract.image_to_string(image)
        print(img_path.upper(), text.strip(), end=f"\n{i}___________________________\n")


if __name__ == '__main__':
    main()