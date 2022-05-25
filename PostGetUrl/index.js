   ( exports.handler = async(event)  => {
  
    const nodemailer = require('nodemailer');
    async function wait(event){
       await event
       return event
    }
    wait(event);
    async function senha (linkUrl){
        //Formatando o link
        const link = linkUrl.replace('"','');
        const linkFinal = link.replace('"','')
        //Const nescessarias para conectar no banco de dados
        const Sequelize = require('sequelize');
        const sequelize = new Sequelize('senhas', "admin", "admin123456", {
            host : "agora-vai-pfvr.cmmqkp6raeke.us-east-1.rds.amazonaws.com",
            dialect : 'mysql'
        })
        //Conceccao com o BD
        const Senhas = await sequelize.define('password',{
            id:{
                type: Sequelize.INTEGER,
                autoIncrement: true,
                allowNull: false,
                primaryKey: true
            },
            senha:{
                type: Sequelize.STRING,
                allowNull: false,
            },
            views:{
                type: Sequelize.STRING,
                allowNull: false,
            },
            horas:{
                type: Sequelize.STRING,
                allowNull: false,
            },
            link:{
                type: Sequelize.STRING,
                allowNull: false,
            },
        })
        //Funcao para transforma meses em seu respectivo numero
        function mesParaNumero (mesString){
            switch (mesString){
                case "January":
                     mes = 01
                     break;
                case "February":
                    mes = 02
                    break;
                case "March":
                    mes = 03
                    break;
                case "April":
                    mes = 04
                    break;
                case "May":
                    mes = 05
                    break;
                case "June":
                    mes = 06
                    break;
                case "July":
                    mes = 07
                    break;
                case "August":
                    mes = 08
                    break;
                case "September":
                    mes = 09
                    break;
                case "October":
                    mes = 10
                    break;
                case "November":
                    mes = 11
                    break;
                case "December":
                    mes = 12
                    break;
            }
            return mes
        }
        //Constantes e formatacoes para comparar as horas
        let mes = 0
        const horasAtual = new Date();
        const horaAtualAux = horasAtual.toString().split(' ');
        const diaAtual = horaAtualAux[2];
        const horasAtualFinal = horaAtualAux[4];
        const mesAtual = mesParaNumero(horaAtualAux[1]);
        const where =await Senhas.findAll({where: {link:linkFinal}});
        let bd = where[0];
        let id = bd.dataValues.id;
        let views = bd.dataValues.views;
        let viewsFormatado =views.replace('"','')
        let viewsFormatadoFinal= viewsFormatado.replace('"','')
        let horas = bd.dataValues.horas;
        let criado = bd.dataValues.createdAt;
        senha = bd.dataValues.senha;
        const criadoEm = criado.toString().split(' ');
        const mesCriacao = mesParaNumero(criado[1]);
        const diaCriacao = criadoEm[2];
        const horasCriacao = criadoEm[4];
        const horaFormatada = horasCriacao.split(':');
        const horaFormatadaAdd = horas.replace('"','');
        const horaFormatadaAddFinal = horaFormatadaAdd.replace('"','');
        let diffDia = diaCriacao;
        let diffMes = mesCriacao;
        let diffHoras = parseInt(horaFormatada[0]) + parseInt(horaFormatadaAddFinal);
        let horasAtualFinalFormatado = horasAtualFinal.split(':') 
        //Comparacoes para verificar se o tempo ja esgotou
        while (diffHoras > 24){
            if (diffHoras > 24){
                diffHoras = diffHoras - 24;
                diffDia = parseInt(diffDia) + 1
            }
            if (diaCriacao >30){
                diffDia = 0
                diffMes = parseInt(diffMes) +1
            }
        }
        if (diffMes > mesAtual){
            return "Numero de horas batido"
        }
        if (parseInt(diaAtual) > diffDia){
            return "Numero de horas batido"
        }
        if (parseInt(diaAtual) == diffDia){
            if (parseInt(horasAtualFinalFormatado[0] > diffHoras)){
                return "Numero de horas batido"
            }
        }
        //Verifica se os views ja foram batidos
        if( viewsFormatadoFinal == 0){
            return "Numero de views batido"
            
        }
        else{
            Senhas.update(
                {views : viewsFormatadoFinal-1},
                { where: { id: id } }
            )
        }
        const teste = await sequelize.sync();
        return senha
    }
    //Chama a funcao senha se o evento nao ven undefined
        if ( JSON.stringify(event) !== undefined){
        var final = await wait(senha(JSON.stringify(event.url)));
        }
        const response = {
            statusCode: 200,
            body: final,
        };
        return response;
})();
