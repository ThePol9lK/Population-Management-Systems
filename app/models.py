from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    Модель пользователя для хранения информации о пользователях.

    Поля:
    - id: Уникальный идентификатор пользователя (первичный ключ).
    - login: Логин пользователя (уникальное значение).
    - password_hash: Хэш пароля.
    - is_active: Флаг активности пользователя (по умолчанию True).
    - role: Роль пользователя (обязательное поле).
    """

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), nullable=False)

    def get_id(self):
        """
        Возвращает идентификатор пользователя как строку, что требуется для Flask-Login.
        """
        return str(self.id)


class Employee(db.Model):
    """
    Модель сотрудника для хранения информации о сотрудниках.

    Поля:
    - id: Уникальный идентификатор сотрудника (первичный ключ).
    - full_name: Полное имя сотрудника (обязательное поле).
    - badge_number: Табельный номер сотрудника (уникальное значение).
    - passport_series: Серия паспорта сотрудника (обязательное поле).
    - passport_number: Номер паспорта сотрудника (обязательное поле).
    - passport_issue_date: Дата выдачи паспорта (обязательное поле).
    - has_patent: Наличие патента (по умолчанию False).
    """

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    badge_number = db.Column(db.String(8), unique=True, nullable=False)
    passport_series = db.Column(db.String(4), nullable=False)
    passport_number = db.Column(db.String(6), nullable=False)
    passport_issue_date = db.Column(db.Date, nullable=False)
    has_patent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """
        Возвращает строковое представление сотрудника, включая его полное имя.
        """
        return f"<Employee {self.full_name}>"


class Building(db.Model):
    """
    Модель здания для хранения информации о зданиях.

    Поля:
    - id: Уникальный идентификатор здания (первичный ключ).
    - name: Наименование здания (обязательное поле).
    - floors: Связь с этажами этого здания (один ко многим).
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    floors = db.relationship('Floor', backref='building', lazy=True)

    def __repr__(self):
        """
        Возвращает строковое представление здания с его наименованием.
        """
        return f"<Building {self.name}>"


class Floor(db.Model):
    """
    Модель этажа для хранения информации об этажах зданий.

    Поля:
    - id: Уникальный идентификатор этажа (первичный ключ).
    - number: Номер этажа (обязательное поле).
    - building_id: Идентификатор здания, к которому относится этот этаж (внешний ключ).
    - rooms: Связь с комнатами на этом этаже (один ко многим).
    """

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)
    rooms = db.relationship('Room', backref='floor', lazy=True)

    def __repr__(self):
        """
        Возвращает строковое представление этажа, включая номер этажа и наименование здания.
        """
        return f"<Floor {self.number} of {self.building.name}>"


class Room(db.Model):
    """
    Модель комнаты для хранения информации о комнатах на этажах.

    Поля:
    - id: Уникальный идентификатор комнаты (первичный ключ).
    - number: Номер комнаты (обязательное поле).
    - floor_id: Идентификатор этажа, к которому относится эта комната (внешний ключ).
    - beds: Связь с койками в этой комнате (один ко многим).
    """

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.id'), nullable=False)
    beds = db.relationship('Bed', backref='room', lazy=True)

    @property
    def is_available(self):
        """
        Проверка, что в комнате есть хотя бы одна свободная койка.

        Возвращает True, если в комнате есть свободная койка.
        """
        return any(not bed.is_occupied for bed in self.beds)

    def __repr__(self):
        """
        Возвращает строковое представление комнаты с её номером и номером этажа.
        """
        return f"<Room {self.number} on floor {self.floor.number}>"


class Bed(db.Model):
    """
    Модель койки для хранения информации о койках в комнатах.

    Поля:
    - id: Уникальный идентификатор койки (первичный ключ).
    - is_occupied: Флаг занятости койки (по умолчанию False).
    - check_in_date: Дата заселения на койку.
    - check_out_date: Дата выселения с койки.
    - room_id: Идентификатор комнаты, к которой относится эта койка (внешний ключ).
    """

    id = db.Column(db.Integer, primary_key=True)
    is_occupied = db.Column(db.Boolean, default=False)
    check_in_date = db.Column(db.DateTime)
    check_out_date = db.Column(db.DateTime)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    def __repr__(self):
        """
        Возвращает строковое представление койки, указывая, занята она или нет.
        """
        return f"<Bed {'Occupied' if self.is_occupied else 'Available'}>"
