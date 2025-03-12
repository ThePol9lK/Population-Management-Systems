from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask.cli import with_appcontext
import click
from werkzeug.security import generate_password_hash
from flask_mail import Mail

from config import Config

# Инициализация объектов расширений для работы с базой данных, миграциями и аутентификацией
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app():
    """
    Создает экземпляр Flask-приложения и настраивает его.

    Этот метод инициализирует необходимые расширения Flask, настраивает
    пути для логина и регистрирует команду CLI для создания пользователя.
    """
    # Создаем Flask-приложение
    app = Flask(__name__)
    # Загружаем настройки из объекта Config
    app.config.from_object(Config)

    # Инициализация расширений с Flask-приложением
    db.init_app(app)  # Инициализация базы данных
    migrate.init_app(app, db)  # Инициализация миграций
    login_manager.init_app(app)  # Инициализация аутентификации
    mail.init_app(app)  # Инициализируем Mail

    login_manager.login_view = "auth.login"  # Указываем на маршрут login в Blueprint `auth`

    from app.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='')  # Регистрация Blueprint для авторизации

    # Регистрируем команду CLI для создания пользователей
    app.cli.add_command(create_user)

    return app


@login_manager.user_loader
def load_user(user_id):
    """
    Функция, которая загружает пользователя по его id для Flask-Login.

    :param user_id: Идентификатор пользователя
    :return: Объект пользователя или None, если не найден
    """
    from app.models import User
    return User.query.get(int(user_id))


# Команда для создания пользователя через CLI
@click.command(name='create-user')
@with_appcontext  # Используем с контекстом приложения Flask
def create_user():
    """
    Команда для создания нового пользователя в базе данных через CLI.

    С помощью этой команды можно создать нового пользователя с логином,
    паролем и ролью (комендант/админ). Пароль будет хеширован перед сохранением.
    """
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    role = input("Введите роль (комендант/админ): ").lower()

    if role not in ['комендант', 'админ']:
        print("Некорректная роль")
        return

    password_hash = generate_password_hash(password)

    from app.models import User

    user = User(login=login, password_hash=password_hash, role=role)

    try:
        db.session.add(user)
        db.session.commit()
        print(f"Пользователь {login} успешно добавлен!")
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при добавлении пользователя: {e}")
