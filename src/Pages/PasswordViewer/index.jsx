import React from 'react';
import { useParams, useLocation   } from 'react-router-dom';

// material-ui
import {
    Box,
    Button,
    Checkbox,
    Divider,
    FormControlLabel,
    FormHelperText,
    Grid,
    Link,
    IconButton,
    InputAdornment,
    InputLabel,
    OutlinedInput,
    Stack,
    Typography
} from '@mui/material';

// third party
import * as Yup from 'yup';
import { Formik } from 'formik';

 
import AnimateButton from '../../Components/animations/AnimatedButton';

// assets
import { Visibility, VisibilityOff } from '@mui/icons-material';

const PassViewer = ( ) => {
    const location = useLocation()
    const { state } = location
    const {linkHref} = state
    
    const {link, response} = linkHref

    const { password }  = response
    //const user_pass =  "b'WkdGRFpYSWo='"
    
    
    //const decodedValue = atob(user_pass.slice(2));

    //console.log(decodedValue)

    function fromBinary(encoded) {
        const binary = atob(encoded);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < bytes.length; i++) {
          bytes[i] = binary.charCodeAt(i);
        }
        return String.fromCharCode(...new Uint16Array(bytes.buffer));
      }
      
      // our previous Base64-encoded string
      let decoded = fromBinary(password) // "✓ à la mode"
      console.log(decoded)
      
    return (
        <Box sx={{ minHeight: '100vh' }}>
            <Grid
                container
                direction="column"
                justifyContent="space-around"
                sx={{
                    minHeight: '100vh'
                }}
            >
                <Grid container 
                    direction="row" 
                    justifyContent="space-around"
                >
                    <Grid container xs={8} lg={4} spacing={4} 
                            sx={{
                                boxShadow: 'rgba(0, 0, 0, 0.15) 0px 2px 8px'
                            }}
                        >
                        <Grid item xs={11} lg={11} >
                           Teste
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Box>
    );
};

export default PassViewer;
