from tkinter import *
from tkinter import filedialog
import os ## *split filename from file extension (to be concitnue)
import PyPDF2
from PyPDF2 import PdfReader
import docx
from docx import Document
from tkinter import font

def replace_chars(text_value):
    replacements = {
        "á": "a", "â": "a", "ã": "a", "à": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "ô": "o", "õ": "o",
        "ú": "u",
        "Á": "A", "Â": "A", "Ã": "A", "À": "A",
        "É": "E", "Ê": "E",
        "Í": "I",
        "Ó": "O", "Ô": "O", "Õ": "O",
        "Ú": "U",
        "ç": "c", "Ç": "C",
        "WEBVTT": "", "0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "",
        ",": "", "!": "", "?": "", ":": "", ";": "", '"': "", ">": "", "_": "", "-": "", "'": "", "\n\n": "", "--": "", ".": ""
    }
    for old, new in replacements.items():
        text_value = text_value.replace(old, new)
    return text_value.strip()

def get_text():
    text_value = text_box.get("1.0", "end-1c")  # get text from start to end
    text_value = replace_chars(text_value)
    print("TextBox Value:", text_value)
    filename_without_extension = os.path.splitext(filename)[0]  # split filename and extensio
    with open(filename_without_extension + '.txt', 'w') as f:
        f.write(text_value) # write to a file with the same name but .txt extension

def clear_text():
    text_box.delete("1.0", "end")  # clear text from start to end

def select_file():
    global filename
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("vtt files", "*.vtt"),
                                                     ("txt files", "*.txt"), 
                                                     ("pdf files", "*.pdf"), 
                                                     ("doc files", "*.doc"),
                                                     ("all files", "*.*")))
    print("Selected file:", filename)
    if filename.endswith('.pdf'):
        pdf_file_obj = open(filename, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
        num_pages = pdf_reader.numPages
        text_value = ''
        for page in range(num_pages):
            page_obj = pdf_reader.getPage(page)
            text_value += page_obj.extractText()
        pdf_file_obj.close()
    elif filename.endswith('.doc'):
        doc = docx.Document(filename)
        text_value = ' '.join([paragraph.text for paragraph in doc.paragraphs])
    else:  # .txt or .vtt file
        with open(filename, 'r') as f:
            text_value = f.read()
    text_box.delete("1.0", "end")
    text_box.insert('end', text_value)

root = Tk()
root.geometry('500x400')
root.config(bg='grey75')

frame = Frame(root, bg='grey75')
frame.pack(pady=10, expand=True)

message = "Your initial text goes here"

# Define the font properties
#text_font = font.Font(family='Helvetica', size=12)

text_box = Text(frame, height=18, width=50, wrap='word') #, font=text_font)
text_box.insert('end', message)
text_box.pack(side=LEFT, expand=True)

scrollbar = Scrollbar(frame, command=text_box.yview)
scrollbar.pack(side="right", fill="y")

text_box.config(yscrollcommand=scrollbar.set)

button_frame = Frame(root, bg='grey75')
button_frame.pack(pady=10)

button_frame = Frame(root, bg='grey75')
button_frame.pack(pady=10)

select_file_button = Button(button_frame, text="Select File", command=select_file, width=12, height=2, 
                            bg='grey15', fg='white', font=("Helvetica", "11", "bold"), relief='raised')
select_file_button.pack(side="left", padx=10)  # add horizontal padding

print_button = Button(button_frame, text="Print & Save", command=get_text, width=12, height=2, 
                      bg='grey15', fg='white', font=("Helvetica", "11", "bold"),  relief='raised' )
print_button.pack(side="left", padx=10)  # add horizontal padding

clear_button = Button(button_frame, text="Clear", command=clear_text, width=12, height=2, 
                      bg='grey15', fg='white', font=("Helvetica", "11", "bold"), relief='raised')
clear_button.pack(side="left", padx=10)

root.mainloop()