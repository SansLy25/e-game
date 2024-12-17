document.addEventListener('DOMContentLoaded', () => {
  const inputGroups = document.querySelectorAll('.input-group');

  inputGroups.forEach(group => {
    const formControl = group.querySelector('.form-control');

    if (formControl) {
      const checkInput = () => {
        if (formControl.value !== '') {
          group.classList.add('has-value');
        } else {
          group.classList.remove('has-value');
        }
      };

      checkInput();

      formControl.addEventListener('input', checkInput);
    }
  });
}); 