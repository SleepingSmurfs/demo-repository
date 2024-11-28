from flask import Flask, request, render_template, jsonify
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import faker
import faker_commerce
import json
import boto3
import uuid
import os
import glob
from botocore.exceptions import NoCredentialsError
from botocore.client import Config
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
import random
import string
import pdfplumber
from supabase import create_client, Client
from pydantic import BaseModel

app = Flask(__name__)
app.secret_key = 'mine' 

# def create_supabase_client() -> Client:
#     supabase_url = os.getenv('https://lplyqcgkevdmibkeyebz.supabase.co')
#     supabase_anon_key = os.getenv('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxwbHlxY2drZXZkbWlia2V5ZWJ6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMjY5ODEwMSwiZXhwIjoyMDQ4Mjc0MTAxfQ.XTtQbzqPDCKp3whOnh43QZ1ZEtwsuC1yChZW1OQiW20Y')
#     return create_client(supabase_url, supabase_anon_key)

# # class Item(BaseModel):
# #     id: str
# #     name: str
# #     description: str

# # @app.post("/items/")
# # async def create_item(item: Item):
# #     supabase = create_supabase_client()
    
# #     # Добавляем данные в таблицу "items"
# #     response = supabase.table('items').insert(item.dict()).execute()

# #     if response.status_code != 201:
# #         raise HTTPException(status_code=response.status_code, detail=response.data)

# #     return response.data
def add_entries_to_vendor_table(supabase, vendor_count):
    fake = Faker()
    foreign_key_list = []
    fake.add_provider(faker_commerce.Provider)
    main_list = []
    for i in range(vendor_count):
        value = {'vendor_name': fake.company(), 'total_employees': fake.random_int(40, 169),
                 'vendor_location': fake.country()}

        main_list.append(value)
    data = supabase.table('Vendor').insert(main_list).execute()
    data_json = json.loads(data.json())
    data_entries = data_json['data']
    for i in range(len(data_entries)):
        foreign_key_list.append(int(data_entries[i]['vendor_id']))
    return foreign_key_list


def add_entries_to_product_table(supabase, vendor_id):
    fake = Faker()
    fake.add_provider(faker_commerce.Provider)
    main_list = []
    iterator = fake.random_int(1, 15)
    for i in range(iterator):
        value = {'vendor_id': vendor_id, 'product_name': fake.ecommerce_name(),
                 'inventory_count': fake.random_int(1, 100), 'price': fake.random_int(45, 100)}
        main_list.append(value)
    data = supabase.table('Product').insert(main_list).execute()


def main():
    vendor_count = 10
    load_dotenv()
    url: str = os.environ.get("https://lplyqcgkevdmibkeyebz.supabase.co")
    key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxwbHlxY2drZXZkbWlia2V5ZWJ6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMjY5ODEwMSwiZXhwIjoyMDQ4Mjc0MTAxfQ.XTtQbzqPDCKp3whOnh43QZ1ZEtwsuC1yChZW1OQiW20")
    supabase: Client = create_client(url, key)
    fk_list = add_entries_to_vendor_table(supabase, vendor_count)
    for i in range(len(fk_list)):
        add_entries_to_product_table(supabase, fk_list[i])

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

settings_folder = 'settings_for_bot'
app.config['UPLOAD_FOLDER'] = 'uploads' 
users = {
    "admin": "password123",
    "user": "userpass"
}

#это не трогаем
def get_lis_of_models():
        # Получаем список всех файлов с расширением .json в папке
    json_files = glob.glob(os.path.join(settings_folder, '*.json'))

    # Извлекаем только имена файлов (без пути)
    json_file_names = [os.path.splitext(os.path.basename(file))[0] for file in json_files]
    return json_file_names


#это не трогаем
def save_settings(model, settings):
    with open(f"/settings_folder/{model}.json", 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

#это не трогаем
def load_settings(model_name):
    settings_file = os.path.join(settings_folder, f"{model_name}.json")
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'welcome_message': "Здравствуйте! Как я могу помочь?",
            'error_message': "Извините, я не понял ваш запрос.",
            'user_icon': 'user_icon.png',
            'bot_icon': 'bot_icon.png',
            'font_family': 'Arial',
            'font_size': '14px',
            'text_color': '#000000',
            'background_color': '#FFFFFF',
            'button_color': '#4CAF50',
            'chat_background_color': '#F1F1F1',
            'bot_message_color': '#007BFF',
            'user_message_color': '#333333',
            'bot_bg_message_color': '#4CAF50',
            'user_bg_message_color': '#4CAF50',
        }
    
