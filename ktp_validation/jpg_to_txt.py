from PIL import Image

import numpy as np

import io
import os
import cv2
import tesserocr

def convertPIL(img):
    # input: image in PIL
    # output: img in numpy array so opencv can process it

    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    return img

def preprocessing_ktp(img):

    if not isinstance(img, np.ndarray):
        img = convertPIL(img)
    
    alpha = 4.0
    beta = -160
    new = alpha * img + beta
    new = np.clip(new, 0, 255).astype(np.uint8)
    kernel = np.ones((2, 2), np.uint8)
    kernel1 = np.ones((1, 1), np.uint8)
    new = cv2.erode(new, kernel, iterations=1)
    new = cv2.erode(new, kernel1, iterations=12)
    new = cv2.blur(new, (2, 2))
    # ret,new = cv2.threshold(new,100,255,cv2.THRESH_TOZERO)
    new = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)
    ret, new = cv2.threshold(new, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return new

def convert_jpg_to_txt(image_path, output_path):
    image = Image.open(image_path)
    
    processed_image = preprocessing_ktp(image)
    
    text = tesserocr.image_to_text(Image.fromarray(processed_image), lang='ind', path='ktp_validation/model/')

    with io.open(output_path + 'ocr.txt', mode='w', encoding='utf8') as file:
        file.write(text)

    with io.open(output_path + 'ocr_NIK.txt', mode='w', encoding='utf8') as file:
        file.write(tesserocr.image_to_text(Image.fromarray(processed_image), lang='ktp', path='ktp_validation/model/'))

# Main function, will loop through the parent document and convert all of the pdf files
def main(parent_directory):

    # Create a directory called output to store the result (.txt files)
    os.makedirs(parent_directory + '/output')
        
    # List all of the images files in a directory jpg
    files = os.listdir(parent_directory)
    
    for file in files:
        if 'ktp' in file.lower():
            convert_jpg_to_txt(parent_directory + file, parent_directory + 'output/')
    # Parallel(n_jobs=num_cores, prefer='threads')(delayed(send_to_google_vision)(file, parent_directory) for file in files)
