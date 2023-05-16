import * as C from "@chakra-ui/react";
import { Checkbox, CheckboxGroup } from '@chakra-ui/react';
import { Text } from '@chakra-ui/react';
import {
    RangeSlider,
    RangeSliderTrack,
    RangeSliderFilledTrack,
    RangeSliderThumb,
  } from '@chakra-ui/react'

const FormComplexityPassword = () => {
  
  return (
    <C.VStack spacing={5}>

        <Text fontSize='xm'>Vou definir a complexidade da minha senha:</Text>
        
        <Checkbox colorScheme='green' defaultChecked>
            Quero caracteres
        </Checkbox>
        <Checkbox colorScheme='green' defaultChecked>
            Quero números
        </Checkbox>
        <Checkbox colorScheme='green' defaultChecked>
            Quero letras
        </Checkbox>
        <Text fontSize='sm'>Quero definir o tamanho da senha:</Text>
        <RangeSlider
                aria-label={['min', 'max']}
                onChangeEnd={(val) => console.log(val)}
                >
                <RangeSliderTrack>
                    <RangeSliderFilledTrack />
                </RangeSliderTrack>
                <RangeSliderThumb index={0} />
                <RangeSliderThumb index={1} />
        </RangeSlider>
        
    </C.VStack>
  );
};

export default FormComplexityPassword;