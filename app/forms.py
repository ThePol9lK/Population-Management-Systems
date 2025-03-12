from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp, EqualTo


class LoginForm(FlaskForm):
    """
    Форма для авторизации пользователя.

    Поля:
    - login: Логин пользователя (обязательное поле, длина от 4 до 80 символов).
    - password: Пароль пользователя (обязательное поле).
    """
    login = StringField('Логин', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Пароль', validators=[DataRequired()])


class BuildingForm(FlaskForm):
    """
    Форма для добавления нового здания.

    Поля:
    - name: Наименование здания (обязательное поле).
    - num_floors: Количество этажей (обязательное поле, минимум 1).
    - num_rooms_per_floor: Количество комнат на этаже (обязательное поле, минимум 1).
    - num_beds_per_room: Количество койок в комнате (обязательное поле, минимум 1).
    """
    name = StringField('Наименование здания', validators=[DataRequired()])
    num_floors = IntegerField('Количество этажей', validators=[DataRequired(), NumberRange(min=1)])
    num_rooms_per_floor = IntegerField('Количество комнат на этаже', validators=[DataRequired(), NumberRange(min=1)])
    num_beds_per_room = IntegerField('Количество койок в комнате', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Добавить')


class EmployeeForm(FlaskForm):
    """
    Форма для добавления нового сотрудника.

    Поля: - full_name: ФИО сотрудника (обязательное поле, длина от 1 до 255 символов).
    - badge_number: Табельный номер сотрудника (обязательное поле, длина 8 символов, соответствует формату 2 буквы + 6 цифр).
    - passport_series: Серия паспорта (обязательное поле, длина 4 символа).
    - passport_number: Номер паспорта (обязательное поле, длина 6 символов).
    - passport_issue_date: Дата выдачи паспорта (обязательное поле).
    - has_patent: Наличие патента (необязательное поле, checkbox).
    """
    full_name = StringField('ФИО', validators=[DataRequired(), Length(min=1, max=255)])
    badge_number = StringField('Табельный номер', validators=[
        DataRequired(),
        Length(min=8, max=8),
        Regexp('^[A-Za-z]{2}[0-9]{6}$', message="Табельный номер должен состоять из 2 букв и 6 цифр.")
    ])
    passport_series = StringField('Серия паспорта', validators=[DataRequired(), Length(min=4, max=4)])
    passport_number = StringField('Номер паспорта', validators=[DataRequired(), Length(min=6, max=6)])
    passport_issue_date = DateField('Дата выдачи паспорта', validators=[DataRequired()])
    has_patent = BooleanField('Наличие патента')
    submit = SubmitField('Добавить')


class UserForm(FlaskForm):
    """
    Форма для создания нового пользователя (учетной записи).

    Поля:
    - login: Логин пользователя (обязательное поле, длина от 4 до 100 символов).
    - password: Пароль пользователя (обязательное поле, минимум 6 символов).
    - confirm_password: Подтверждение пароля (обязательное поле, должно совпадать с полем password).
    - role: Роль пользователя (обязательное поле, длина от 3 до 20 символов).
    """
    login = StringField('Логин', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    role = StringField('Роль', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Добавить учетную запись')
