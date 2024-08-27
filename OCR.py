import fitz  
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import io
import os

def preprocess_image(image):
    image = image.convert('L')  
    enhancer = ImageEnhance.Contrast(image) 
    image = enhancer.enhance(2)
    image = image.point(lambda p: p > 128 and 255)  
    return image

def extract_text_from_pdf(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        
        if page_text.strip():
            text += page_text
        else:
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))

                image = preprocess_image(image)
                ocr_text = pytesseract.image_to_string(image, lang="chi_sim")
                text += ocr_text

    lines = text.splitlines()
    non_empty_lines = [line.replace(" ", "",).strip() for line in lines if line.strip()]
    single_line_text = "".join(non_empty_lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(single_line_text)

def convert_all_pdfs(pdf_folder, txt_folder):
    os.makedirs(txt_folder, exist_ok=True)
    
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            output_filename = filename.replace(".pdf", ".txt")
            output_path = os.path.join(txt_folder, output_filename)
            
            extract_text_from_pdf(pdf_path, output_path)
            print(f"Converted {pdf_path} to {output_path}")

# 设置PDF文件夹和TXT文件夹路径
pdf_folder = "../PDF"
txt_folder = "../TXT"

convert_all_pdfs(pdf_folder, txt_folder)
