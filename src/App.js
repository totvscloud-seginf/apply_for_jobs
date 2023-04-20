import { useRoutes, BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './Pages/Login';
import Register from './Pages/Register';
import PassViewer from './Pages/PasswordViewer';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={< Login/>} />
        <Route path='/register' element={<Register />} />
        <Route path='/passview' element={<PassViewer  />} component={PassViewer}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
