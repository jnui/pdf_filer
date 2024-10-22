
## READ IMAGE FORMAT PDF FILES, USE OCR TO FIND TEXT AND RE-FILE INTO FOLDERS

This script was made to speed up the time it takes us to look at scanned documents and put the pdf's into a folder .
Note scanned documents are usually saved as images inside a pdf.
In our situation we looked for addresses and added a name in front of the address.
For example, we looked for "123 Main", and added "Smith"
the list.txt file has tuples in the format of ('Smith','123 Main')
The script file will go through all the pdf files found in the "scans" folder and look for matching text.

# Setup

I used VS Code, the pdf2Image module did not install well. (wrapper for poppler).
I found that the best way was to create a virtual environment in vs code, then manually install modules with PIP
e.g. in terminal
python -m venv venv
choose "yes" to the prompt
pip install pdf2image
pip install pytesseract
pip install -r requirements.txt




### Overview

	project
	|- README          # the top level description of content (this doc)
	|- LICENSE         # the license for this project
	|- refile4.py       # the main script, run this script
	|- list.txt         # a list of tuples that contain text to match, and a label (2nd item is text to match)
	|- requirements.txt                 # requirements.txt	
	|- scans/           # folder where script looks for pdf files, it is also where new folders are made
	| |- scantest.pdf   # pdf that is in image format taken from a scanner, has the text in it
  |

	
