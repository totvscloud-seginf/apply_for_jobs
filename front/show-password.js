const urlParams = new URLSearchParams(window.location.search);
        const uuid = urlParams.get('uuid');

        const url = 'http://127.0.0.1:5000/password';

        const data = {
            password_uuid: uuid,
            code: Number(document.getElementById('code').value)
        };

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        const form = document.getElementById("myForm");
        form.addEventListener("submit", (event) => {
            
            event.preventDefault();

            fetch(url, options)
                .then((response) => response.text())
                .then((data) => {
                    document.getElementById("password").innerHTML = data;
                });
        });