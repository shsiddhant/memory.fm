import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './components/homepage';
import Summary from './components/summary';

function App() {

  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/user/:username/summary" element={<Summary />} />
    </Routes>
    </BrowserRouter>
  )
}

export default App
