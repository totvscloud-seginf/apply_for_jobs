import React from 'react';
import { useState } from 'react';
import { Link as RouterLink, Navigate } from 'react-router-dom';
import useRequest from '../../hooks/request';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
// material-ui
import {
    Box,
    Button,
    CircularProgress,
    Divider,
    Backdrop,
    FormHelperText,
    Grid,
    Link,
    IconButton,
    InputAdornment,
    InputLabel,
    OutlinedInput,
    Stack,
    Modal,
    Typography
} from '@mui/material';

// third party
import * as Yup from 'yup';
import { Formik } from 'formik';

 
import AnimateButton from '../../Components/animations/AnimatedButton';

// assets
import { Visibility, VisibilityOff } from '@mui/icons-material';

const Login = () => {
    const { makeRequest } = useRequest();
    const { navigate } = useNavigate()
    const [alertType, setAlertType] = useState('');
     
    const [bkopen, setBkOpen] = useState(false);
    const [text, setText] = useState({
        title: '',
        body: ''
    })
    const [open, setOpen] = useState(false);
    const [showPassword, setShowPassword] = React.useState(false);
    const handleClickShowPassword = () => {
        setShowPassword(!showPassword);
    };

    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };

    const handleCloseBk = () => {
        setBkOpen(false);
      };

    const handleOpenBk = () => {
        setBkOpen(true);
      };

    const handleClose = () => {
        setOpen(!open);
        if(text.title === 'OK'){
            navigate('/')
        }        
    };
 

    return (
        <Box sx={{ minHeight: '100vh' }}>
            <ToastContainer />
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
                    
                    <Grid container xs={8} lg={5} spacing={4} 
                            sx={{
                                boxShadow: 'rgba(0, 0, 0, 0.15) 0px 2px 8px'
                            }}
                        >   <Grid item lg={12} xs={12}>
                                <Typography id="login-tittle" sx={{ mt: 2 }}>
                                    LOGIN 
                                </Typography>
                            </Grid>
                            
                        <Grid item xs={11} lg={11} 
                             >
                            <Formik
                                initialValues={{
                                    login: '',
                                    senha: '',
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
                                    }}
                                validationSchema={Yup.object().shape({
                                    login: Yup.string().email('Must be a valid email').max(255).required('Email is required'),
                                    senha: Yup.string().max(255).required('Password is required')
                                })}
                                onSubmit={async (values, { setErrors, setStatus, setSubmitting }) => {
                                    try {
                                        handleOpenBk()
                                        
                                       
                                        values.password.password = values.senha
                                        const { passlifetime, passlimitview, senha, ...rest } = values
                                        
                                        console.log(rest)
                                        let req_param = {         
                                            url: 'https://z2jytnr0a7.execute-api.sa-east-1.amazonaws.com/default/userPassValidator/do_user_login',
                                            data : rest
                                        };
                                        const response = await makeRequest(req_param)
                                        
                                        if ('resp' in response) {
                                            const resp = response['resp'];
                                            
                                            if ('result' in resp) {
                                                const result = resp['result'];
                                                setText({
                                                    title: result,
                                                    body: resp.data,                                                    
                                                })
                                               
                                               if(result === 'OK') {
                                                    toast.success('Logado com sucesso!', {
                                                        position: "top-right",
                                                        autoClose: 5000,
                                                        hideProgressBar: false,
                                                        closeOnClick: true,
                                                        pauseOnHover: false,
                                                        draggable: true,
                                                        progress: undefined,
                                                        theme: "light",
                                                    });
                                               }else {
                                                toast.error(resp.data, {
                                                    position: "top-right",
                                                    autoClose: 5000,
                                                    hideProgressBar: false,
                                                    closeOnClick: true,
                                                    pauseOnHover: false,
                                                    draggable: true,
                                                    progress: undefined,
                                                    theme: "light",
                                                });

                                               }
                                                
                                            }
                                           
                                          
                                            handleCloseBk()
                                        }
                                        setStatus({ success: false });
                                        setSubmitting(false);
                                    } catch (err) {
                                        setStatus({ success: false });
                                        setErrors({ submit: err.message });
                                        setSubmitting(false);
                                    }
                                }}
                            >
                                {({ errors, handleBlur, handleChange, handleSubmit, isSubmitting, touched, values }) => (
                                    <form noValidate onSubmit={handleSubmit}>
                                        <Grid container spacing={3}>
                                            <Grid item xs={12}>
                                                <Stack spacing={1}>
                                                    <InputLabel htmlFor="email-login">Email Address</InputLabel>
                                                    <OutlinedInput
                                                        id="email-login"
                                                        type="email"
                                                        value={values.login}
                                                        name="login"
                                                        onBlur={handleBlur}
                                                        onChange={handleChange}
                                                        placeholder="Enter email address"
                                                        fullWidth
                                                        error={Boolean(touched.login && errors.login)}
                                                    />
                                                    {touched.login && errors.login && (
                                                        <FormHelperText error id="standard-weight-helper-text-email-login">
                                                            {errors.login}
                                                        </FormHelperText>
                                                    )}
                                                </Stack>
                                            </Grid>
                                            <Grid item xs={12}>
                                                <Stack spacing={1}>
                                                    <InputLabel htmlFor="password-login">Password</InputLabel>
                                                    <OutlinedInput
                                                        fullWidth
                                                        error={Boolean(touched.senha && errors.senha)}
                                                        id="-password-login"
                                                        type={showPassword ? 'text' : 'password'}
                                                        value={values.senha}
                                                        name="senha"
                                                        onBlur={handleBlur}
                                                        onChange={handleChange}
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
                                                        placeholder="Enter password"
                                                    />
                                                    {touched.senha && errors.senha && (
                                                        <FormHelperText error id="standard-weight-helper-text-senha-login">
                                                            {errors.senha}
                                                        </FormHelperText>
                                                    )}
                                                </Stack>
                                            </Grid>

                                            <Grid item xs={12} sx={{ mt: -1 }}>
                                                <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={2}>
                                                   
                                                    <Link variant="h6" component={RouterLink} to='./register' color="text.primary" fontSize={15}>
                                                        Cadastre-se
                                                    </Link>
                                                    <Link variant="h6" component={RouterLink} to='./passrecover' color="text.primary" fontSize={15}>
                                                        Esqueceu a senha?
                                                    </Link>
                                                </Stack>
                                            </Grid>
                                            {errors.submit && (
                                                <Grid item xs={12}>
                                                    <FormHelperText error>{errors.submit}</FormHelperText>
                                                </Grid>
                                            )}
                                            <Grid item xs={12}>
                                                <AnimateButton>
                                                    <Button
                                                        disableElevation
                                                        disabled={isSubmitting}
                                                        fullWidth
                                                        size="large"
                                                        type="submit"
                                                        variant="contained"
                                                        color="primary"
                                                    >
                                                        Login
                                                    </Button>
                                                </AnimateButton>
                                            </Grid>
                                            <Grid item xs={12}>
                                                <Divider>
                                                   
                                                </Divider>
                                            </Grid>
                                        </Grid>
                                    </form>
                                )}
                            </Formik>
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

export default Login;
