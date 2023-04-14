const code = Math.floor(Math.random() * 90000) + 10000;
const spancode = document.getElementById("code");
spancode.innerHTML = code;

const form = document.getElementById("myForm");
form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    formData.append("code", code);
    fetch("http://127.0.0.1:5000/generate_url", {
        method: "POST",
        body: formData,
    })
        .then((response) => response.text())
        .then((data) => {
            const link = "http://localhost:4566/static-bucket/show-password.html?uuid=" + data;
            document.getElementById("linkSpan").innerHTML = link;
            document.getElementById("link").href = link;
        });
});