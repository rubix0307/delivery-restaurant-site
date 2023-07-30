function togglePasswordVisibility() {
            const passwordInputs = document.querySelectorAll('.password');
            const eyeIcons = document.querySelectorAll('.eye');

            for (let i = 0; i < passwordInputs.length; i++) {
                const inputType = passwordInputs[i].type;
                const isPasswordVisible = inputType === 'text';

                if (isPasswordVisible) {
                    passwordInputs[i].type = 'password';
                    eyeIcons[i].textContent = '🙈';
                } else {
                    passwordInputs[i].type = 'text';
                    eyeIcons[i].textContent = '🐵';
                }
            }
        }