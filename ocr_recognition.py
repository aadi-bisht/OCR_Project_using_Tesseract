import os
import pytesseract
from PIL import Image
import re


IGNORE_KEYWORDS = {
    'incoming', 'call', 'verizon', 'wifi', 'wi-fi', 'send', 'message',
    'call', 'center', 'identified', 'hiya', 'domestic', 'flagged', 'hiya',
    'drag', 'move', 'most', 'recent', 'call', 'battery', 'california', 'texas',
    'louisiana', 'michigan', 'massachusetts', 'virginia', 'risk', 'level', 'most', 'recent', 'yesterday'
}


def read_image(data_df):
    clean_lines = []
    folder_path = "./images"
    for filename in data_df["IMAGE NAME"].tolist():
        file_path = os.path.join(folder_path, filename)

        try:
            image = Image.open(file_path)
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DATAFRAME)
            ocr_data = ocr_data.dropna(subset=["text"])
            ocr_data = ocr_data[ocr_data["conf"] > 90]
            lines = ocr_data.groupby(["page_num", "block_num", "par_num", "line_num"])
            caller_name = clean_text(lines)

        except FileNotFoundError as e:
            caller_name = ["No Business Name Presented"]

        clean_lines.append(caller_name)
    return clean_lines


def is_noise_line(text):
    text_lower = text.lower().strip()
    return (
        any(kw.lower() in text_lower for kw in IGNORE_KEYWORDS) or
        re.search(r'\d{2,}|\+?\d[\d\-() ]{6,}', text) or
        re.search(r'\d+%|\d+:\d+', text) or
        len(text) < 3
    )


def clean_text(lines):
    all_lines = []
    for _, line_df in lines:
        text = " ".join(t.strip() for t in line_df["text"] if t.strip())
        if not text or is_noise_line(text):
            continue
        all_lines.append(text)
    return all_lines