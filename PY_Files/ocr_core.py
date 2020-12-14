import builtins
import call_tesseract
from PIL import Image as PilImage
import os

original_open = open
def bin_open(filename, mode='rb'): # note, the default mode now opens in binary
    return original_open(filename, mode)

# tesseract location must be changed in pytesseract     
def tes_ocr(img):
    bit64='C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    bit32='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    call_tesseract.call_tesseract.tesseract_path=bit64
    try:
        builtins.open = bin_open
        bts = call_tesseract.image_to_text(img)
    finally:
        builtins.open = original_open
    ocr_txt=(str(bts, 'cp1252', 'ignore'))
    return ocr_txt

    
def check_extract(extract,min_threshold):
    use=[]
    for word in extract:
        for letter in word:
            if letter.isalpha() or letter.isdigit():
                use.append(word)
        if len(use) > min_threshold:break
    return use

    
def ful_ocr(img_path):
    img = PilImage.open(img_path)
    img = img.convert('L')
    angle=0
    min_threshold=4
    while True:
        if angle<-360:
            ocr_txt=""
            break
        img=PilImage.open(img_path)
        ocr_txt = tes_ocr(img)
        extract=ocr_txt.split()
        use=check_extract(extract,min_threshold)
        if len(use) > min_threshold:
            img.save(img_path)
            break
        else:
           angle=angle-90
           img=img.rotate(angle, expand=True)
           img.save(img_path)
    return ocr_txt

    
def change_angle(img_path,angle):
    img=PilImage.open(img_path)
    img=img.rotate(angle)
    img.save(img_path)
         

#cordinates in % ratio of rows and columns
def ocr_extract(directory,filename):
    ocr_txt=""; org_path=directory+'/'+filename
    if filename[-4:].lower() in ['.jpg','.png']:
        ocr_txt=ful_ocr(org_path)
    return ocr_txt
