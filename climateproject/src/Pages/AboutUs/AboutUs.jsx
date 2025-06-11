import React, { useEffect, useRef, useState } from "react";
import "../../Styles/aboutus.css";

const AboutUs = () => {
  const sectionRef = useRef();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => setVisible(entry.isIntersecting),
      { threshold: 0.2 }
    );
    if (sectionRef.current) observer.observe(sectionRef.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={sectionRef}
      className={`about-section ${visible ? "visible" : ""}`}
    >
      <div className="about-box">
        <h1>About the Website</h1>
        <p>
          This platform, developed by <strong>Coastal Seven Consulting</strong>, uses AI to monitor and predict environmental changes. 
        </p>
        <p>
          Users can explore real-time data on <strong>air quality</strong>, <strong>water pollution</strong>, and <strong>temperature</strong>.
        </p>
        <p>
          Our goal is to make climate data accessible and help communities take informed actions.
        </p>

        <h2>🌱 Mission</h2>
        <p>
          To empower everyone with simple, accurate environmental insights.
        </p>

        <h2>🔭 Vision</h2>
        <p>
          A world where data-driven awareness leads to better climate decisions.
        </p>
      </div>
    </div>
  );
};

export default AboutUs;