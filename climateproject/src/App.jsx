import React from 'react'
import RegisterForm from './Pages/RegisterForm/RegisterForm'
import SignInForm from './Pages/SignInForm/SignInForm'
import ThirdPage from './Pages/ThirdPage/ThirdPage'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Landing from './Pages/LandingPage/Landing'
import AboutUs from './Pages/AboutUs/AboutUs'
import ContactForm from './Pages/Contactform/ContactForm'
import Test from './Pages/testing/Test'
import Globe from './Pages/Test/Globe'
const App = () => {
  return (
    // <Router>
    //   <Routes>
    //     <Route path="/" element={<Test />} /> 
    //     <Route path="/signin" element={<SignInForm />} />
    //     <Route path="/register" element={<RegisterForm />} /> 
    //     <Route path="/third" element={<ThirdPage />} />
    //     <Route path="/about" element={<AboutUs />} />
    //     <Route path="/contact" element={<ContactForm />} />
       
    //   </Routes>
    // </Router>
    <>
    <Globe />
    </>
  );
};

export default App;