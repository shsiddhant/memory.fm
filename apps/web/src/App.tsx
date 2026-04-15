import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './components/pages/homepage';
import Overview from './components/pages/overview';

function App() {

  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/user/:username/overview" element={<Overview />} />
    </Routes>
    </BrowserRouter>
  )
}

export default App
