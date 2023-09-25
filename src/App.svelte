<script>
  import dataRaw from "$data/data-migration-incidents.json";
  //import data from "$data/data-migration-individual.json";
  import totals from "$data/data-migration-totals.json";

  // Convert date strings to Date objects
  dataRaw.forEach((d) => {
    d.date = new Date(d.date);
  });
  let data = dataRaw;

  import Annotations from "$components/Annotations.svelte";
  import AxisX from "$components/AxisX.svelte";
  import Chart from "$components/Chart.svelte";
  import Legend from "$components/Legend.svelte";
  import Source from "$components/Source.svelte";
  import Thresholds from "$components/Thresholds.svelte";
  import Tooltip from "$components/Tooltip.svelte";

  import { scaleBand, scaleSqrt, scaleTime } from "d3-scale";
  import { extent, min, max } from "d3-array";
  import { timeFormat } from "d3";

  const colorMapping = {
    "North America": "hsla(181, 88%, 35%, 1)",
    "Central America": "hsla(181, 88%, 50%, 1)",
    Caribbean: "hsla(181, 88%, 65%, 1)",
    "South America": "hsla(181, 88%, 80%, 1)",
    Mediterranean: "hsla(5, 81%, 50%, 1)",
    Europe: "hsla(5, 81%, 38%, 1)",
    "Northern Africa": "hsla(39, 100%, 47%, 1)",
    "Eastern Africa": "hsla(39, 100%, 57%, 1)",
    "Western Africa": "hsla(39, 100%, 67%, 1)",
    "Middle Africa": "hsla(39, 100%, 77%, 1)",
    "Southern Africa": "hsla(39, 100%, 87%, 1)",
    "South-eastern Asia": "hsla(268, 17%, 50%, 1)",
    "Southern Asia": "hsla(268, 17%, 60%, 1)",
    "Western Asia": "hsla(268, 17%, 70%, 1)",
    "Central Asia": "hsla(268, 17%, 80%, 1)",
    "Eastern Asia": "hsla(268, 17%, 90%, 1)",
  };

  let chartReady = false;

  // Function to calculate values based on viewport width
  const calcVw = (value) => {
    return value * (viewportWidth / 2560);
  };

  $: margin = {
    top: calcVw(150),
    right: calcVw(200),
    bottom: calcVw(10),
    left: calcVw(10),
  };

  let viewportWidth = window.innerWidth;
  let viewportHeight = window.innerHeight;
  let aspectRatio = 16 / 9;
  let notSvgHeight = calcVw(270); /* 270 at 2560 */
  let height;

  // Set width to viewport width
  let width = viewportWidth;

  // Calculate the expected height based on the width and aspect ratio
  let expectedHeight = width / aspectRatio;

  // Calculate total height including elements outside SVG
  let totalHeight = expectedHeight + notSvgHeight;

  // Check if the total height exceeds the viewport height
  if (totalHeight > viewportHeight) {
    // Adjust width and height based on the viewport height and aspect ratio
    height = viewportHeight - notSvgHeight;
    width = height * aspectRatio;
  } else {
    height = expectedHeight;
  }

  const maxRadius = calcVw(50);
  const minRadius = calcVw(1);

  $: innerWidth = width - margin.left - margin.right;
  $: innerHeight = height - margin.top - margin.bottom;

  $: yScale = scaleBand()
    .domain(Object.keys(colorMapping))
    .range([0, innerHeight])
    .paddingOuter(0);

  // Get min date and set to Jan 1 of the year for xScale domain
  const originalMinDate = min(data.map((d) => d.date));
  // Create a copy of the min date
  const minDate = new Date(originalMinDate);
  // Set the copy to Jan 1 of the year
  minDate.setMonth(0);
  minDate.setDate(1);
  minDate.setHours(0, 0, 0, 0);

  // Get max date set to Dec 31 of the year for xScale domain
  const originalMaxDate = max(data.map((d) => d.date));
  // Create a copy of the max date
  const maxDate = new Date(originalMaxDate);
  // Set the copy to Dec 31 of the year
  maxDate.setMonth(11);
  maxDate.setDate(31);
  maxDate.setHours(0, 0, 0, 0);

  $: xScale = scaleTime().domain([minDate, maxDate]).range([0, innerWidth]);

  $: radiusScale = scaleSqrt()
    .domain(extent(data, (d) => d.value))
    .range([minRadius, maxRadius]);

  // Function to format numbers
  const formatNumber = new Intl.NumberFormat("en-US", {
    style: "decimal",
  }).format;

  // Function to format dates
  const formatMonth = timeFormat("%b %Y");
  const formatDate = timeFormat("%e %b %Y");

  let showAnnotations = true;
  let circleHovered;
