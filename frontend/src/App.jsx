import { useState } from "react";
import FormInsertEmail from "./components/FormInsertEmail";
import FormComplexityPassword from "./components/FormComplexityPassword";
import FormChooseTypePassword from "./components/FormChooseTypePassword";
import * as C from "@chakra-ui/react";
import Step from "./components/Step";
import FormInsertMyPassword from "./components/FormInsertMyPassword";
import { Text } from '@chakra-ui/react';
import FormInsertTime from "./components/FormInsertTime";
import { BrowserRouter, Routes, Link, Route } from 'react-router-dom';

function App() {
  const [step, setStep] = useState(1);

  const getCompStep = () => {
    switch (step) {
      case 1:
        return <FormInsertEmail />;
      case 2:
        return <FormChooseTypePassword />;
      case 3:
        return <FormComplexityPassword />;
      case 4:
        return <FormInsertMyPassword />;
      case 5:
        return <FormInsertTime />;
      default:
        return <FormInsertEmail />;
    }

    <BrowserRouter>
    <Link to="/"></Link>

    <Routes>
      <Route path="/" index component={<FormInsertEmail />}></Route>
      <Route path="/typepassword" element={<FormChooseTypePassword />}></Route>
      <Route path="/" element={<FormComplexityPassword />}></Route>
    </Routes>
    </BrowserRouter>
  };

  const Steps = [1, 2, 3, 4, 5, 6];

  return (
      <C.Flex h="100vh" align="center" justify="center">
        <C.Center maxW={600} w="100%" py={10} px={2} flexDir="column">
        
          <Text fontFamily="arial" lineHeight="150px" fontSize='40px' as="b" color='gray'>TOTVS Password Generator</Text>
        
          <C.HStack spacing={5}>
            {Steps.map((item) => (
              <Step key={item} index={item} active={step === item} />
            ))}
          </C.HStack>

          <C.Divider my={5} borderColor="blackAlpha.700" />

          <C.Box w="80%">{getCompStep()}</C.Box>

          <C.HStack spacing={10} mt={4}>
            <C.Button onClick={() => setStep(step - 1)} disabled={step === 1}>
              Voltar
            </C.Button>
            <C.Button
              colorScheme="blue"
              onClick={() => step !== 10 && setStep(step + 1)}
            >
              {step === 8 ? "Enviar" : "Próximo"}
            </C.Button>
          </C.HStack>
        </C.Center>
      </C.Flex>
  );
}

export default App;