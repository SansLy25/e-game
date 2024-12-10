document.addEventListener("DOMContentLoaded", () => {

    // Максимальное значение для input
    const MAX_VALUE = 30;

    // Найти все input[type="number"] с readonly
    const inputs = document.querySelectorAll('input[type="number"][readonly]');

    inputs.forEach(input => {
        // Найти родительский контейнер
        const container = input.closest('.bg-gray-50.dark\\:bg-gray-700.rounded-lg.p-4.space-y-4');

        if (container) {
            const svgContainer = container.querySelector('.flex-shrink-0');

            if (svgContainer) {
                // Функция для обновления SVG
                const updateSVG = () => {
                    const value = parseInt(input.value, 10);

                    svgContainer.innerHTML = value === 0
                        ? `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x w-5 h-5 text-red-500"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>`
                        : `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check w-5 h-5 text-green-500 dark:text-green-400"><path d="M20 6 9 17l-5-5"></path></svg>`;
                };

                // Инициализировать SVG
                updateSVG();

                // Слушать событие изменения input
                input.addEventListener('input', updateSVG);

                // Для программного изменения значения (например, кнопками)
                const observer = new MutationObserver(() => updateSVG());
                observer.observe(input, {attributes: true, attributeFilter: ['value']});
            }

            // Обработчики для кнопок инкремента и декремента
            const incrementButton = container.querySelector('button:nth-child(1)');
            const decrementButton = container.querySelector('button:nth-child(3)');

            if (incrementButton && decrementButton) {
                incrementButton.addEventListener("click", (e) => {
                    e.preventDefault();
                    let value = parseInt(input.value, 10);
                    if (!isNaN(value) && value < MAX_VALUE) {
                        input.value = value + 1;
                        input.dispatchEvent(new Event('input')); // Триггерим событие input
                    }
                });

                decrementButton.addEventListener("click", (e) => {
                    e.preventDefault();
                    let value = parseInt(input.value, 10);
                    if (!isNaN(value) && value > 0) {
                        input.value = value - 1;
                        input.dispatchEvent(new Event('input')); // Триггерим событие input
                    }
                });
            }
        } else {
            console.warn("Container not found for input", input);
        }
    });

    // Функция для обновления значений input
    const updateInputValues = (sectionId, value) => {
        const section = document.getElementById(sectionId);
        if (section) {
            const inputs = section.querySelectorAll('input[type="number"][readonly]');
            inputs.forEach(input => {
                input.value = value;
                input.dispatchEvent(new Event('input')); // Сигнализируем об изменении значения
            });
        }
    };

    // Обработчик для фиолетовой кнопки
    const purpleButton = document.querySelector('button.bg-purple-50');
    if (purpleButton) {
        purpleButton.addEventListener('click', () => {
            updateInputValues('short', 1); // Устанавливаем значение 1 в секции short
            updateInputValues('long', 1);  // Устанавливаем значение 1 в секции long
        });
    }


    const blueButton = document.querySelector('button.w-full.px-4.py-2.rounded-lg.bg-blue-50.dark\\:bg-blue-900\\/30.text-blue-600.dark\\:text-blue-400.hover\\:bg-blue-100.dark\\:hover\\:bg-blue-900\\/50.transition-colors.flex.items-center.gap-2');
    if (blueButton) {
        blueButton.addEventListener('click', () => {
            updateInputValues('short', 1); // Устанавливаем значение 1 в секции short
            updateInputValues('long', 0);  // Устанавливаем значение 0 в секции long
        });
    }

    // Обработчик для зеленой кнопки
    const greenButton = document.querySelector('button.bg-green-50');
    if (greenButton) {
        greenButton.addEventListener('click', () => {
            updateInputValues('short', 0); // Устанавливаем значение 0 в секции short
            updateInputValues('long', 1);  // Устанавливаем значение 1 в секции long
        });
    }

    // Обработчик для красной кнопки
    const redButton = document.querySelector('button.bg-red-50');
    if (redButton) {
        redButton.addEventListener('click', () => {
            updateInputValues('short', 0); // Устанавливаем значение 0 во всех секциях
            updateInputValues('long', 0);
        });
    }
    const slider = document.getElementById("time-slider");
    const timeValue = document.getElementById("time-value");

    slider.addEventListener("input", () => {
        timeValue.textContent = `${slider.value} мин`;
    });
});