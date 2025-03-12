document.addEventListener('DOMContentLoaded', () => {
    // Находим все здания
    const buildings = document.querySelectorAll('.accordion-item');

    buildings.forEach((building) => {
        const buttons = building.querySelectorAll('.bridge__floors-buttons button');
        const floors = building.querySelectorAll('.bridge__floor-wrapper');

        // Изначально показываем первый этаж для каждого здания
        if (floors.length > 0) {
            floors[0].classList.add('active');
        }

        // Назначаем обработчик на каждую кнопку этажей внутри конкретного здания
        buttons.forEach((button, index) => {
            button.addEventListener('click', () => {
                // Убираем класс active у всех этажей данного здания
                floors.forEach(floor => floor.classList.remove('active'));
                // Добавляем класс active только для выбранного этажа
                floors[index].classList.add('active');
            });
        });
    });
});
