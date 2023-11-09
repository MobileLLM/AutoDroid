from PIL import Image
import pytesseract

def ocr_output(image_path):
    # 打开图像文件
    img = Image.open(image_path)

    # 使用Tesseract进行OCR处理
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')

    # 去除结果中的空白字符
    text = text.strip()

    # 如果文本长度为0，则认为没有识别到文字，返回空字符串
    if len(text) == 0:
        return ""
    else:
        # 返回识别到的文本
        return text

# 使用该函数并传入图像路径
result = ocr_output('/home/wenhao/Desktop/autodroid/AutoDroid-sys-taskpolicyv2/output/calendar/views/view_28e2dc4401f32750dc506e977256a3cf.png')

# 输出结果
print(result if result else "没有检测到文字。")