#это не трогаем
@app.route('/load_settigs/<model_name>', methods=['GET'])
def load_settings_route(model_name):
    settings = load_settings(model_name)
    return jsonify(settings)
    
#это не трогаем    
@app.route("/", methods=["GET", "POST"])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    model_name = request.form.get('model', 'bot1')  # По умолчанию 'default'
    settings = load_settings(model_name)
    list_of_models = get_lis_of_models()

    if request.method == "POST":
        settings['welcome_message'] = request.form.get('welcome_message')
        settings['error_message'] = request.form.get('error_message')
        settings['user_icon'] = request.form.get('user_icon')
        settings['bot_icon'] = request.form.get('bot_icon')
        settings['font_family'] = request.form.get('font_family')
        settings['font_size'] = request.form.get('font_size')
        settings['text_color'] = request.form.get('text_color')
        settings['background_color'] = request.form.get('background_color')
        settings['button_color'] = request.form.get('button_color')
        settings['chat_background_color'] = request.form.get('chat_background_color')
        settings['bot_message_color'] = request.form.get('bot_message_color')
        settings['user_message_color'] = request.form.get('user_message_color')
        settings['bot_bg_message_color'] = request.form.get('bot_bg_message_color')
        settings['user_bg_message_color'] = request.form.get('user_bg_message_color')
        model = request.form.get('model')

        save_settings(model, settings)
        return render_template('settings_page.html', settings=settings)

    return render_template('settings_page.html', settings=settings, list_of_models=list_of_models)

#это не трогаем
@app.route("/upload")
def upload():
    return render_template('upload.html')  # Страница для загрузки файлов

#это не трогаем
@app.route("/bot")
def bot():
    model_name = request.form.get('model', 'bot1')  # По умолчанию 'default'
    settings = load_settings(model_name)
    list_of_models = get_lis_of_models()
    return render_template('bot_page.html', settings=settings)  # Страница для загрузки файлов

#функция получения файла
@app.route("/upload_file", methods=["POST"])
def upload_file():
    # Проверяем, был ли файл в запросе
    if 'file_input' not in request.files:
        #если нас нае.. то выдаем ошибку
        return jsonify({"success": False, "error": "Нет файла в запросе"}), 400

    #полуение файл из реквеста
    print(request)
    file = request.files['file_input']
    model = request.form.get('model')
    print(model)

    # Проверка, был ли файл выбран
    if file.filename == '':
        #если нас нае.. то выдаем ошибку
        return jsonify({"success": False, "error": "Не выбран файл"}), 400



    if file:
        # Генерация уникального имени для файла
        # Генерация безопасного имени файла
        filename = file.filename
        print(filename)
        file_ext = os.path.splitext(filename)[1].lower()

        # Установка пути в зависимости от модели
        base_upload_dir = os.path.join(os.getcwd(), 'uploads')  # Корневая директория для всех файлов
        model_upload_dir = os.path.join(base_upload_dir, model)  # Директория для конкретной модели

        # Создание директории для модели, если её нет
        os.makedirs(model_upload_dir, exist_ok=True)
        file_path = os.path.join(model_upload_dir, filename)
        try:
            file.save(file_path)
        except Exception as e:
            return jsonify({"success": False, "error": f"Ошибка сохранения файла: {str(e)}"}), 500
        file_ext = os.path.splitext(file.filename)[1].lower()
        print(file_ext)
        pars_file(file.filename, model, file_ext)
        

        #тут модно прописать функцию, чтобы она брала этот файл и для определенной версии модели чет делала

        return jsonify({"success": True, "message": f"Файл  успешно загружен!"})

    return jsonify({"success": False, "error": "Ошибка при загрузке файла"}), 500



