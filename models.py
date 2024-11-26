from database import db

class User(db.Model):
    __tablename__ = 'users'  # Имя таблицы в базе данных
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор пользователя
    username = db.Column(db.String(80), unique=True, nullable=False)  # Имя пользователя
    windows = db.relationship('Window', backref='user', lazy=True)  # Связь с окнами

    def __repr__(self):
        return f'<User  {self.username}>'

class Window(db.Model):
    __tablename__ = 'windows'  # Имя таблицы в базе данных
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор окна
    title = db.Column(db.String(120), nullable=False)  # Заголовок окна
    content = db.Column(db.Text, nullable=False)  # Содержимое окна
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Внешний ключ на пользователя

    def __repr__(self):
        return f'<Window {self.title}>'
