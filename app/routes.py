from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User, Room, Bed, Employee, Floor, Building
from app.forms import LoginForm, BuildingForm, EmployeeForm, UserForm
from app.utils import send_email

# Создаем Blueprint
bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Страница для входа пользователя. Если форма заполнена корректно,
    выполняется проверка логина и пароля. При успешном входе - редирект на главную страницу.
    При ошибке - отображается сообщение об ошибке.

    Метод:
    - GET: Отображает форму входа.
    - POST: Обрабатывает отправку формы.
    """
    form = LoginForm()

    if form.validate_on_submit():
        # Проверка логина и пароля
        user = User.query.filter_by(login=form.login.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Успешный вход!', 'success')
            return redirect(url_for('auth.index'))  # Перенаправление на главную страницу
        else:
            flash('Неверный логин или пароль', 'danger')

    return render_template('login.html', form=form)


@bp.route('/')
@login_required
def index():
    try:
        buildings = Building.query.options(
            db.joinedload(Building.floors).joinedload(Floor.rooms).joinedload(Room.beds)
        ).all()
        return render_template('rooms.html', buildings=buildings)
    except Exception as e:
        print(f"Ошибка: {e}")
        return "Произошла ошибка, проверьте данные в базе.", 500


@bp.route('/get_employees')
def get_employees():
    employees = Employee.query.all()
    employee_list = [{'id': emp.id, 'name': emp.full_name} for emp in employees]
    return jsonify(employee_list)


@bp.route('/logout')
def logout():
    """
    Страница для выхода пользователя. После выхода - редирект на страницу входа.
    """
    logout_user()
    return redirect(url_for('auth.login'))


# Страница заселения
@bp.route('/check_in_ajax', methods=['POST'])
@login_required
def check_in_ajax():
    """
    AJAX-обработчик для заселения сотрудника в койку.
    После успешного заселения отправляет email-уведомление.
    """
    data = request.json

    try:
        employee_id = data.get('employee')
        bed_id = data.get('bed')
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')

        if not all([employee_id, bed_id, check_in_date, check_out_date]):
            return jsonify({'status': 'error', 'message': 'Некоторые данные отсутствуют.'}), 400

        bed = Bed.query.get(bed_id)
        employee = Employee.query.get(employee_id)

        if not bed:
            return jsonify({'status': 'error', 'message': f'Койка с ID {bed_id} не найдена.'}), 400
        if bed.is_occupied:
            return jsonify({'status': 'error', 'message': 'Койка уже занята.'}), 400
        if not employee:
            return jsonify({'status': 'error', 'message': f'Сотрудник с ID {employee_id} не найден.'}), 400

        from datetime import datetime
        try:
            bed.check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
            bed.check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')
        except ValueError as ve:
            return jsonify({'status': 'error', 'message': f'Ошибка в формате даты: {ve}'}), 400

        bed.is_occupied = True
        db.session.commit()

        # Отправка email
        subject = "Подтверждение заселения"
        message = f"""
        Уважаемый {employee.full_name},

        Вы успешно заселены в общежитие.

        Дата заселения: {check_in_date}
        Дата выселения: {check_out_date}
        Койка: {bed_id}

        Спасибо!
        """
        email_sent = send_email(subject, message)

        if email_sent:
            return jsonify({'status': 'success', 'message': 'Заселение успешно! Уведомление отправлено.'}), 200
        else:
            return jsonify({'status': 'success', 'message': 'Заселение успешно! Но уведомление не отправлено.'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Ошибка сервера: {e}")
        return jsonify({'status': 'error', 'message': 'Произошла внутренняя ошибка сервера.'}), 500


@bp.route('/add_building', methods=['GET', 'POST'])
@login_required  # Требуется авторизация
def add_building():
    """
    Страница для добавления нового здания, этажей, комнат и коек.
    """
    form = BuildingForm()

    if form.validate_on_submit():
        # Создаем новое здание
        building = Building(name=form.name.data)
        db.session.add(building)
        db.session.commit()  # Сохраняем здание, чтобы получить его id

        # Создание этажей для здания
        for i in range(form.num_floors.data):
            floor = Floor(number=i + 1, building_id=building.id)
            db.session.add(floor)
            db.session.commit()

            # Создание комнат для каждого этажа
            for j in range(form.num_rooms_per_floor.data):
                room = Room(number=f"Room {j + 1}", floor_id=floor.id)
                db.session.add(room)
                db.session.commit()

                # Создание койки для каждой комнаты
                for k in range(form.num_beds_per_room.data):
                    bed = Bed(is_occupied=False, room_id=room.id)
                    db.session.add(bed)

        db.session.commit()  # Завершаем транзакцию, добавляем все койки

        flash('Здание и помещения успешно добавлены!', 'success')
        return redirect(url_for('auth.index'))

    return render_template('add_building.html', form=form)


@bp.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    """
    Страница для добавления нового сотрудника. Проверяется уникальность табельного номера.
    """
    form = EmployeeForm()

    if form.validate_on_submit():
        # Проверка на уникальность табельного номера
        existing_employee = Employee.query.filter_by(badge_number=form.badge_number.data).first()
        if existing_employee:
            flash('Сотрудник с таким табельным номером уже существует!', 'danger')
            return redirect(url_for('auth.add_employee'))

        # Создание нового сотрудника
        employee = Employee(
            full_name=form.full_name.data,
            badge_number=form.badge_number.data,
            passport_series=form.passport_series.data,
            passport_number=form.passport_number.data,
            passport_issue_date=form.passport_issue_date.data,
            has_patent=form.has_patent.data
        )

        db.session.add(employee)
        db.session.commit()

        flash('Сотрудник успешно добавлен!', 'success')
        return redirect(url_for('auth.index'))

    return render_template('add_employee.html', form=form)


@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Страница для добавления нового пользователя. Пароль хешируется перед сохранением в базе данных.
    """
    form = UserForm()

    if form.validate_on_submit():
        # Хешируем пароль
        hashed_password = generate_password_hash(form.password.data)

        # Создание нового пользователя
        user = User(
            login=form.login.data,
            password_hash=hashed_password,
            role=form.role.data,
        )

        db.session.add(user)
        db.session.commit()

        flash('Учётная запись успешно создана!', 'success')
        return redirect(url_for('auth.index'))

    return render_template('add_user.html', form=form)
