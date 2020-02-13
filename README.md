# ktp_validation

This web app can be used as KTP validator. User will input:
* KTP Image (`*.jpg`, `*.jpeg`, `*.png`)
* Name in KTP
* NIK
* Date of birth in KTP

The app will validate between user's inputs and the content of KTP. It uses OCR (Optical Character Recognition) to extract information from KTP.

## Prerequisite
To run this program, Tesseract must be installed on your computer. Follow this [link](https://github.com/tesseract-ocr/tesseract/wiki) for further info.

<br>

After install Tesseract, install the required library using command: 
`pip install -r requirements.txt`.

## Run Program
To run the app use:
`python run.py`