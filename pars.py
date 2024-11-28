from pypdf import PdfReader
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
from docx import Document
import csv
import json
import tarfile
import zipfile
import gzip


filename = 'demo2' # name of the pdf file no extension

with open(f"{filename}.txt", "w", encoding="utf-8", errors="replace") as text_file:
    with open(f'{filename}.pdf', 'rb') as pdf_file:

        reader = PdfReader(pdf_file)

        for page in reader.pages:
            text = page.extract_text()
            text_file.write(text)



# открываем текстовый файл, куда будем добавлять заголовки
with open("url_file.txt", "a", encoding="utf-8") as file:

    url = "https://thecode.media/parsing/"

    html_code = str(urlopen(url).read(),'utf-8')
    soup = BeautifulSoup(html_code, "html.parser")

    s = soup.find('title').text
    print(s)

    for par in soup.find_all('p'):
        file.write(par.text + '\n')


def convert_docx_to_txt(input_file, output_file):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Файл {input_file} не найден.")

    doc = Document(input_file)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

input_docx = "12.docx"
output_txt = "output.txt"

try:
    convert_docx_to_txt(input_docx, output_txt)
except FileNotFoundError as e:
    print(f"Ошибка: {e}")








def export_csv(csv_file, txt_file):
    with open(txt_file, "w") as my_output_file:
        with open(csv_file, "r") as my_input_file:
            [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()


def export_json(json_file, txt_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Запись данных в TXT-файл
    with open(txt_file, 'w', encoding='utf-8') as f:
        if isinstance(data, dict):
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
        elif isinstance(data, list):
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False, indent=4))
                f.write("\n")
        else:
            f.write(str(data))






            
            




def export_sql(sql_file, txt_file):
    with open(sql_file, 'r', encoding='utf-8') as f:
        with open(txt_file, 'w', encoding='utf-8') as output:
            output.write(f.read())




def export_gz(gz_file, txt_file):
    with gzip.open(gz_file, 'rt', encoding='utf-8') as f:
        with open(txt_file, 'w', encoding='utf-8') as output:
            output.write(f.read())







def export_tar(tar_file, txt_file):
    with tarfile.open(tar_file, 'r') as input:
        with open(txt_file, 'w', encoding='utf-8') as f:
            # Перебор всех файлов в архиве
            for member in input.getmembers():
                if member.isfile():
                    f.write(f"--- Содержимое файла: {member.name} ---\n")

                    f = input.extractfile(member)
                    content = f.read().decode('utf-8', errors='ignore')
                    f.write(content)
                    f.write("\n\n")
                    
            input.close()


def export_zip(zip_file, txt_file):
    with zipfile.ZipFile(zip_file, 'r') as input:
        with open(txt_file, 'w', encoding='utf-8') as f:
            # Перебор всех файлов в архиве
            for member in input.infolist():
                if member.is_file():
                    f.write(f"--- Содержимое файла: {member.filename} ---\n")
                    f.write(input.read(member.filename).decode('utf-8', errors='ignore'))
                    f.write("\n\n")
            input.close()