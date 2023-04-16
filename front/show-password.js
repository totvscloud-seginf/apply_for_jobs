const urlParams = new URLSearchParams(window.location.search);
const uuid = urlParams.get('uuid');
const url = 'http://127.0.0.1:5000/';

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

    fetch(url + "password", options)
        .then((response) => {
            if (response.status === 200) {
                response.json().then((data) => {
                    document.getElementById("password").innerHTML = data.password;
                });
            } else {
                    alert("Senha indisponível");
            }
        })
        .catch((error) => {
            console.error(error);
        });
});
