import pdfplumber
import pytesseract
from PIL import Image

def extract_text(file_path, file_type):
    text = ""

    if file_type == "pdf":
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    else:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    return text
