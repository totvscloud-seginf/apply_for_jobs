import * as C from "@chakra-ui/react";
import { Text } from '@chakra-ui/react';

const FormInsertMyPassword = () => {
  return (
    <C.VStack spacing={5}>
        <Text fontSize='xm'>Vou definir minha senha:</Text>
      <C.Input type="password" placeholder="Digite sua senha" borderColor="blue.700" />
      {/* <C.Input
        type="email"
        placeholder="Confirme seu E-mail"
        borderColor="blue.700"
      />
      <C.Input type="password" placeholder="Senha" borderColor="blue.700" /> */}
    </C.VStack>
  );
};

export default FormInsertMyPassword;