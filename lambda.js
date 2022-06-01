const AWS = require("aws-sdk");

const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
  let body;
  let statusCode = 200;
  const headers = {
      'Access-Control-Allow-Origin':'*',
      'Access-Control-Allow-Methods':'POST, PUT, DELETE, GET, OPTIONS',
      'Access-Control-Request-Method':'*',
      'Access-Control-Allow-Headers':'Origin, X-Requested-With, Content-Type, Accept, Authorization'
  };

  try {
    switch (event.routeKey) {
      case "GET /items/{id}":
        let result = await dynamo
          .get({
            TableName: "passwords",
            Key: {
              id: event.pathParameters.id
            }
          })
          .promise();
        let access = JSON.stringify(result.Item.click);
        let flag = JSON.stringify(result.Item.flag);
        var count = parseInt(flag)+1;
        if(flag>=access){
          body = "Sua senha expirou.";
          await dynamo
            .delete({
              TableName: "passwords",
              Key: {
                id: event.pathParameters.id
              }
            })
            .promise();
        }else{
           body = `Sua senha é:    ${JSON.stringify(result.Item.pass).replaceAll('"',"")} `;
           let click =  JSON.stringify(result.Item.click).replaceAll('"',"");
           await dynamo
            .put({
              TableName: "passwords",
              Item: {
                id: JSON.stringify(result.Item.id).replaceAll('"',""),
                pass: JSON.stringify(result.Item.pass).replaceAll('"',""),
                click: parseInt(click),
                flag: count
              }
            })
            .promise();
           
        }
        break;
      case "PUT /items":
        let requestJSON = JSON.parse(event.body);
        await dynamo
          .put({
            TableName: "passwords",
            Item: {
              id: requestJSON.id,
              pass: requestJSON.pass,
              click: requestJSON.click,
              flag: requestJSON.flag
            }
          })
          .promise();
        body = "https://dn30s93wrk.execute-api.us-east-1.amazonaws.com/items/"+requestJSON.id;;
        break;
      default:
        throw new Error(`Unsupported route: "${event.routeKey}"`);
    }
  } catch (err) {
    statusCode = 400;
    body = err.message;
  } finally {
    body = JSON.stringify(body);
  }

  return {
    statusCode,
    body,
    headers
  };
};
