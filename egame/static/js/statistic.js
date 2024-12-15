document.addEventListener('DOMContentLoaded', async () => {
    // Получаем slug экзамена из URL
    const examSlug = window.location.pathname.split('/')[1];

    // URL для API
    const apiUrl = `/api/statistic/get_exam_statistic/${examSlug}`;

    try {
        // Запрос к API
        const response = await fetch(apiUrl);
        const data = await response.json();

        // 1. Средний балл
        const averageScore = data.average_score;
        document.getElementById('average_score_parameter').textContent = `${averageScore}%`;

        const scoreDifference = ((averageScore - data.all_users_average_score) / data.all_users_average_score * 100).toFixed(0);
        const scoreMessage = scoreDifference >= 0
            ? `На ${scoreDifference}% выше среднего`
            : `На ${Math.abs(scoreDifference)}% ниже среднего`;
        document.getElementById('score_message').textContent = scoreMessage;

        document.getElementById('score_bar').style.width = `${averageScore}%`;

        // 2. Среднее время подготовки
        const averageDuration = data.average_duration;
        const maxDuration = data.max_duration;
        const allUsersAverageDuration = data.all_users_average_duration;

        const hours = Math.floor(averageDuration / 3600);
        const minutes = Math.floor((averageDuration % 3600) / 60);
        const formattedDuration = hours > 0 ? `${hours}ч ${minutes}м` : `${minutes}м`;
        document.getElementById('average_duration_parameter').textContent = formattedDuration;

        const durationDifference = ((averageDuration - allUsersAverageDuration) / allUsersAverageDuration * 100).toFixed(0);
        const durationMessage = durationDifference >= 0
            ? `На ${durationDifference}% выше среднего`
            : `На ${Math.abs(durationDifference)}% ниже среднего`;
        document.getElementById('duration_message').textContent = durationMessage;

        const durationProgress = (averageDuration / maxDuration * 100).toFixed(2);
        document.getElementById('duration_bar').style.width = `${durationProgress}%`;

        // 3. Среднее количество заданий
        const averageVariantSize = data.average_variant_size;
        const maxVariantSize = data.max_variant_size;
        const variantCount = data.variant_count;

        document.getElementById('variant_parameter').textContent = `${averageVariantSize}з`;
        document.getElementById('variant_message').textContent = `Всего вариантов решено: ${variantCount}`;

        const variantProgress = (averageVariantSize / maxVariantSize * 100).toFixed(2);
        document.getElementById('variant_bar').style.width = `${variantProgress}%`;

        // Преобразуем данные для графиков
        const maxPoints = 50; // Максимальное количество точек на графике
        const scoreDynamic = data.score_dynamic.slice(-maxPoints).map(item => ({
            date: item.date,
            value: item.score
        }));

        const durationDynamic = data.duration_dynamic.slice(-maxPoints).map(item => ({
            date: item.date,
            value: item.duration / 60 // Переводим секунды в минуты
        }));

        // Данные для первого графика (scoreChart)
        const scoreData = {
            labels: scoreDynamic.map(item => item.date), // Даты
            datasets: [{
                label: 'Результат',
                data: scoreDynamic.map(item => item.value), // Значения
                backgroundColor: 'rgba(59, 130, 246, 0.2)', // Градиент для заливки
                borderColor: 'rgba(59, 130, 246, 1)', // Цвет линии
                borderWidth: 2,
                fill: true, // Заливка под линией
                tension: 0.4, // Сглаживание линии
            }]
        };

        // Данные для второго графика (durationChart)
        const durationData = {
            labels: durationDynamic.map(item => item.date), // Даты
            datasets: [{
                label: 'Время (минуты)',
                data: durationDynamic.map(item => item.value), // Значения
                backgroundColor: 'rgba(236, 72, 153, 0.2)', // Градиент для заливки (розовый)
                borderColor: 'rgba(236, 72, 153, 1)', // Цвет линии (розовый)
                borderWidth: 2,
                fill: true, // Заливка под линией
                tension: 0.4, // Сглаживание линии
            }]
        };

        // Настройки графика (общие для обоих графиков)
        const chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Решения',
                        color: '#9da5bc',
                    },
                    grid: {
                        color: 'rgba(107, 114, 128, 0.2)', // Цвет сетки X
                    },
                    ticks: {
                        color: '#9da5bc', // Цвет текста оси X
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Результат',
                        color: '#9da5bc',
                    },
                    grid: {
                        color: 'rgba(107, 114, 128, 0.2)', // Цвет сетки Y
                    },
                    ticks: {
                        color: '#9da5bc', // Цвет текста оси Y
                    }
                }
            },
            plugins: {
                tooltip: {
                    enabled: true, // Включение подсказок
                    callbacks: {
                        title: (context) => `Дата: ${context[0].label}`, // Заголовок подсказки
                        label: (context) => `Результат: ${context.raw}` // Текст подсказки для первого графика
                    }
                },
                legend: {
                    display: false, // Скрытие легенды
                }
            }
        };

        // Создание первого графика (scoreChart)
        const ctxScore = document.getElementById('scoreChart');
        if (ctxScore) {
            new Chart(ctxScore, {
                type: 'line', // Тип графика: линия
                data: scoreData,
                options: chartOptions
            });
        } else {
            console.error('Элемент с id="scoreChart" не найден!');
        }

        // Создание второго графика (durationChart)
        const ctxDuration = document.getElementById('durationChart');
        if (ctxDuration) {
            new Chart(ctxDuration, {
                type: 'line', // Тип графика: линия
                data: durationData,
                options: {
                    ...chartOptions,
                    scales: {
                        ...chartOptions.scales,
                        y: {
                            title: {
                                display: true,
                                text: 'Время (минуты)',
                                color: '#9da5bc',
                            },
                            grid: {
                                color: 'rgba(107, 114, 128, 0.2)', // Цвет сетки Y
                            },
                            ticks: {
                                color: '#9da5bc', // Цвет текста оси Y
                            }
                        }
                    },
                    plugins: {
                        ...chartOptions.plugins,
                        tooltip: {
                            ...chartOptions.plugins.tooltip,
                            callbacks: {
                                ...chartOptions.plugins.tooltip.callbacks,
                                label: (context) => `Время: ${context.raw}м` // Текст подсказки для второго графика
                            }
                        }
                    }
                }
            });
        } else {
            console.error('Элемент с id="durationChart" не найден!');
        }

        // Отображение рейтинга
        const friendsRating = data.friends_average_scores;
        const sortedFriends = Object.entries(friendsRating)
            .sort((a, b) => b[1] - a[1]) // Сортировка по убыванию баллов
            .slice(0, 5); // Берем топ-5

        // Расстановка имен и баллов по местам
        for (let rank = 1; rank <= 5; rank++) {
            const nameId = `name${rank}`;
            const scoreId = `score${rank}`;

            const nameElement = document.getElementById(nameId);
            const scoreElement = document.getElementById(scoreId);

            if (nameElement && scoreElement) {
                if (sortedFriends[rank - 1]) {
                    const [name, score] = sortedFriends[rank - 1];
                    nameElement.textContent = name;
                    scoreElement.textContent = score;
                } else {
                    // Если места не хватает, заполняем "Отсутствует" и "0"
                    nameElement.textContent = 'Отсутствует';
                    scoreElement.textContent = '0';
                }
            }
        }
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
    }
    document.getElementById('score_circle').style.display = `none`;
    document.getElementById('duration_circle').style.display = `none`;
});