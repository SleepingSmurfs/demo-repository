from docx import Document
import os
model= "model1"
filename = "test"
file_ext = "docx"

txt_file = f"/Users/gk/Desktop/***tons/Хакатон Т1 мск/v2/ml/{model}/{filename}.txt"
input_file = f'/Users/gk/Desktop/***tons/Хакатон Т1 мск/v2/uploads/{model}/{filename}.{file_ext}'
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Файл {input_file} не найден.")

doc = Document(input_file)
text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

with open(txt_file, 'w', encoding='utf-8') as f:
    f.write(text)