import React from 'react';
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./Home.css"; 

function Home() {
  return (
    <div>
      <Navbar />
      <div className="hero-section">
        <div className="container">
          <div className="hero-content">
            <h1>Welcome to All In One Therapy</h1>
            <p>
              We provide comprehensive therapy services to help you achieve optimal health and wellness.<br />
              Our selection of AI therapists are designed to aid you and support your well-being.
            </p>
            <p>
              Whether you need physiotherapy or psychotherapy, or other specialized services, we're here to support you on your journey.
            </p>
          </div>
          <div className="hero-image">
            <img src="/hero_icons.png" alt="Hero Icons" />
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Home;
