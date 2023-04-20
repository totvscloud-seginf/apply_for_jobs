import React from 'react';
import { Link as RouterLink } from 'react-router-dom';

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

// ============================|| FIREBASE - LOGIN ||============================ //

const Login = () => {
    const [checked, setChecked] = React.useState(false);

    const [showPassword, setShowPassword] = React.useState(false);
    const handleClickShowPassword = () => {
        setShowPassword(!showPassword);
    };

    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };

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
                            <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                                                        LOGIN 
                            </Typography>
                        <Grid item xs={11} lg={11} 
                             >
                            <Formik
                                initialValues={{
                                    email: 'info@codedthemes.com',
                                    password: '123456',
                                    submit: null
                                }}
                                validationSchema={Yup.object().shape({
                                    email: Yup.string().email('Must be a valid email').max(255).required('Email is required'),
                                    password: Yup.string().max(255).required('Password is required')
                                })}
                                onSubmit={async (values, { setErrors, setStatus, setSubmitting }) => {
                                    try {
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
                                                        value={values.email}
                                                        name="email"
                                                        onBlur={handleBlur}
                                                        onChange={handleChange}
                                                        placeholder="Enter email address"
                                                        fullWidth
                                                        error={Boolean(touched.email && errors.email)}
                                                    />
                                                    {touched.email && errors.email && (
                                                        <FormHelperText error id="standard-weight-helper-text-email-login">
                                                            {errors.email}
                                                        </FormHelperText>
                                                    )}
                                                </Stack>
                                            </Grid>
                                            <Grid item xs={12}>
                                                <Stack spacing={1}>
                                                    <InputLabel htmlFor="password-login">Password</InputLabel>
                                                    <OutlinedInput
                                                        fullWidth
                                                        error={Boolean(touched.password && errors.password)}
                                                        id="-password-login"
                                                        type={showPassword ? 'text' : 'password'}
                                                        value={values.password}
                                                        name="password"
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
                                                    {touched.password && errors.password && (
                                                        <FormHelperText error id="standard-weight-helper-text-password-login">
                                                            {errors.password}
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
        </Box>
    );
};

export default Login;
