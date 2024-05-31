import React, { useEffect, useState } from 'react';
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./Physio.css";

const imageList = [
  "exer1.png",
  "exer2.png",
  "exer3.png",
  "exer4.png",
  "exer5.png",
  "exer6.png",
];

function Physio() {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [showButton, setShowButton] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % imageList.length);
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const scrollToDiagram = () => {
    const diagramElement = document.getElementById("diagram");
    if (diagramElement) {
      diagramElement.scrollIntoView({ behavior: "smooth" });
    } else {
      console.error("Element with id 'diagram' not found.");
    }
  };

  const handleScroll = () => {
    if (window.scrollY > 100) {
      setShowButton(false);
    } else {
      setShowButton(true);
    }
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <div className="physio-container">
      <div className="left-rect"></div>
      <div className="right-rect"></div>
      <Navbar />
      <div className="content">
        <div className="image-slideshow">
          <img src={`/pics_physio/${imageList[currentImageIndex]}`} alt="Slideshow" className="slideshow-image" />
        </div>
        <div className={`centered-button ${showButton ? 'show' : 'hide'}`}>
          <button className="start-button" onClick={scrollToDiagram}>Start↓</button>
        </div>
      </div>
      <Footer />
      <div id="diagram" className="diagram-container">
        <div className="body-parts">
          <div className="body-parts-row">
            <button className="circle-button">N</button>
          </div>
          <div className="body-parts-row">
            <button className="circle-button">LS</button>
            <button className="circle-button">RS</button>
          </div>
          <div className="body-parts-row">
            <button className="circle-button">LE</button>
            <button className="circle-button">RE</button>
          </div>
          <div className="body-parts-row">
            <button className="circle-button">C</button>
          </div>
          <div className="body-parts-row">
            <button className="circle-button">H</button>
          </div>
          <div className="body-parts-row">
            <button className="circle-button">LQ</button>
            <button className="circle-button">RQ</button>
          </div>
          <div className="body-parts-row">
            <button className="circle-button">LK</button>
            <button className="circle-button">RK</button>
          </div>
          <div className="body-parts-row">
            <button className="circle-button">LA</button>
            <button className="circle-button">RA</button>
          </div>
        </div>
        <div className="submit-button-container">
          <div className="text-above-submit">
            (N) - neck<br />
            (LS) - left shoulder<br />
            (LE) - left elbow<br />
            (RS) - right shoulder<br />
            (RE) - right elbow<br />
            (C) - core<br />
            (H) - hip<br />
            (LQ) - left quad<br />
            (LK) - left knee<br />
            (LA) - left ankle<br />
            (RQ) - right quad<br />
            (RK) - right knee<br />
            (RA) - right ankle
          </div>
          <button className="submit-button">Submit</button>
        </div>
      </div>
    </div>
  );
}

export default Physio;
