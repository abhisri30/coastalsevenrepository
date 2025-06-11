import React, { useEffect, useState } from 'react';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_worldLow from "@amcharts/amcharts4-geodata/worldLow";
import am4geodata_continentsLow from "@amcharts/amcharts4-geodata/continentsLow";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";
import '../../Styles/Test.css';
import NavBar from '../../Components/NavBar';

am4core.useTheme(am4themes_animated);

const TypingOverlay = () => {
  const lines = [
    { text: 'Welcome to', className: 'line-welcome' },
    { text: 'Coastal Seven Consulting', className: 'line-name' },
    { text: 'Are you ready to explore?', className: 'line-ready' },
  ];

  const [typedLines, setTypedLines] = useState(lines.map(() => ''));
  const [currentLineIndex, setCurrentLineIndex] = useState(0);
  const [currentCharIndex, setCurrentCharIndex] = useState(0);

  useEffect(() => {
    let timeoutId;
    if (currentLineIndex < lines.length) {
      if (currentCharIndex < lines[currentLineIndex].text.length) {
        timeoutId = setTimeout(() => {
          setTypedLines(prev => {
            const newLines = [...prev];
            newLines[currentLineIndex] += lines[currentLineIndex].text[currentCharIndex];
            return newLines;
          });
          setCurrentCharIndex(prev => prev + 1);
        }, 50);
      } else {
        timeoutId = setTimeout(() => {
          setCurrentLineIndex(prev => prev + 1);
          setCurrentCharIndex(0);
        }, 300);
      }
    }
    return () => clearTimeout(timeoutId);
  }, [currentCharIndex, currentLineIndex, lines]);

  return (
    <div className="typing-overlay">
      {typedLines.map((line, idx) => (
        <div key={idx} className={`typed-line ${lines[idx].className}`}>
          {line}
        </div>
      ))}
    </div>
  );
};

const Test = () => {
  useEffect(() => {
    const chart = am4core.create("chartdiv", am4maps.MapChart);

    chart.geodata = am4geodata_worldLow;
    chart.projection = new am4maps.projections.Orthographic();
    chart.panBehavior = "rotateLongLat";
    chart.padding(20, 20, 20, 20);
    chart.zoomControl = new am4maps.ZoomControl();
    chart.deltaLongitude = 20;
    chart.deltaLatitude = -20;

    chart.adapter.add("deltaLatitude", delta =>
      am4core.math.fitToRange(delta, -90, 90)
    );

    const shadowPolygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
    shadowPolygonSeries.geodata = am4geodata_continentsLow;
    shadowPolygonSeries.useGeodata = true;
    shadowPolygonSeries.mapPolygons.template.fill = am4core.color("#000");
    shadowPolygonSeries.mapPolygons.template.fillOpacity = 0.6;

    const polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
    polygonSeries.useGeodata = true;
    polygonSeries.mapPolygons.template.tooltipText = "{name}";
    polygonSeries.mapPolygons.template.fill = am4core.color("#4da6ff");
    polygonSeries.mapPolygons.template.stroke = am4core.color("#ffffff");
    polygonSeries.mapPolygons.template.strokeWidth = 0.5;

    const hoverState = polygonSeries.mapPolygons.template.states.create("hover");
    hoverState.properties.fill = am4core.color("#000");

    const graticuleSeries = chart.series.push(new am4maps.GraticuleSeries());
    graticuleSeries.mapLines.template.stroke = am4core.color("#fff");
    graticuleSeries.mapLines.template.strokeOpacity = 0.2;

    return () => {
      chart.dispose();
    };
  }, []);

  return (
    <div>
      <NavBar />
      <div className="test-container">
     
      <div className="left-panel">
        <TypingOverlay />
      </div>
      <div className="right-panel">
        <div id="chartdiv"></div>
        <svg className="black-overlay" width="100%" height="100%">
          <defs>
            <radialGradient id="Gradient" cx="0.5" cy="0.5" r="0.5">
              <stop offset="0%" stopColor="#000" stopOpacity="0" />
              <stop offset="60%" stopColor="#000" stopOpacity="0.2" />
              <stop offset="80%" stopColor="#000" stopOpacity="0.6" />
              <stop offset="100%" stopColor="#000" stopOpacity="0.85" />
            </radialGradient>
          </defs>
          <circle cx="951.3" cy="368.7" r="664.6" fill="url(#Gradient)" />
        </svg>
      </div>
    </div>
    </div>
  );
};

export default Test;