</script>

<main>
  <!-- If viewport width is larger than 1000px, show interactive version -->
  {#if viewportWidth >= 1000}
    <h1>
      At least {formatNumber(totals["Total"].value)} migrants went missing since
      2014
    </h1>
    <h2>
      The Missing Migrants Project of the International Organization for
      Migration (IOM) has documented {formatNumber(totals["Total"].value)} cases
      of people who died or went missing during migration (as of {formatDate(
        originalMaxDate
      )}). The actual number is likely much higher. Each circle in this graph
      represents an incident where at least one migrant died or went missing.
      The circle's size indicates the number of people affected. Color and
      vertical position denote the region of occurrence. Incidents are arranged
      by date from left to right.
    </h2>

    <div
      class="chart-container"
      bind:clientWidth={width}
      on:mouseover={() => {
        showAnnotations = false;
      }}
      on:focus={() => {
        showAnnotations = false;
      }}
      on:mouseleave={() => {
        showAnnotations = true;
        circleHovered = null;
      }}
    >
      <svg {width} {height}>
        <Thresholds {xScale} {formatNumber} {formatMonth} {calcVw} />
        <g
          class="inner-chart"
          transform="translate({margin.left}, {margin.top})"
        >
          <AxisX {xScale} height={innerHeight} />
          <Legend
            {yScale}
            {radiusScale}
            {colorMapping}
            width={innerWidth}
            {totals}
            {formatNumber}
            {calcVw}
          />
          <Chart
            {xScale}
            {yScale}
            {radiusScale}
            {colorMapping}
            bind:data
            bind:chartReady
            bind:circleHovered
          />
        </g>
        {#if chartReady}
          <Annotations
            {xScale}
            {yScale}
            {data}
            {totals}
            {formatNumber}
            {showAnnotations}
            {calcVw}
          />
        {/if}
      </svg>
      {#if circleHovered}
        <Tooltip
          data={circleHovered}
          width={innerWidth}
          {margin}
          {radiusScale}
          {formatNumber}
          {colorMapping}
        />
      {/if}
    </div>
    <Source />
  {:else}
    <!-- If viewport width is smaller than 1000px, show static version -->
    <div class="static">
      <img
        src="static-graph-missing-migrants.png"
        alt="Missing Migrants Graph"
        class="responsive-image"
      />
      <p>
        The <strong>interactive version</strong> of the graph is currently only available
        on large screens. Please visit this page on a desktop computer or a tablet
        in landscape mode.
      </p>
    </div>
  {/if}
</main>

<style>
  main {
    background-color: #333;
    color: #f8f8f8;
    font-family: Lato, sans-serif;
    margin: 0 auto;
    padding: 1.25vw 0.625vw 0.625vw 1.25vw;
  }
  h1 {
    font-size: 2.5vw; /* 64px at 2560 */
    font-weight: 800;
    margin: 0 0 0.625vw 0; /* 16px at 2560 */
  }
  h2 {
    font-size: 1.25vw; /* 32px at 2560 */
    margin: 0.625vw 0; /* 16px at 2560 */
  }
  .responsive-image {
    width: 100%; /* Make the image expand to the width of its container */
    height: auto; /* Maintain the image's aspect ratio */
    display: block; /* Remove any margins or spacing */
    max-width: 100%; /* Ensure it doesn't scale beyond its original size */
  }
  .static p {
    margin: 0.625vw 0;
  }
</style>
