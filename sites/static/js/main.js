$(document).ready(function() {
    let qt_char = $(".qt_char")
    let tamanho = qt_char.val()

    if (tamanho >= 8){
        geraSenha(tamanho)
    }
    
    //request para gerar uma password nova
    $(".qt_char").on("change", function(){
        let qt_char = $(".qt_char").val()
        geraSenha(qt_char)
    });
    
    function geraSenha(tamanho){
        $.ajax({
            type: 'GET',
            url: '/api/password/size/'+tamanho,
            success: function(res) {
                // joga retorno no campo hidden para o post
                $(".password").val(res.password)
            }
        });
    }
}); 