#создание модели
@app.route('/create_model', methods=['POST'])
def create_model():
    #получаем данные из реквеста
    data = request.get_json()
    model_name = data.get("model_name")
    
    #если название оказалось пустым
    if not model_name:
        return jsonify({"error": "Название модели не может быть пустым"}), 400

    
    try:
        os.makedirs(settings_folder, exist_ok=True)  # Создание папки, если её нет
        #сгружается конфигурация кастомизации
        config_data = {
            "welcome_message": "new bot",
            "error_message": "new bot",
            "user_icon": "user_icon.png",
            "bot_icon": "bot_icon.png",
            "font_family": "Arial",
            "font_size": "122",
            "text_color": "#ffffff",
            "background_color": "#ffffff",
            "button_color": "#ffffff",
            "chat_background_color": "#ffffff",
            "bot_message_color": "#ffffff",
            "user_message_color": "#ffffff",
            "bot_bg_message_color": "#ffffff",
            "user_bg_message_color": "#ffffff",
            "bot_background_image": ""
        }
        #и сохраняется в
        with open(f"{settings_folder}/{model_name}.json", "w", encoding="utf-8") as config_file:
            json.dump(config_data, config_file, ensure_ascii=False, indent=4)
        
        #ответ на фронт
        return jsonify({"message": "Модель создана успешно"}), 201
    #обработка ошибок
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#страница логина на сраницу кастомизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #получаем данные из реквеста
        username = request.form['username']
        password = request.form['password']
        
        #если совпало
        if username in users and users[username] == password:
            session['username'] = username  # Сохраняем пользователя в сессии
            return redirect(url_for('index'))  # Перенаправление на страницу настроек
        else:
            flash("Неверное имя пользователя или пароль")  # Сообщение об ошибке
    
    return render_template('login.html')  # Рендерим форму логина


@app.route('/inside_login', methods=['GET', 'POST'])
def inside_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username  # Сохраняем пользователя в сессии
            return redirect(url_for('inside_chat_bot'))  # Перенаправление на страницу настроек
        else:
            flash("Неверное имя пользователя или пароль")  # Сообщение об ошибке
    
    return render_template('inside_login.html')  # Рендерим форму логина

@app.route("/inside_chat_bot")
def inside_chat_bot():
    model_name = request.form.get('model', 'bot1')  # По умолчанию 'default'
    settings = load_settings(model_name)
    list_of_models = get_lis_of_models()
    return render_template('inside_chat_bot.html', settings=settings, list_of_models=list_of_models)  # Страница для загрузки файлов

@app.route('/send_message', methods=['POST'])
def send_message():
    print("jwrhfkjdhg")
    data = request.get_json()
    user_message = data.get("message")
    model = data.get("model")

    if not user_message:
        return jsonify({"error": "Сообщение не может быть пустым"}), 400

    # Логика ответа бота
    bot_response = f"Ваше сообщение: '{user_message}' получено!"

    # Здесь можно добавить сложную логику или подключение модели для ответа

    return jsonify({"response": bot_response}), 200

    




def pars_file(filename, model, file_ext):
    print("parsing start")
    txt_file = f"{current_dir}/ml/{model}/{filename}.txt"
    input_file = f'{current_dir}/uploads/{model}/{filename}'

    if file_ext == ".pdf":
        print("parsing start1")
        print(input_file )
        with open(txt_file, "w", encoding="utf-8", errors="replace") as text_file:
            with pdfplumber.open(input_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    print(text)
                    if text:
                        print(text)
                        text_file.write(text + "\n")

    elif file_ext == ".docx":
        print("parsing start2")
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Файл {input_file} не найден.")

        doc = Document(input_file)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
    elif file_ext == ".csv":
        csv_file = input_file

        with open(txt_file, "w") as my_output_file:
            with open(csv_file, "r") as my_input_file:
                [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
        my_output_file.close()

    elif file_ext == ".json":
        json_file = input_file

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

    elif file_ext == ".sql":
        sql_file = input_file
        with open(sql_file, 'r', encoding='utf-8') as f:
            with open(txt_file, 'w', encoding='utf-8') as output:
                output.write(f.read())

    elif file_ext == ".gz":
        gz_file = input_file

        with gzip.open(gz_file, 'rt', encoding='utf-8') as f:
            with open(txt_file, 'w', encoding='utf-8') as output:
                output.write(f.read())

    elif file_ext == ".tar":
        tar_file = input_file
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

    elif file_ext == ".zip":
        zip_file = input_file
        with zipfile.ZipFile(zip_file, 'r') as input:
            with open(txt_file, 'w', encoding='utf-8') as f:
                # Перебор всех файлов в архиве
                for member in input.infolist():
                    if member.is_file():
                        f.write(f"--- Содержимое файла: {member.filename} ---\n")
                        f.write(input.read(member.filename).decode('utf-8', errors='ignore'))
                        f.write("\n\n")
                input.close()


def parc_url(model, url):
    name = generate_random_name()
    
    
    txt_file = f"/ml/{model}/{name}.txt"
    with open(txt_file, "a", encoding="utf-8") as file:

        html_code = str(urlopen(url).read(),'utf-8')
        soup = BeautifulSoup(html_code, "html.parser")

        s = soup.find('title').text
        print(s)

        for par in soup.find_all('p'):
            file.write(par.text + '\n')



def generate_random_name(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=length))






if __name__ == "__main__":
    app.run(debug=True)
