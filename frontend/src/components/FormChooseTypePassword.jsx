import * as C from "@chakra-ui/react";
import { Button, ButtonGroup } from '@chakra-ui/react'

const FormChooseTypePassword = () => {
  return (
    <C.VStack spacing={5}>
        <Button
        size='md'
        height='48px'
        width='300px'
        border='2px'
        borderColor='green.500'
        >
        Quero senha automática
        </Button>

        <Button
        size='md'
        height='48px'
        width='300px'
        border='2px'
        borderColor='green.500'
        >
        Quero escrever minha senha
        </Button>

        

    </C.VStack>
  );
};

export default FormChooseTypePassword;