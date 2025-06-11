import React, { useLayoutEffect, useRef } from 'react';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_worldLow from "@amcharts/amcharts4-geodata/worldLow";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";
import "../../Styles/Test2.css";

const Test2 = () => {
  const chartRef = useRef(null);

  useLayoutEffect(() => {
    // Apply theme
    am4core.useTheme(am4themes_animated);

    // Create chart instance
    let chart = am4core.create(chartRef.current, am4maps.MapChart);

    chart.geodata = am4geodata_worldLow;
    chart.projection = new am4maps.projections.Orthographic();
    chart.panBehavior = "rotateLongLat";
    chart.deltaLatitude = -20;
    chart.padding(20, 20, 20, 20);

    // Create polygon series
    let polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
    polygonSeries.useGeodata = true;

    // Configure map appearance
    let polygonTemplate = polygonSeries.mapPolygons.template;
    polygonTemplate.tooltipText = "{name}";
    polygonTemplate.fill = am4core.color("#FF6633");
    polygonTemplate.stroke = am4core.color("#000033");
    polygonTemplate.strokeWidth = 0.5;
    polygonTemplate.cursorOverStyle = am4core.MouseCursorStyle.pointer;
    polygonTemplate.url = "https://www.datadrum.com/main.php?package={id}";
    polygonTemplate.urlTarget = "_blank";

    // Graticule lines
    let graticuleSeries = chart.series.push(new am4maps.GraticuleSeries());
    graticuleSeries.mapLines.template.line.stroke = am4core.color("#ffffff");
    graticuleSeries.mapLines.template.line.strokeOpacity = 0.08;
    graticuleSeries.fitExtent = false;

    chart.backgroundSeries.mapPolygons.template.polygon.fillOpacity = 0.1;
    chart.backgroundSeries.mapPolygons.template.polygon.fill = am4core.color("#ffffff");

    // Hover state
    let hs = polygonTemplate.states.create("hover");
    hs.properties.fill = chart.colors.getIndex(0).brighten(-0.5);

    // Animate rotation
    let animation;
    setTimeout(() => {
      animation = chart.animate({ property: "deltaLongitude", to: 100000 }, 20000000);
    }, 3000);

    chart.seriesContainer.events.on("down", () => {
      // animation.stop(); // Uncomment if you want to stop on drag
    });

    // Cleanup
    return () => {
      chart.dispose();
    };
  }, []);

  return (
    <div className="test-container">
      <div id="chartdiv" ref={chartRef}></div>
    </div>
  );
};

export default Test2;
