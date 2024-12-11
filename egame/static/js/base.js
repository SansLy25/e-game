document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('button').forEach(button => {
        const originalOnClick = button.onclick;
        button.onclick = function (event) {
            if (!originalOnClick) return;

            event.preventDefault();

            let url = null;
            if (originalOnClick.toString().includes('window.location')) {
                url = originalOnClick.toString().match(/['"]([^'"]*)['"]/)[1];
            }

            if (url) {
                if (event.ctrlKey) {
                    window.open(url, '_blank');
                } else {
                    window.location.href = url;
                }
            } else {
                originalOnClick.call(this, event);
            }
        };
    });

    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function (event) {
            const url = this.href;
            if (url) {
                event.preventDefault();
                if (event.ctrlKey) {
                    window.open(url, '_blank');
                } else {
                    window.location.href = url;
                }
            }
        });
    });
});



window.addEventListener('beforeunload', function () {
    localStorage.setItem('lastScrollY', window.scrollY);
});

document.addEventListener('DOMContentLoaded', function () {
    const lastScrollY = localStorage.getItem('lastScrollY');
    if (lastScrollY) {
        window.scrollBy({
            top: lastScrollY,
            behavior: 'instant'
        });
        localStorage.removeItem('lastScrollY');
    }
});



function changeColorTheme(baseColor, baseBgSubtle) {
    document.documentElement.style.setProperty('--base-color', baseColor);
    document.documentElement.style.setProperty('--base-color-subtle', baseBgSubtle);

    localStorage.setItem('baseColor', baseColor);
    localStorage.setItem('baseBgSubtle', baseBgSubtle);
}

function removeColorTheme() {
    localStorage.removeItem('baseColor');
    localStorage.removeItem('baseBgSubtle');
}

function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}