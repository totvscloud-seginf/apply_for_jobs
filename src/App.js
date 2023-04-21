import { useRoutes, BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './Pages/Login';
import Register from './Pages/Register';
import PassRecover from './Pages/PassRecover';
import PassViewer from './Pages/PasswordViewer';
import PassViewerLink from './Pages/PasswordViewer/index_link';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={< Login/>} />
        <Route path='/register' element={<Register />} />
        <Route path='/passrecover' element={<PassRecover/>} />
        <Route path= '/passview' element={<PassViewer />} component={PassViewer}/>
        <Route path='/passview/:currlink' element={<PassViewerLink  />}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
