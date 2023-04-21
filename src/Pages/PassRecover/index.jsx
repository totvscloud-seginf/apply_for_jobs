import { useEffect, useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import useRequest from '../../hooks/request';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
// material-ui
import {
    Box,
    Button,
    Divider,
    FormControl,
    FormHelperText,
    Grid,
    Link,
    IconButton,
    InputAdornment,
    InputLabel,
    OutlinedInput,
    Stack,
    CircularProgress,
    Backdrop,
    Checkbox,
    Typography,
    FormControlLabel,
    Modal 
} from '@mui/material';

// third party
import * as Yup from 'yup';
import { Formik } from 'formik';

// project import
 
import AnimateButton from '../../Components/animations/AnimatedButton';
import { strengthColor, strengthIndicator } from '../../utils/password-strength';

// assets
import { Directions, Visibility, VisibilityOff } from '@mui/icons-material';


const PassRecover = () => {
   
    
    const { makeRequest } = useRequest();
    const [level, setLevel] = useState();
    const [showFields, setShowFields] = useState(false)
    const [text, setText] = useState({  type : 1,
                                        title: '',
                                        body: '',
                                        __pass: '',
                                    })
    const [linkHref, setLinkHref] = useState({  
                                                id: 0,
                                                login: '',
                                                locallink: '',
                                                response: {},
                                                link: '' 
                                            })
    const [showPassword, setShowPassword] = useState(false);
    const [autoPassword, setAutoPassword] = useState(false);
    const [showPassInput, setshowPassInput] = useState('');
    const [dataRequestType, setDataRequestType] = useState('');
    const [open, setOpen] = useState(false);
    const [RespData, setRespData] = useState({})
    const [autoPass, setAutoPass] = useState({
                                            number: false,
                                            letter: false,
                                            espChar: false,
                                            passlength: ''
                                          })
    const [btnLabel, setBtnLabel] = useState('Salvar senha')
    const [bkopen, setBkOpen] = useState(false);

    const handleCloseBk = () => {
        setBkOpen(false);
      };
    const handleOpenBk = () => {
        setBkOpen(true);
      };
     
    const handleClose = () => {
        setOpen(false);
        setBkOpen(false);
        
      };
 
    const handleClickShowPassword = () => {
        setShowPassword(!showPassword);
    };

    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };

    const changePassword = (value) => {
        const temp = strengthIndicator(value);
        setLevel(strengthColor(temp));
    };

    const handleCheck = () =>{
        setAutoPassword(!autoPassword)
        if(!autoPassword){
            setBtnLabel('Gerar Senha')
        }else{
            setBtnLabel('Salvar senha')
        }
            
        if(showPassInput === 'none'){
            setshowPassInput('')
            return
        }
        setshowPassInput('none')
    }
  
    const handleCheckBox = (el) => {
        
        if(el.target.id === 'passlength'){
            setAutoPass({...autoPass, [ el.target.id ]: el.target.value })
        }
        else{
            setAutoPass({...autoPass, [ el.target.id ]: el.target.checked })
        }
          
    }

    const handleType = (el) =>{
        const  requestType = el.target.attributes.datarequest.value
        setDataRequestType(requestType)
    }

    const notify = (resp, check_ = true) => { 
        let count = 0  
        toast.error(resp.data, {
            onClose: () => {
                count++
                if (count > 1){
                    
                    if(check_){
                        setShowFields(!showFields)
                        document.getElementById('pass_recovery_btn').style.display = 'none'
                    }
                    if(!check_ && !showFields){
                        document.getElementById('pass_recovery_btn').style.display = 'inline-flex'
                    }
                    if(resp.result === 'WARNING'){
                        setShowFields(!showFields)
                        document.getElementById('pass_recovery_btn').style.display = 'inline-flex'
                    }
                    handleCloseBk()
                }                
            },
            position: "top-right",
            autoClose: 3000,
            closeOnClick: true,                                                            
        });
    
    }

    useEffect(() => {
        changePassword('');
       
    }, []);
    

    const label = { inputProps: { 'aria-label': 'Checkbox demo' } };
    
    
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
                    margin={1}
                >
                    <Grid container item xs={11} lg={4} spacing={2} 
                            sx={{
                                boxShadow: 'rgba(0, 0, 0, 0.15) 0px 2px 8px'
                            }}
                        >
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
                                    login: Yup.string().email('O email deve ser válido').max(255).required('Tem que digitar um email'),
                                    passlifetime : Yup.number().required('É necessário informar um tempo de vida'),
                                    passlimitview : Yup.number().required('É necessário informar um limite de visualizações')
                                })}
                                onSubmit={async (values, { setErrors, setStatus, setSubmitting }) => {
                                    try {
                                        handleOpenBk()
                                        
                                        if (dataRequestType === "do_user_get_link") {
                                            values.password.auto = 'false'
                                            values.password.password = values.senha
                                            const { passlifetime, passlimitview, senha, ...rest } = values
                                            
                                            let req_param = {         
                                                url: 'https://z2jytnr0a7.execute-api.sa-east-1.amazonaws.com/default/userPassValidator/do_user_get_link',
                                                data : rest
                                            };
                                            
                                            let _urllink = window.location.href
                                            _urllink = _urllink.split('/passrecover')[0]
                                            
                                            const response = await makeRequest(req_param)
                                            
                                            if ('resp' in response) {
                                                const resp = response['resp'];
                                                if ('result' in resp){
                                                    const result = resp['result']
                                                    if(result !== 'OK'){
                                                        notify(resp)
                                                        return
                                                    }
                                                }
                                                
                                                const link_gen = 'https://z2jytnr0a7.execute-api.sa-east-1.amazonaws.com/default/userPassValidator/'+resp.currentlink
                                                setText({
                                                    type: 0,
                                                    title: 'Recuperaçao da senha',
                                                    body: 'Para visualizar a senha clique aqui',
                                                    locallink: _urllink+'/passview/'+resp.currentlink+'&login='+values.login+'&link='+window.btoa(unescape(encodeURIComponent(link_gen))),
                                                    __pass: resp.auto_password ?? '' 
                                                })

                                                setLinkHref({
                                                        id: 1,
                                                        login: values.login,
                                                        response: resp,
                                                        userlink: '/passview/'+resp.currentlink+'&login='+values.login+'&link='+window.btoa(unescape(encodeURIComponent(link_gen))),
                                                        link: link_gen
                                                    })
                                                setOpen(true)                                               
                                            };
                                            
                                        }else if(dataRequestType === 'do_user_set_new_pass') {
                                          
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
                                                url: 'https://z2jytnr0a7.execute-api.sa-east-1.amazonaws.com/default/userPassValidator/do_user_set_new_pass',
                                                data : rest
                                            };
                                            
                                            const response = await makeRequest(req_param)
                                            
                                            if ('resp' in response) {
                                                const resp = response['resp'];
                                                
                                                if ('result' in resp) {
                                                    const result = resp['result'];
                                                    notify(resp, false)
                                                    setText({
                                                        title: result,
                                                        body: resp.data,
                                                        __pass: resp.auto_password ?? '' 
                                                    })
                                                    
                                                    
                                                }
                                        
                                            
                                                handleCloseBk()
                                            }  
                                        }
   
                                         
                                        setStatus({ success: false });
                                        setSubmitting(false);
                                    } catch (err) {
                                        console.error(err);
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
                                                       { text.type === 0 ? <RouterLink  to={{pathname : "/passview/"}} state={{linkHref}}  underline='hover'>{text.body}</RouterLink> : text.body }
                                                    </Typography>
                                                    <Typography id="modal-modal-description1" sx={{ mt: 2}}>
                                                        <Typography id="modal-modal-description1" sx={{ mt: 2}}>Você pode usar o link: </Typography>
                                                       { text.type === 0 ? <RouterLink style={{fontSize: '12px', overflowWrap: 'anywhere'}}  to={{ pathname: linkHref.userlink}} underline='hover'>{text.locallink}</RouterLink> : text.body }
                                                    </Typography>
                                                    <Typography id="modal-modal-description2" sx={{ mt: 2 }}>
                                                        {text.__pass}
                                                    </Typography>
                                                </Box>
                                            </Modal>                                              
                                            <Grid item xs={12}>
                                                <Stack spacing={1}>
                                                    <InputLabel htmlFor="email-signup">Digite seu Email</InputLabel>
                                                    <OutlinedInput
                                                        fullWidth
                                                        error={Boolean(touched.email && errors.email)}
                                                        id="email-login"
                                                        type="email"
                                                        value={values.email}
                                                        name="login"
                                                        onBlur={handleBlur}
                                                        onChange={handleChange}
                                                        placeholder="seu@email"
                                                        inputProps={{}}
                                                    />
                                                    {touched.email && errors.email && (
                                                        <FormHelperText error id="helper-text-email-signup">
                                                            {errors.email}
                                                        </FormHelperText>
                                                    )}
                                                </Stack>
                                                
                                                
                                            </Grid>
                                            <Divider />
                                            <Grid item xs={12}>
                                                <Stack spacing={1}>
                                                    <AnimateButton>
                                                        <Button
                                                            disableElevation
                                                            disabled={isSubmitting}
                                                            fullWidth
                                                            size="large"
                                                            type="submit"
                                                            variant="contained"
                                                            id='pass_recovery_btn'
                                                            color="primary"
                                                            onClick={handleType}
                                                            datarequest = 'do_user_get_link'
                                                        >
                                                            Recuperar senha
                                                        </Button>
                                                    </AnimateButton>
                                                </Stack>
                                            </Grid>
                                            <Grid item xs={12}   display={showFields ? '' : 'none'}>
                                                
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
                                            </Grid>
                                            <Grid item xs={12} display={showPassInput? '' : 'none'}>
                                                <Stack spacing={1} justifyContent="flex-start" alignItems="flex-start"  divider={<Divider orientation="horizontal" flexItem />}>
                                                    <Typography variant="paramtitle" fontSize="1.25rem" sx={{backgroundColor: 'transparent'}} >
                                                                Defina os parametros para senha
                                                    </Typography>
                                                    <FormControlLabel
                                                        
                                                        labelPlacement="end"
                                                        control={<Checkbox
                                                                id='number'
                                                                onChange={handleCheckBox}
                                                                {...label}
                                                                sx={{ '& .MuiSvgIcon-root': { fontSize: 28 } }}/>}
                                                        label='Deve conter números'
                                                    />
                                                     <FormControlLabel
                                                        labelPlacement="end"
                                                        control={<Checkbox
                                                                id='letter'
                                                                onChange={handleCheckBox}
                                                                {...label}
                                                                sx={{ '& .MuiSvgIcon-root': { fontSize: 28 } }}/>}
                                                        label='Deve conter letras'
                                                    />
                                                     <FormControlLabel
                                                        labelPlacement="end"
                                                        control={<Checkbox
                                                                id='espChar'
                                                                onChange={handleCheckBox}
                                                                {...label}
                                                                sx={{ '& .MuiSvgIcon-root': { fontSize: 28 } }}/>}
                                                        label='Deve conter caracteres especiais'
                                                    />
                                                    <Grid item xs={12} lg={12}  sx={{width: '100%'}}>
                                                        <FormControlLabel
                                                            sx={{width: '100%'}}
                                                             
                                                            labelPlacement="top"
                                                            control={<OutlinedInput
                                                                        fullWidth
                                                                        id='passlength'
                                                                        onChange={handleCheckBox}
                                                                        sx={{ '& .MuiSvgIcon-root': { fontSize: 28 } }}/>}
                                                            label='Quantidade de caracteres'
                                                        />
                                                    </Grid>
                                                    <Divider />
                                                </Stack>
                                               
                                            </Grid>
                                            <Grid item xs={12} display={showFields ? '' : 'none' }>
                                                <Grid item xs={12} display={showPassInput}>
                                                    <Stack spacing={1}>
                                                        <InputLabel htmlFor="password-signup">Defina uma senha</InputLabel>
                                                        <OutlinedInput
                                                            disabled={autoPassword}
                                                            fullWidth
                                                            error={Boolean(touched.senha && errors.senha)}
                                                            id="password-signup"
                                                            type={showPassword ? 'text' : 'password'}
                                                            value={values.senha}
                                                            name="senha"
                                                            onBlur={handleBlur}
                                                            onChange={(e) => {
                                                                handleChange(e);
                                                                changePassword(e.target.value);
                                                            }}
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
                                                        {touched.senha && errors.senha && (
                                                            <FormHelperText error id="helper-text-password-signup">
                                                                {errors.senha}
                                                            </FormHelperText>
                                                        )}
                                                    </Stack>
                                                    <FormControl fullWidth sx={{ mt: 2 }}>
                                                        <Grid container spacing={2} alignItems="center">
                                                            <Grid item>
                                                                <Box sx={{ bgcolor: level?.color, width: 85, height: 8, borderRadius: '7px' }} />
                                                            </Grid>
                                                            <Grid item>
                                                                <Typography variant="subtitle1" fontSize="0.75rem">
                                                                    {level?.label}
                                                                </Typography>
                                                            </Grid>
                                                        </Grid>
                                                    </FormControl>
                                                </Grid>
                                            </Grid>
                                            {errors.submit && (
                                                <Grid item xs={12}>
                                                    <FormHelperText error>{errors.submit}</FormHelperText>
                                                </Grid>
                                            )}
                                            <Grid item display={showFields ? 'flex' : 'none' } lg={12} xs={12} 
                                                sx={{flexWrap: 'Wrap', alignContent: 'space-between', justifyContent: 'space-between'}} id='grupo2'>
                                                <Grid item xs={6} lg={6}>
                                                    <Stack> 
                                                        <InputLabel htmlFor="email-signup">Definir tempo de vida</InputLabel>
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
                                                        <InputLabel htmlFor="email-signup">Máximo de visualizações</InputLabel>
                                                        <OutlinedInput
                                                            
                                                            error={Boolean(touched.passlimitview && errors.passlimitview)}
                                                            id="passlimitview"
                                                            type="number"
                                                            value={values.passlimitview}
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
                                                <Grid item xs={12} sx={{ paddingTop: '10px'}}>
                                                    <AnimateButton>
                                                        <Button
                                                            disableElevation
                                                            disabled={isSubmitting}
                                                            fullWidth
                                                            size="large"
                                                            type="submit"
                                                            variant="contained"
                                                            color="primary"
                                                            onClick={handleType}
                                                            datarequest="do_user_set_new_pass"
                                                        >
                                                            {btnLabel}
                                                        </Button>
                                                    </AnimateButton>
                                                </Grid>
                                            </Grid>  
                                            <Grid item xs={12}>
                                                <Divider>
                                                    <Link variant="return" component={RouterLink}  color="text.primary" fontSize={15}  to='/'>Voltar para Login</Link>
                                                </Divider>
                                            </Grid>
                                            <Grid item xs={12}>
                                                
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

export default PassRecover;
