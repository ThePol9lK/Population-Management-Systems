// Получаем все элементы с классом .pillow
const pillows = document.querySelectorAll('.pillow');

// Добавляем обработчик клика на каждый элемент .pillow
pillows.forEach(pillow => {
    pillow.addEventListener('click', function() {
        this.classList.toggle('active'); // При клике добавляется или убирается класс active
    });
});
