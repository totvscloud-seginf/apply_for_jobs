import React from 'react';
import { useParams, Link as RouterLink  } from 'react-router-dom';
import { useState } from 'react';
import useRequest from '../../hooks/request';
// material-ui
import {
    Box,
    Modal,
    Grid,
    Button,
    Link,
    IconButton,
    CircularProgress,
    Backdrop,
    InputAdornment,
    Divider,
    
    OutlinedInput,
    Stack,
    Typography
} from '@mui/material';


// assets
import { Visibility, VisibilityOff } from '@mui/icons-material';


const PassViewerLink = ( ) => {
    const teste = useParams()
    
    const [showPassword, setShowPassword] = useState(false);

    
    const { makeRequest } = useRequest();
    
    const link_params = new URLSearchParams(teste.currlink)
    
    const linkHref = {}
    for (const [key, value] of link_params){
        if (key === 'link'){
            linkHref[key] = decodeURIComponent(escape(window.atob(value)));
        }
        else{
            linkHref[key] = value
        }
        
    }
    
    
    const {link, login} = linkHref
    

    const [open, setOpen] = useState(false);
    const [mensagem, setMensagem ] = useState('')
    const [passValue, setpassValue] = useState('')
    const [bkopen, setBkOpen] = useState(false);
 
    const values = {login: login,
        password: {
            password: '',
            auto: '',
            passlimitview: '',
            passlifetime: '',
            currentlink: '',
            params: {
                passlen: '',
                numbers: '',
                letter: '',
                espChar: ''
            }
        }
    }

    let req_param = {         
        url: link,        
        data : values
    };

    

    const handleClose = () => {
        setOpen(false);
    };

    const handleCloseBk = () => {
        setBkOpen(false);
      };
    const handleOpenBk = () => {
        setBkOpen(true);
      };

    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };


    const handleClickShowPassword = () => {        
        setShowPassword(!showPassword);        
    };

    const handleGetPassWord = async () => {
        handleOpenBk()
        const response = await makeRequest(req_param)
        
        if ('resp' in response) {
            const resp = response['resp'];
    
            if ('result' in resp) {
              const result = resp['result'];
    
              if (result !== 'OK') {
                setMensagem(resp.data);
                setOpen(true);
                return;
              }
            }
    
            setpassValue(response.resp.password);
            handleCloseBk()
          }   
          
    }  

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
                    spacing={4} 
                >
                    <Grid item xs={8} lg={8} 
                            sx={{
                                boxShadow: 'rgba(0, 0, 0, 0.15) 0px 2px 8px'
                            }}
                        >
                        <Grid item xs={11} lg={11} >
                            <Modal  open={open}
                                    onClose={handleClose}
                                    aria-labelledby="child-modal-title"
                                    aria-describedby="child-modal-description"
                            >
                                <Box sx={{position: 'absolute',
                                            top: '50%',
                                            left: '50%',
                                            transform: 'translate(-50%, -50%)',
                                            width: 400,
                                            bgcolor: 'background.paper',
                                            border: 'none',
                                            borderRadius: '25px',
                                            boxShadow: 24,
                                            p: 4}}>
                                    <Typography id="modal-modal-title" variant="h6" component="h2">
                                        Erro!
                                    </Typography>
                                    <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                                        {mensagem}
                                    </Typography>
                                </Box>
                            </Modal>
                            <Grid container spacing={0} sx={{paddingBottom: '20px'}} >
                                <Grid item lg={12} sm={12} display={'flex'} >
                                    <Typography id="modal-modal-description" sx={{ mt: 3 }}>
                                        Para ver o passworod  <span> </span>  
                                        <Button 
                                            onClick={handleGetPassWord}
                                            variant="contained" 
                                            size='small' 
                                            >
                                            Clique Aqui
                                        </Button>   
                                    </Typography>
                                   
                                </Grid>
                            </Grid>
                            <Stack spacing={1}>
                                
                                        <OutlinedInput
                                            disabled={true}
                                            fullWidth
                                            id="password"
                                            type={showPassword ? 'text' : 'password'}                                                            
                                            name="password"
                                            value={passValue ?? ''}
                                            endAdornment={
                                                <InputAdornment position="end">
                                                    <IconButton
                                                            aria-label="toggle password visibility"
                                                            onClick={handleClickShowPassword}
                                                            onMouseDown={handleMouseDownPassword}
                                                            edge="end"
                                                            size="large"
                                                    >
                                                        {showPassword ? <Visibility /> : <VisibilityOff />}
                                                        
                                                    </IconButton>
                                                </InputAdornment>
                                            }
                                            placeholder="******"
                                            inputProps={{}}
                                            />
                            </Stack>
                        </Grid>
                        <Grid item xs={11}>
                            <Divider sx={{padding: '30px'}}>
                                <Link variant="return" component={RouterLink}  color="text.primary" fontSize={15}  to='/'>Voltar</Link>
                            </Divider>
                        </Grid>
                        
                    </Grid>
                    
                </Grid>
            </Grid>
            <Backdrop
                sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                open={bkopen}
                onClick={handleCloseBk}
                >
                <CircularProgress color="inherit" />
            </Backdrop>
        </Box>
    );
};

export default PassViewerLink;
