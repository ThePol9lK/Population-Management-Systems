import os


class Config:
    """
    Класс Config содержит настройки для конфигурации приложения.
    Используется для хранения важных параметров безопасности,
    базы данных и других опций настройки.
    """

    # Ключ для защиты сессий и подписания данных (важно для безопасности).
    # Если переменная окружения SECRET_KEY не задана, используется значение по умолчанию.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

    # Настройки для базы данных
    # Переменная окружения DATABASE_URL содержит URL для подключения к базе данных.
    # Если переменная окружения не задана, используется SQLite база данных по умолчанию.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')

    # Отключаем отслеживание изменений в базе данных, чтобы избежать лишних уведомлений в логах.
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключаем отслеживание изменений, чтобы не было лишних уведомлений в логе.

    # Дополнительные настройки для производительности и безопасности
    # Отключаем логирование SQL-запросов. Включение этого параметра может замедлить работу приложения в продакшн-среде.
    SQLALCHEMY_ECHO = False

    # Настройка типа сессии для хранения данных сессии на файловой системе.
    # Может быть полезно для масштабируемости или хранения сессий на сервере.
    SESSION_TYPE = 'filesystem'

    # Настройки SMTP для Яндекса
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
