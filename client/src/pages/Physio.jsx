import React, { useEffect, useRef, useState } from 'react';
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./Physio.css";
import muscularSystemImage from '../other_assets/muscular_system.png'; 
import getStarted from '../other_assets/get_started.png'; 
import bodyImage from '../other_assets/human_labeled.png'; 
import tempGif from '../other_assets/temp.gif'; 
import temp2Gif from '../other_assets/temp2.gif'; 

const imageList = [
  "exer1.png",
  "exer2.png",
  "exer3.png",
  "exer4.png",
  "exer5.png",
  "exer6.png",
];

function Physio() {
  const videoRef = useRef(null);
  const [cameraIndex, setCameraIndex] = useState(0); 
  const [cameras, setCameras] = useState([]);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [showButton, setShowButton] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [showTherapyModal, setShowTherapyModal] = useState(false);
  const [textBoxValue, setTextBoxValue] = useState("");

  useEffect(() => {
    fetchCameras();
  }, []);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.src = `http://127.0.0.1:5000/video_feed?camera=${cameraIndex}`;
    }
  }, [cameraIndex, videoRef]);
  
  const fetchCameras = () => {
    fetch('http://127.0.0.1:5000/cameras')
      .then(response => response.json())
      .then(data => {
        setCameras(data.cameras);
        if (data.cameras.length > 0) {
          setCameraIndex(0); 
        }
      })
      .catch(error => {
        console.error('Error fetching cameras:', error);
      });
  };

  const openModal = () => {
    setShowModal(true);
  };

  const openTherapyModal = () => {
    setShowTherapyModal(true);
  };

  const resetModal = () => {
    setTextBoxValue("");
    setShowModal(false);
  };

  const resetTherapyModal = () => {
    setTextBoxValue("");
    setShowTherapyModal(false);
  };

  const scrollToDiagram = () => {
    const diagramElement = document.getElementById("diagram");
    if (diagramElement) {
      diagramElement.scrollIntoView({ behavior: "smooth" });
    } else {
      console.error("Element with id 'diagram' not found.");
    };
  };

  const handleScroll = () => {
    setShowButton(window.scrollY <= 100);
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const addToTextBox = (text) => {
    setTextBoxValue(textBoxValue + text);
  };

  const clearTextBox = () => {
    setTextBoxValue("");
  };

  const handleCameraChange = event => {
    const newIndex = parseInt(event.target.value, 10);
    setCameraIndex(newIndex);
  };

  return (
    <div className="physio-container">
      <div className="left-rect"></div>
      <div className="right-rect"></div>
      <Navbar />
      <div className="content">
        <div className="collage-container">
          {imageList.map((image, index) => (
            <img
              key={index}
              src={`/pics_physio/${image}`}
              alt={`Exercise ${index + 1}`}
              className={`slideshow-image ${index === currentImageIndex ? 'active' : ''}`}
            />
          ))}
        </div>
        <div className="sample-text" style={{ fontSize: '200px' }}>THIS IS <br/>THE FIRST STEP <br/>TOWARD YOUR <br/>PHYSICAL GOALS.......<br/>.....↓ </div>
        <div className={`centered-button ${showButton ? 'show' : 'hide'}`}>
          <button className="start-button" onClick={scrollToDiagram}>Start Your Physiotherapy Journey↓</button>
        </div>
        <div className="image-container">
          <div className="pain-buttons-container">
            <img src={muscularSystemImage} alt="Muscular System" onClick={openModal} /> 
          </div>
          <div className="get-started-container">
            <img src={getStarted} alt="Get Started IMG" /> 
          </div>
        </div>
      </div>
      <Footer />
      <div id="diagram" className="diagram-container">
      </div>
      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <div className="sample-text" style={{ fontSize: '20px', fontWeight: 'bold', textDecoration: 'underline' }}>LET'S START BY DETERMINING KEY AREAS WHERE YOU FEEL PAIN/DISCOMFORT...<br/> </div>
            <img src={bodyImage} alt="Body Image" />
            <div className="button-container">
              <button className="red-button" onClick={() => addToTextBox("(N), ")}>(N) - Neck</button>
              <button className="red-button" onClick={() => addToTextBox("(C), ")}>(C) - Core</button>
              <button className="red-button" onClick={() => addToTextBox("(LS), ")}>(LS) - Left Shoulder</button>
              <button className="red-button" onClick={() => addToTextBox("(RS), ")}>(RS) - Right Shoulder</button>
              <button className="red-button" onClick={() => addToTextBox("(LE), ")}>(LE) - Left Elbow</button>
              <button className="red-button" onClick={() => addToTextBox("(RE), ")}>(RE) - Right Elbow</button>
              <button className="red-button" onClick={() => addToTextBox("(LW), ")}>(LW) - Left Wrist</button>
              <button className="red-button" onClick={() => addToTextBox("(RW), ")}>(RW) - Right Wrist</button>
              <button className="red-button" onClick={() => addToTextBox("(LH), ")}>(LH) - Left Hip</button>
              <button className="red-button" onClick={() => addToTextBox("(RH), ")}>(RH) - Right Hip</button>
              <button className="red-button" onClick={() => addToTextBox("(LK), ")}>(LK) - Left Knee</button>
              <button className="red-button" onClick={() => addToTextBox("(RK), ")}>(RK) - Right Knee</button>
              <button className="red-button" onClick={() => addToTextBox("(LF), ")}>(LF) - Left Foot</button>
              <button className="red-button" onClick={() => addToTextBox("(RF), ")}>(RF) - Right Foot</button>
              <textarea className="text-box" value={textBoxValue} readOnly />
              <button className="clear-button" onClick={clearTextBox}>Clear</button>
              <button className="close-button" onClick={resetModal}>Close</button>
              {textBoxValue.includes("(N), (LS), (RS), ") ? (
                <button className="green-button" onClick={openTherapyModal}>Launch Therapy Session!</button>
              ) : (
                <div className="coming-soon-modal">
                    <div className="sample-text" style={{ fontSize: '10px', fontWeight: 'bold', textDecoration: 'underline' }}>This Exercise does not exist, choose differnt target areas..</div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {showTherapyModal && (
        <div className="modal">
          <div className="modal-content">
            <h1>Therapy Session</h1>
            <div className="therapy-session-content">
              <div className="video-container">
                <h2>Live Video Feed, Choose Your Camera and Start!</h2>
                <select value={cameraIndex} onChange={handleCameraChange}>
                  {cameras.map((camera, index) => (
                    <option key={index} value={index}>{camera}</option>
                  ))}
                </select>
                <img ref={videoRef} alt="Video feed" style={{ width: '100%' }} />
                <h3 className="exercise-description">Exercise Description:</h3>
                <h3>Push-Ups: <br />A classic exercise where you position yourself on the<br /> floor or against a wall and exert a force <br />perpendicular to the surface you are on, <br />typically using your arms to lift br and lower your body.</h3>
              </div>
              <div className="gif-container">
                <img src={tempGif} alt="Exercise GIF" />
                <img src={temp2Gif} alt="Exercise GIF 2" /> 
              </div>
            </div>
            <button className="reset-button" onClick={resetTherapyModal}>Reset</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Physio;

