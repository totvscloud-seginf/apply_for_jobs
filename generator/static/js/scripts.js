// Definicao das variaveis a serem utilizadas
let passwordDisplay = document.querySelector('#password-display'),
    passwordUpdateButton = document.querySelector('#passowrd-update-button'),
    passwordHiddenInput = document.querySelector('#id_value'),
    stringSizeRange = document.querySelector('#string-size-range'),
    stringSizeDisplay = document.querySelector('#string-size-display');

function generatePasswordValue(passwordSize) {
    /*
    Faz a requisicao para a API gerar uma nova string de senha segura, insere a senha no campo do tipo hidden que guarda
    o valor do password a ser registrado no banco de dados.
    :param passwordSize: Recebe um integer com o tamanho da string segura a ser gerada.
    */
    const url = `/api/passwords/value/size=${passwordSize}/`

    fetch(url)
        .then(response => response.json())
        .then(password => {
            passwordDisplay.innerHTML = password.value;
            passwordHiddenInput.value = password.value;
        });
}

function copyLinkToClipboard(id) {
    /*
    Copia a URL de visualização para a area de transferencia.
    */
    let hostname = window.location.host,
        url = `${hostname}/passwords/${id}/`;

    navigator.clipboard.writeText(url);
}

// Como o mesmo arquivo js eh reaproveitado em varios templates, verifica se os ojetos html existem antes de criar o Event Listener.
if (stringSizeDisplay && stringSizeRange) {
    // Faz a requisicao para a API gerar uma senha randomica com o comprimento padrao de 8 caracteres.
    generatePasswordValue(8);
    // Assegura que os inputs range e number tenham o mesmo valor para determinar o comprimento da senha randomica a ser gerada.
    stringSizeDisplay.value = stringSizeRange.value;

    // Event Listener do botão que faz a requisição pra API gerar uma nova senha randomica com os parametros personalizados.
    passwordUpdateButton.addEventListener('click', () => {
        generatePasswordValue(stringSizeRange.value);
    });

    // Event Listener do input do tipo range que sincroniza tambem o input do tipo number do tamanho da senha e faz a requisicao para a API.
    stringSizeRange.addEventListener('input', () => {
        stringSizeDisplay.value = stringSizeRange.value;
        generatePasswordValue(stringSizeRange.value);
    });

    // Event Listener do input do tipo number que sincroniza tambem o input do tipo range do tamanho da senha e faz a requisicao para a API.
    stringSizeDisplay.addEventListener('focusout', () => {
        stringSizeRange.value = stringSizeDisplay.value;
        generatePasswordValue(stringSizeDisplay.value);
    });
}

