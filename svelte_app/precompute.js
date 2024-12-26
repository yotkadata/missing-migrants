import { scaleBand, scaleSqrt, scaleTime } from "d3-scale";
import { extent, min, max } from "d3-array";
import { forceSimulation, forceY, forceX, forceCollide } from "d3-force";
import fs from "fs";

let minDate = new Date();
let maxDate = new Date();
let originalMinDate, originalMaxDate;

import data from "./public/data/data-migration-incidents.json" assert { type: "json" };

data.forEach((d) => {
  d.date = new Date(d.date);
});

function getChartDimensions(viewportWidth, viewportHeight) {
  let aspectRatio = 16 / 9;
  let notSvgHeight = 270;
  let height;
  let width = viewportWidth;
  let expectedHeight = width / aspectRatio;
  console.log("expectedHeight", expectedHeight);
  let totalHeight = expectedHeight + notSvgHeight;
  console.log("totalHeight", totalHeight);

  if (totalHeight > viewportHeight) {
    height = viewportHeight - notSvgHeight;
    //width = height * aspectRatio;
  } else {
    height = expectedHeight;
  }
  return { width, height };
}

// Viewport and margin settings
const { width, height } = getChartDimensions(2560, 1440);
const margin = {
  top: 150,
  right: 200,
  bottom: 10,
  left: 10,
};
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;

const groups = [
  "North America",
  "Central America",
  "Caribbean",
  "South America",
  "Mediterranean",
  "Europe",
  "Northern Africa",
  "Eastern Africa",
  "Western Africa",
  "Middle Africa",
  "Southern Africa",
  "South-eastern Asia",
  "Southern Asia",
  "Western Asia",
  "Central Asia",
  "Eastern Asia",
];

const maxRadius = 50;
const minRadius = 1;

if (data.length) {
  originalMinDate = min(data.map((d) => d.date));
  minDate = new Date(originalMinDate);
  minDate.setMonth(0);
  minDate.setDate(1);
  minDate.setHours(0, 0, 0, 0);

  originalMaxDate = max(data.map((d) => d.date));
  maxDate = new Date(originalMaxDate);
  maxDate.setMonth(11);
  maxDate.setDate(31);
  maxDate.setHours(0, 0, 0, 0);

  console.log("minDate", minDate);
  console.log("maxDate", maxDate);
} else {
  console.log("No data");
}

// Scales
const yScale = scaleBand()
  .domain(groups)
  .range([0, innerHeight])
  .paddingOuter(0);
const xScale = scaleTime().domain([minDate, maxDate]).range([0, innerWidth]);
const radiusScale = scaleSqrt()
  .domain(extent(data, (d) => d.value))
  .range([minRadius, maxRadius]);

console.log("width", width);
console.log("height", height);
console.log("innerWidth", innerWidth);
console.log("innerHeight", innerHeight);
console.log("xScale", xScale.range());
console.log("yScale", yScale.range());

const simulation = forceSimulation(data)
  .force(
    "x",
    forceX()
      .x((d) => xScale(d.date))
      .strength(1)
  )
  .force(
    "y",
    forceY()
      .y((d) => yScale(d.group))
      .strength(0.8)
  )
  .force(
    "collide",
    forceCollide()
      .radius((d) => radiusScale(d.value) + 1)
      .strength(1)
      .iterations(5)
  )
  .alphaDecay(0.02) // 0.1 with precomputed positions, 0.05 without
  .restart();

// Manually tick the simulation to precompute final positions
for (let i = 0; i < 1000; i++) {
  console.log(
    "Running tick " +
      i +
      " (alpha: " +
      simulation.alpha() +
      ", stops at " +
      simulation.alphaMin() +
      ")"
  );
  simulation.tick();

  if (simulation.alpha() <= simulation.alphaMin()) {
    break;
  }
}

// Save data to json file
fs.writeFileSync(
  "./public/data/data-migration-incidents-precomputed.json",
  JSON.stringify(data, null, 4)
);
