let senhaElemento = document.querySelector("div.gerador-senha p")
const botaoGerarSenha = document.querySelector("div.gerador-senha button") 
const botaoValidade  = document.querySelector("div.validade button")

const caracteres = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","w","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","X","W","Y","0","1","2","3","4","5","6","7","8","9","@","#","$"]
//const botaourl = document.querySelector("div.url button")

let senha = ""


//criando uma function gerars senha

const gerarSenha = ()=>{
    
  for(let i = 1; i <= 12; i++){
    //Dicionario de todos os caracteres
    senha += caracteres[Math.floor(Math.random() * caracteres.length)]
    if(senha < 12){gerarSenha}
    
  }

  senhaElemento.textContent = senha

  senha = ""

}


botaoGerarSenha.onclick = ()=>{
  gerarSenha()

}
botaoValidade.onclick = ()=>{
  window.location = "urlsenha.html"

}


senhaElemento.onclick = ()=>{
  navigator.clipboard.writeText(senhaElemento.textContent)

  senhaElemento.classList.add("copiada")
}  

/*cont urlsenha = ()=>{
  
  window.location = "urlsenha.html"
  senhaElemento.textContent = senha

}
*/

