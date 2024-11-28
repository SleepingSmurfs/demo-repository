from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Путь к файлу настроек
settings_file = 'settings.json'

# Загружаем настройки из файла
def load_settings():
    try:
        with open(settings_file, 'r') as f:
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
        }

# Сохраняем настройки в файл
def save_settings(settings):
    with open(settings_file, 'w') as f:
        json.dump(settings, f)

@app.route("/", methods=["GET", "POST"])
def index():
    settings = load_settings()

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

        save_settings(settings)

    return render_template('settings_page.html', settings=settings)

@app.route('/bot')
def bot():
    settings = load_settings()
    # Страница с основным чатом бота
    return render_template('bot_page.html', settings=settings)

if __name__ == "__main__":
    app.run(debug=True)
