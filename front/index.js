const gateway_url = "http://127.0.0.1:5000/";
const s3_url = "http://localhost:4566/static-bucket/";

const code = Math.floor(Math.random() * 90000) + 10000;
const spancode = document.getElementById("code");
spancode.innerHTML = code;

const passwordOptions = document.querySelector('#passwordOptions');
const passwordInput = document.querySelector('#password');

passwordOptions.addEventListener('change', () => {
    if (passwordOptions.value === 'custom') {
        passwordInput.removeAttribute('disabled');
    } else {
        passwordInput.value = ''
        passwordInput.setAttribute('disabled', '');
    }
});

const form = document.getElementById("myForm");
form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    formData.append("code", code);
    fetch(gateway_url + "generate_url", {
        method: "POST",
        body: formData,
    }).then((response) => {
        if (response.status === 200) {
            response.json().then((data) => {
                const link = s3_url + "show-password.html?uuid=" + data.password_id;
                document.getElementById("linkSpan").innerHTML = link;
                document.getElementById("link").href = link;
            });
            response.json().then((data) => {
                document.getElementById("error").innerHTML = data.message;
            });
        } else {
            alert("Erro inesperado, verifique se o formulário esta correto.");
        }
    });
});
