# Tesseract Optical Character Recognition
Make text character recognition using the python package, namely [pytesseract](https://pypi.org/project/pytesseract/) from [Tesseract](https://tesseract-ocr.github.io/).

## Install the pytesseract package (using windows):
- Download [TesseractEXE](https://tesseract-ocr.github.io/tessdoc/Downloads) (<i>Go to Binaries for Windows</i>).
- Install and envorinment path on your windows, and envorinment too path tessdata in tesseract dir.
- After that, check in your command prompt with this ```tesseract -v``` (<i>Result: show tesseract version</i>).
- Next, install pytesseract packages with this ```pip install pytesseract```.
- Done it. See more setting in my code file, there are some comments that are considered for setting up the tesseract so that it can run.
For more information check:
1. (pyimagesearch)[https://www.pyimagesearch.com/2017/07/03/installing-tesseract-for-ocr/]
1. (tesseract-OCR github)[https://github.com/tesseract-ocr/tessdata]
1. (murtazahassan)[https://www.murtazahassan.com/text-detection-opencv/]

## Add tesseract language
To adjust the text image that you provide.

Download [here](https://github.com/tesseract-ocr/tessdata).

After that, move to dir tessdata on tesseract path.
