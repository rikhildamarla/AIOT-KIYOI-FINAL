import React, { useEffect, useRef, useState } from 'react';
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const Physio = () => {
  const videoRef = useRef(null);
  const [cameraIndex, setCameraIndex] = useState(0); 
  const [cameras, setCameras] = useState([]);

  useEffect(() => {
    fetchCameras();
  }, []);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.src = `http://127.0.0.1:5000/video_feed?camera=${cameraIndex}`;
    }
  }, [cameraIndex]);

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

  const handleCameraChange = event => {
    const newIndex = parseInt(event.target.value, 10);
    setCameraIndex(newIndex);
  };

  return (
    <div>
      <Navbar />
      <h1>Live Video Feed</h1>
      <select value={cameraIndex} onChange={handleCameraChange}>
        {cameras.map((camera, index) => (
          <option key={index} value={index}>{camera}</option>
        ))}
      </select>
      <img ref={videoRef} alt="Video feed" style={{ width: '100%' }} />
      <Footer />
    </div>
  );
};

export default Physio;