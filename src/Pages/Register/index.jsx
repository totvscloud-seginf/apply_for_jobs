import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useRequest from '../../hooks/request';
// material-ui
import {
    Box,
    Button,
    Checkbox,
    Divider,
    Backdrop,
    CircularProgress,
    FormHelperText,
    Grid,
    Link,
    IconButton,
    InputAdornment,
    InputLabel,
    OutlinedInput,
    Stack,
    Modal,
    FormControlLabel,
    Typography
} from '@mui/material';

// third party
import * as Yup from 'yup';
import { Formik, useFormik } from 'formik';

 
import AnimateButton from '../../Components/animations/AnimatedButton';

// assets
import { AutoAwesome, Visibility, VisibilityOff } from '@mui/icons-material';

const Register = () => {
    const navigate = useNavigate()
    
    const [showPassword, setShowPassword] = useState(false);
    const [bkopen, setBkOpen] = useState(false);
    const [text, setText] = useState({
        title: '',
        body: ''
    })
    
    const { makeRequest } = useRequest();
    const [showPassInput, setshowPassInput] = useState('');
    const [open, setOpen] = useState(false);
    const [autoPass, setAutoPass] = useState({
        number: false,
        letter: false,
        espChar: false,
        passlength: ''
      })
    const label = { inputProps: { 'aria-label': 'Checkbox demo' } };

    const handleClickShowPassword = () => {
        setShowPassword(!showPassword);
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
    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };

    const handleCheckBox = (el) => {
        if(el.target.id === 'passlength'){
            setAutoPass({...autoPass, [ el.target.id ]: el.target.value })
        }
        else{
            setAutoPass({...autoPass, [ el.target.id ]: el.target.checked })
        }          
    }
    
    const handleCheck = () =>{
        
        if(showPassInput === 'none'){
            setshowPassInput('')
            return
        }
        setshowPassInput('none')
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
                     
                  
                >   
                    <Grid container xs={8} lg={5} spacing={4}  
                            sx={{
                                boxShadow: 'rgba(0, 0, 0, 0.15) 0px 2px 8px'
                            }}
                        >
                        <Grid item lg={12} xs={12}>
                            <Typography id="register-tittle" sx={{ mt: 2 }}>
                                REGISTRO 
                            </Typography>
                        </Grid>
                        <Grid item xs={11} lg={11} 
                             >
                            <Formik
                               initialValues={{
                                login: '',
                                senha: '',
                                passlifetime: 0,
                                passlimitview: 0,
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
                                    passlifetime : Yup.number().required('É necessário informar um tempo de vida'),
                                    passlimitview : Yup.number().required('É necessário informar um limite de visualizações')
                                })}
                                onSubmit={async (values, { setErrors, setStatus, setSubmitting }) => {
                                    try {
                                        
                                        handleOpenBk()
                                        
                                        values.password.auto = 'false'
                                        if (autoPass.number || autoPass.espChar || autoPass.letter || autoPass.passlength){
                                            values.password.auto = 'true'
                                            values.password.params.numbers = autoPass.number
                                            values.password.params.espChar = autoPass.espChar
                                            values.password.params.letter = autoPass.letter
                                            values.password.params.passlen = autoPass.passlength
                                        }
                                        values.password.password = values.senha
                                        const { passlifetime, passlimitview, senha, ...rest } = values
                                        

                                        rest.password.passlifetime = values.passlifetime
                                        rest.password.passlimitview = values.passlimitview
                                        
                                        let req_param = {         
                                            url: 'https://z2jytnr0a7.execute-api.sa-east-1.amazonaws.com/default/userPassValidator/do_save_new_user',
                                            data : rest
                                        };
                                        const response = await makeRequest(req_param)
                                        console.log(response)
                                        if ('resp' in response) {
                                            const resp = response['resp'];
                                            console.log(resp)
                                            if ('result' in resp) {
                                                const result = resp['result'];
                                                
                                                setText({
                                                    title: result,
                                                    body: resp.data,
                                                    __pass: resp.auto_password ?? '' 
                                                })
                                                setOpen(!open)
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
                                            
                                            <Modal open={open}
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
                                                        {text.title}
                                                    </Typography>
                                                    <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                                                        {text.body}
                                                    </Typography>
                                                    <Typography id="modal-modal-description2" sx={{ mt: 2 }}>
                                                        {text.__pass}
                                                    </Typography>
                                                </Box>
                                            </Modal>
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
                                                        error={Boolean(touched.senha && errors.senha )}
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
                                                    {touched.senha  && errors.senha  && (
                                                        <FormHelperText error id="standard-weight-helper-text-password-login">
                                                            {errors.senha}
                                                        </FormHelperText>
                                                    )}
                                                </Stack>
                                            </Grid>

                                            {errors.submit && (
                                                <Grid item xs={12}>
                                                    <FormHelperText error>{errors.submit}</FormHelperText>
                                                </Grid>
                                            )}
                                            
                                            <Grid item xs={12}>
                                                
                                                <Stack spacing={1}>
                                                    <FormControlLabel
                                                        labelPlacement="start"
                                                        
                                                        control={<Checkbox
                                                                name='auto'
                                                                onChange={handleCheck}
                                                                {...label}
                                                                sx={{ '& .MuiSvgIcon-root': { fontSize: 28 } }}/>}
                                                        label='Gerar senha Aleatória?'
                                                    />                                                        
                                                    
                                                </Stack>
                                                <Grid item display={'flex'} lg={12} xs={12} 
                                                    sx={{flexWrap: 'Wrap', alignContent: 'space-between', justifyContent: 'space-between'}} id='grupo2'>
                                                    <Grid item xs={6} lg={6}>
                                                        <Stack> 
                                                            <InputLabel htmlFor="passlifetime">Definir tempo de vida</InputLabel>
                                                            <OutlinedInput                                                                
                                                                error={Boolean(touched.passlifetime && errors.passlifetime)}
                                                                id="passlifetime"
                                                                type="number"
                                                                value={values.lifetime}
                                                                name="passlifetime"
                                                                onBlur={handleBlur}
                                                                onChange={handleChange}
                                                                placeholder="Valores em horas"
                                                                inputProps={{}}
                                                            />
                                                            {touched.passlifetime && errors.passlifetime && (
                                                                <FormHelperText error id="helper-text-email-signup">
                                                                    {errors.passlifetime}
                                                                </FormHelperText>
                                                            )}
                                                        </Stack>
                                                    </Grid>
                                                    <Grid item xs={6} lg={6}>
                                                        <Stack sx={{ minWidth: 0 }}>
                                                            <InputLabel htmlFor="passlimitview">Máximo de visualizações</InputLabel>
                                                            <OutlinedInput
                                                                
                                                                error={Boolean(touched.passlimitview && errors.passlimitview)}
                                                                id="passlimitview"
                                                                type="number"
                                                                value={values.maxview}
                                                                name="passlimitview"
                                                                onBlur={handleBlur}
                                                                onChange={handleChange}
                                                                placeholder="Link poderá ser aberto n vezes"
                                                                inputProps={{}}
                                                            />
                                                            {touched.passlimitview && errors.passlimitview && (
                                                                <FormHelperText error id="helper-text-email-signup">
                                                                    {errors.passlimitview}
                                                                </FormHelperText>
                                                            )}
                                                        </Stack>
                                                    </Grid>
                                                </Grid>
                                                <Grid item xs={12} display={showPassInput? '' : 'none'}>
                                                    <Stack spacing={1} justifyContent="flex-start" alignItems="flex-start"  divider={<Divider orientation="horizontal" flexItem />}>
                                                        <Typography variant="paramtitle" fontSize="1.25rem" sx={{backgroundColor: 'transparent'}} >
                                                                    Defina os parametros para senha
                                                        </Typography>
                                                        <FormControlLabel
                                                            name='numbers'
                                                            labelPlacement="end"
                                                            control={<Checkbox
                                                                    id='number'
                                                                    name='numbers'
                                                                    onChange={handleCheckBox}
                                                                    {...label}
                                                                    sx={{ '& .MuiSvgIcon-root': { fontSize: 28 } }}/>}
                                                            label='Deve conter números'
                                                        />
                                                        <FormControlLabel
                                                            labelPlacement="end"
                                                            control={<Checkbox
                                                                    id='letter'
                                                                    name='letter'
                                                                    onChange={handleCheckBox}
                                                                    {...label}
                                                                    sx={{ '& .MuiSvgIcon-root': { fontSize: 28 } }}/>}
                                                            label='Deve conter letras'
                                                        />
                                                        <FormControlLabel
                                                            labelPlacement="end"
                                                            control={<Checkbox
                                                                    id='espChar'
                                                                    name='espChar'
                                                                    onChange={handleCheckBox}
                                                                    {...label}
                                                                    sx={{ '& .MuiSvgIcon-root': { fontSize: 28 } }}/>}
                                                            label='Deve conter caracteres especiais'
                                                        />
                                                        <Grid item xs={12} lg={12}  sx={{width: '100%'}}>
                                                            <FormControlLabel
                                                                sx={{width: '100%'}}                                                                
                                                                labelPlacement="top"
                                                                value={values.password.passlen}
                                                                
                                                                control={<OutlinedInput
                                                                            fullWidth
                                                                            value={values.password.passlen}
                                                                            id='passlength'
                                                                            name='passlength'
                                                                            onChange={handleCheckBox}
                                                                            sx={{ '& .MuiSvgIcon-root': { fontSize: 28 } }}/>}
                                                                label='Quantidade de caracteres'
                                                            />
                                                        </Grid>
                                                        <Divider />
                                                    </Stack>
                                               
                                                </Grid>
                                                <Grid item xs={12} sx={{marginTop: '20px', marginBottom: '20px'}}>
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
                                                        Registrar
                                                    </Button>
                                                    </AnimateButton>
                                                </Grid>
                                                <Grid>
                                                    <Divider> </Divider>
                                                </Grid>
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

export default Register;
