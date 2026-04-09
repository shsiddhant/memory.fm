import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './components/homepage';
import Overview from './components/overview';

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
