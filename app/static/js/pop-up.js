// Функция для открытия модального окна
function openCheckInModal(bedId, roomNumber, floorNumber, buildingName) {
    // Заполняем данные в модальное окно
    document.getElementById('bed').value = `Койка ${bedId}`;

    // Получаем список сотрудников через AJAX
    fetch('/get_employees')
        .then(response => response.json())
        .then(data => {
            const employeeSelect = document.getElementById('employee');
            employeeSelect.innerHTML = '';  // Очищаем список перед заполнением
            data.forEach(employee => {
                const option = document.createElement('option');
                option.value = employee.id;
                option.text = employee.name;
                employeeSelect.appendChild(option);
            });
        });

    // Инициализация модального окна
    const modal = new bootstrap.Modal(document.getElementById('checkInModal'));
    modal.show();
}
