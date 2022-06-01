import React, {useState, useEffect}from 'react';
import { StyleSheet, Text, View, TouchableOpacity, TextInput, FlatList} from 'react-native';

export default function App() {

  const [access, setAccess] = useState('');
  const [resp, setResp] = useState('');
  const [identity, setIdentity] = useState('');
  //const [data, setData] = useState({});
 
  var chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ!@#$%^&*()+?><:{}[]";
  var passwordLength = 16;
  var password = "";
  for (var i = 0; i < passwordLength; i++) 
  {
    var randomNumber = Math.floor(Math.random() * chars.length);
    password += chars.substring(randomNumber, randomNumber + 1);
  }
  const data = {
      id:identity,
      pass: password,
      click:parseInt(access),
      flag: 0
    };

  let putPassword = async () => {

   await fetch('https://dn30s93wrk.execute-api.us-east-1.amazonaws.com/items', {
        method: "PUT",
        headers: {'Content-Type':'application/json'},
        mode: 'cors',
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        setResp(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  }


  return (
    <View style={styles.container}>
      <View style={styles.box}>

      <Text style={styles.text}>Gerador de Senha Serverless</Text>

      <TextInput style={styles.textInput} 
                 placeholder='Identificação do cliente' 
                 placeholderTextColor='black' 
                 onChangeText={setIdentity}/>
      <TextInput style={styles.textInput} 
                 placeholder='Quantidade de visualização' 
                 placeholderTextColor='black'
                 onChangeText={setAccess}/>
      <TextInput style={styles.urlReceive}
                 defaultValue={resp}/>

      <TouchableOpacity style={styles.button} onPress={putPassword}>
        <Text style={styles.textButton} >Gerar Senha</Text>
      </TouchableOpacity>

      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#4682B4',
    alignItems: 'center',
    justifyContent: 'center',
    borderColor: 'black',
    
  },
  box: {
    width: '700px',
    height: '300px',
    backgroundColor:'#E0FFFF',
    alignItems: 'center',
    justifyContent: 'center',
    display: 'flex',
    borderRadius: '10px'
  },
  button: {
    backgroundColor: '#add8e6',
    borderRadius: '8px',
    padding: '10px 15px',
    marginTop: 20
  },
  text: {
    fontSize: 20,
    color: 'black',
    marginBottom: 50,
  },
  textButton: {
    fontSize: 15,
    color: 'black',
    padding:'10px'
  },
  textInput: {
    position: 'relative',
    height: '40px',
    width: '35%',
    borderRadius: '8px',
    margin: '15px 0 20px',
    padding: '0 20px',
    letterSpacing: '2px',
    marginBottom: 10,
    textAlign: 'center'
  },
  urlReceive: {
    position: 'relative',
    height: '40px',
    width: '80%',
    borderRadius: '8px',
    margin: '15px 0 20px',
    padding: '0 20px',
    letterSpacing: '2px',
    marginBottom: 10
  },
});
