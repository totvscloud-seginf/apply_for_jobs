import * as C from "@chakra-ui/react";
import { Text } from '@chakra-ui/react';

const FormInsertTime = () => {
  return (
    <C.VStack spacing={5}>
        <Text fontSize='xm'>Quantas vezes a senha gerada poderá ser vista:</Text>
      <C.Input type="text" placeholder="Número de vezes" borderColor="blue.700" />

      <Text fontSize='xm'>Quanto tempo a senha ficará válida:</Text>
      <C.Input type="text" placeholder="Número de dias" borderColor="blue.700" />
      
      
      {/* <C.Input
        type="email"
        placeholder="Confirme seu E-mail"
        borderColor="blue.700"
      />
      <C.Input type="password" placeholder="Senha" borderColor="blue.700" /> */}
    </C.VStack>
  );
};

export default FormInsertTime;