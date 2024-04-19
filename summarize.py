import requests
import tkinter as tk
from tkinter import filedialog, scrolledtext
from PyPDF2 import PdfReader
import os
from transformers import pipeline
import io

def upload_pdf():
    file_path = filedialog.askopenfilename()
    if file_path:
        files = {'file': open(file_path, 'rb')}
        response = requests.post('http://localhost:8000/upload', files=files)
        data = response.json()
        file_path = data.get('file_path')
        if file_path:
            # Read the contents of the uploaded file
            with open(file_path, 'rb') as f:
                pdf_contents = f.read()
            # Get summaries directly from text contents
            model1_summary = get_model_summary1(pdf_contents)
            model2_summary = get_model_summary2(pdf_contents)
            # Update tkinter GUI with summaries
            
            
            model1_text.insert(tk.END, model1_summary)
            model2_text.insert(tk.END, model2_summary)
            root.update()  
            
def get_model_summary1(pdf_contents):
    summarizer = pipeline("summarization", model="google-t5/t5-base", tokenizer="google-t5/t5-base", framework="tf")
    text = extract_text_from_pdf(pdf_contents)
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def get_model_summary2(pdf_contents):
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")
    text = extract_text_from_pdf(pdf_contents)
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def extract_text_from_pdf(pdf_contents):
    with io.BytesIO(pdf_contents) as stream:
        pdf_reader = PdfReader(stream)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


# Create a simple GUI
root = tk.Tk()
root.title('PDF Summarization')

# Header
header = tk.Label(root, text='PDF Summarization', font=('Helvetica', 16, 'bold'))
header.pack()

# Upload Section
upload_label = tk.Label(root, text='Upload PDF:', font=('Helvetica', 12))
upload_label.pack()  # Pack the label widget
upload_button = tk.Button(root, text='Browse', command=upload_pdf)
upload_button.pack()

# Display Area for Model 1 Summary
model1_label = tk.Label(root, text='Model 1 Summary:', font=('Helvetica', 12))
model1_label.pack()
model1_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)  # Adjust width parameter
model1_text.pack()

# Display Area for Model 2 Summary
model2_label = tk.Label(root, text='Model 2 Summary:', font=('Helvetica', 12))
model2_label.pack()
model2_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)  # Adjust width parameter
model2_text.pack()



root.mainloop()
