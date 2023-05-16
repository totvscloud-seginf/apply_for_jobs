import * as C from "@chakra-ui/react";
import { Text } from '@chakra-ui/react';
import React from "react";

class Password extends React.Component {

  constructor(props){
      super(props);

      this.state = {
              id: 1,
              email: 'netto@netto.com', 
              password: '', 
              views: '', 
              time_views: '',
              url: '',
              expire: false,
              date_free: '',
              last_updated: '',
              use_characters: false,
              use_numbers: false,
              use_words: false,
              pass_size: false
      }
  } 
}

atualizaEmail = (e) => {
    this.setState(
      {
        nome: e.target.value,
      }
    )
}

const FormInsertEmail = () => {
  return (
    <C.VStack spacing={5}>
        <Text fontSize='xm'>Digite seu e-mail para iniciar o processo de criação de senha:</Text>
      <C.Input 
      type="email" 
      placeholder="Digite o E-mail" 
      borderColor="blue.700" 
      value={this.state.email} 
      onChange={this.atualizaEmail}
      />
    </C.VStack>
  );
};

export default FormInsertEmail;