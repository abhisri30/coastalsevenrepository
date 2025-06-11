import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { VscArrowLeft } from "react-icons/vsc";
import "../../Styles/ThirdPage.css";
import asia from "../../assets/asia.png";

const continentData = {
  Asia: {
    description: 'Asia is the largest continent by both area and population.',
    background: asia,
  },
  Africa: {
    description: 'Africa is known for its diverse culture and wildlife.',
    background: '/images/africa.jpg',
  },
  Europe: {
    description: 'Europe is known for its rich history and cultural diversity.',
    background: '/images/europe.jpg',
  },
  NorthAmerica: {
    description: 'North America includes Canada, the US, and Mexico.',
    background: '/images/northamerica.jpg',
  },
  SouthAmerica: {
    description: 'South America features the Amazon rainforest and Andes mountains.',
    background: '/images/southamerica.jpg',
  },
  Australia: {
    description: 'Australia is a continent and country known for its unique wildlife.',
    background: '/images/australia.jpg',
  },
  Antarctica: {
    description: 'Antarctica is the coldest and southernmost continent.',
    background: '/images/antarctica.jpg',
  }
};

// Fallback data in case API fails
const sampleData = {
  Asia: { airQuality: { pm25: 'Moderate', ozone: 'Safe' }, seaLevel: { rise: '3.2 mm/year', risk: 'Coastal cities' } },
  Africa: { airQuality: { pm25: 'Good', ozone: 'Moderate' }, seaLevel: { rise: '2.8 mm/year', risk: 'Delta regions' } },
  Europe: { airQuality: { pm25: 'Unhealthy', ozone: 'Unsafe' }, seaLevel: { rise: '3.1 mm/year', risk: 'Mediterranean coast' } },
  NorthAmerica: { airQuality: { pm25: 'Moderate', ozone: 'Safe' }, seaLevel: { rise: '3.5 mm/year', risk: 'East coast cities' } },
  SouthAmerica: { airQuality: { pm25: 'Good', ozone: 'Safe' }, seaLevel: { rise: '3.0 mm/year', risk: 'Amazon basin' } },
  Australia: { airQuality: { pm25: 'Good', ozone: 'Safe' }, seaLevel: { rise: '2.9 mm/year', risk: 'Great Barrier Reef' } },
  Antarctica: { airQuality: { pm25: 'Excellent', ozone: 'Thin' }, seaLevel: { rise: '1.2 mm/year', risk: 'Global melt impact' } },
};

const ThirdPage = () => {
  const [activeTab, setActiveTab] = useState('Description');
  const [selectedContinent, setSelectedContinent] = useState('');
  const [showPrompt, setShowPrompt] = useState(true);
  const [data, setData] = useState(null);
  const [typedText, setTypedText] = useState('');
  const [charIndex, setCharIndex] = useState(0);
  const [loading, setLoading] = useState(false);

  // Prompt user to enter continent
  useEffect(() => {
    if (showPrompt) {
      const name = prompt("Enter continent name (Asia, Africa, Europe, NorthAmerica, SouthAmerica, Australia, Antarctica):");
      if (continentData[name]) {
        setSelectedContinent(name);
        setShowPrompt(false);
      } else {
        alert('Invalid continent name. Please reload and try again.');
      }
    }
  }, [showPrompt]);

  // Fetch data from backend using POST /climate/info
  useEffect(() => {
    if (!selectedContinent) return;

    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await axios.post('http://127.0.0.1:8020/climate/info', {
          data_type: "climate",
          continents: [selectedContinent]
        }, {
          headers: { 'Content-Type': 'application/json' }
        });

        // Assuming the response is like: { Asia: { airQuality: ..., seaLevel: ... } }
        const climateInfo = response.data[selectedContinent] || {};
        setData(climateInfo);
      } catch (error) {
        console.error("API error, using sample data:", error);
        setData(sampleData[selectedContinent] || {});
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedContinent]);

  // Typing effect
  useEffect(() => {
    if (!selectedContinent || !data) return;

    let fullText = '';
    const defaultDesc = continentData[selectedContinent].description;
    const air = data.airQuality || {};
    const sea = data.seaLevel || {};

    if (activeTab === 'Air Quality') {
      fullText = `Air Quality - PM2.5: ${air.pm25 || 'N/A'}, Ozone: ${air.ozone || 'N/A'}.`;
    } else if (activeTab === 'Sea Level') {
      fullText = `Sea Level - Rise: ${sea.rise || 'N/A'}, Risk Zones: ${sea.risk || 'N/A'}.`;
    } else {
      fullText = defaultDesc;
    }

    setTypedText('');
    setCharIndex(0);

    const interval = setInterval(() => {
      setCharIndex(prev => {
        const next = prev + 1;
        setTypedText(fullText.substring(0, next));
        if (next >= fullText.length) clearInterval(interval);
        return next;
      });
    }, 40);

    return () => clearInterval(interval);
  }, [selectedContinent, activeTab, data]);

  const continent = continentData[selectedContinent];
  if (!continent || !data) return null;

  return (
    <div className="continent-page">
      <div className="top-bar">
        <button className="back-button" onClick={() => setShowPrompt(true)}>
          <VscArrowLeft size={24} />
        </button>
        <div className="tabs">
          <button className={activeTab === 'Description' ? 'active' : ''} onClick={() => setActiveTab('Description')}>Description</button>
          <button className={activeTab === 'Air Quality' ? 'active' : ''} onClick={() => setActiveTab('Air Quality')}>Air Quality</button>
          <button className={activeTab === 'Sea Level' ? 'active' : ''} onClick={() => setActiveTab('Sea Level')}>Sea Level</button>
        </div>
      </div>

      <div className="content-container">
        <div className="image-container">
          <img src={continent.background} alt={selectedContinent} className="continent-image" />
        </div>

        <div className="sidebar">
          <h2 className="continent-title">{selectedContinent}</h2>
          <div className="typing-text">
            {loading ? (
              <p>Loading climate info...</p>
            ) : (
              <p>{typedText}<span className="cursor">|</span></p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThirdPage;
