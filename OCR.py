import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import io

def preprocess_image(image):
    image = image.convert('L')  # 灰度
    enhancer = ImageEnhance.Contrast(image) # 对比度
    image = enhancer.enhance(2)
    image = image.point(lambda p: p > 128 and 255)  #二值化
    # image = image.filter(ImageFilter.MedianFilter(size=3))  # 滤波
    return image

def extract_text_from_pdf(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        
        if page_text.strip():
            # 如果页面包含文本内容，直接提取文本
            text += page_text
        else:
            # 如果页面不包含文本内容，使用OCR提取图片中的文字
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                # 预处理图像
                image = preprocess_image(image)
                ocr_text = pytesseract.image_to_string(image, lang="chi_sim")
                text += ocr_text

    # 删除多余的空格和空白行，并将所有文字合并成一行
    lines = text.splitlines()
    non_empty_lines = [line.replace(" ", "",).strip() for line in lines if line.strip()]
    single_line_text = "".join(non_empty_lines)

    # 将文本保存到文件中
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(single_line_text)


pdf_path = "./PDF/paper1.pdf"
output_path = "./TXT/paper2.txt"
pdf_text = extract_text_from_pdf(pdf_path, output_path)
