   ( exports.handler = async(event)  => {
    //Constantes para enviar o email
    //O certo seria nao ter colocado a senha em texto puro mas sim como variavel de ambiente, porem pela falta de tempo foi texto puro
    const nodemailer = require('nodemailer');
    const user = "totvsempresa123456"
    const pass = "74123felipe"


    //Declarando o MD5
    var md5 = require('md5');
    //Funcao para aguardar o evento
   async function wait(event){
       await event
   }
   wait(event);
   //Funcao principal
    async function senha (hours, viewrs, passwords, email){
        //Variaveis para funcionamento e conecxao do bd
        var md5 = require('md5');
        const Sequelize = require('sequelize');
        const sequelize = new Sequelize('senhas', "admin", "admin123456", {
            host : "agora-vai-pfvr.cmmqkp6raeke.us-east-1.rds.amazonaws.com",
            dialect : 'mysql'
        })
        //Conecxao com o BD
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
        //Criacao no BD dos dados passado pela variavel event
        const novaSenha = await Senhas.create({
            senha: passwords,
            views: viewrs,
            horas: hours,
            link: md5(passwords)
        })
        const teste = await sequelize.sync();
        return teste
        }
        const senhaCliente = Math.random().toString(36).substring(0, 15);
        //Chamo a funcao senha caso o evento venha diferente de undefined
        if ( JSON.stringify(event) !== undefined){
            await wait(senha(JSON.stringify(event.horas),JSON.stringify(event.views),senhaCliente));
        console.log(JSON.stringify(event.views));
        console.log(JSON.stringify(event.horas));
        let transporter = nodemailer.createTransport({
            host:"smtp.gmail.com",
            port: 587,
            auth:{user,pass}
        });
        //Funcao para enviar o email
       await transporter.sendMail({
            from:user,
            to: JSON.stringify(event.email),
            subject: "Chave de acesso ",
            text:"Ola, sua chave de acesso para sua senha : "+md5(senhaCliente),
        });
        }
        const response = {
            statusCode: 200,
            body: JSON.stringify(md5(senhaCliente)),
        };
        return response;
    
})();
