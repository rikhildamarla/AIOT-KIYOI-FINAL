import React from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.min.js"

import Home from "./pages/Home";
import Physio from "./pages/Physio";
import Psycho from "./pages/Psycho";

function App() {
  return (
   <BrowserRouter>
   <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/physio" element={<Physio />} />
    <Route path="/psycho" element={<Psycho />} />
   </Routes>
   </BrowserRouter>
  )
}

export default App


