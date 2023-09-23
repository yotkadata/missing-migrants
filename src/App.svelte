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

  $: margin = {
    top: 110,
    right: 180,
    bottom: 10,
    left: 10,
  };

  let width = 700;
  $: height = 700;

  const maxRadius = 30;
  const minRadius = 1;

  $: innerWidth = width - margin.left - margin.right;
  $: innerHeight = height - margin.top - margin.bottom;

  $: yScale = scaleBand()
    .domain(Object.keys(colorMapping))
    .range([0, innerHeight])
    .paddingOuter(0);

  // Get min date and set to Jan 1 of the year
  const minDate = min(data.map((d) => d.date));
  minDate.setMonth(0);
  minDate.setDate(1);
  minDate.setHours(0, 0, 0, 0);

  // // Get max date set to Dec 31 of the year
  const maxDate = max(data.map((d) => d.date));
  maxDate.setMonth(11);
  maxDate.setDate(31);
  minDate.setHours(0, 0, 0, 0);

  $: xScale = scaleTime().domain([minDate, maxDate]).range([0, innerWidth]);

  $: radiusScale = scaleSqrt()
    .domain(extent(data, (d) => d.value))
    .range([minRadius, maxRadius]);

  // Function to format numbers
  const formatNumber = new Intl.NumberFormat("en-US", {
    style: "decimal",
  }).format;

  // Function to format dates
  const formatDate = timeFormat("%b %Y");
</script>

<main>
  <h1>
    At least {formatNumber(totals["Total"].value)} migrants went missing since 2014
  </h1>
  <h2>
    The Missing Migrants Project of the International Organization for Migration
    (IOM) has documented {formatNumber(totals["Total"].value)} cases of people who
    died or went missing during migration. The actual number is likely much higher.
    Each circle in this graph represents an incident where at least one migrant died
    or went missing. The circle's size indicates the number of people affected. Color
    and vertical position denote the region of occurrence. Incidents are arranged
    by date from left to right.
  </h2>

  <div class="chart-container" bind:clientWidth={width}>
    <svg {width} {height}>
      <Thresholds {xScale} {formatNumber} {formatDate} />
      <g class="inner-chart" transform="translate({margin.left}, {margin.top})">
        <AxisX {xScale} height={innerHeight} />
        <Legend
          {yScale}
          {radiusScale}
          {colorMapping}
          width={innerWidth}
          {totals}
          {formatNumber}
        />
        <Chart
          {xScale}
          {yScale}
          {radiusScale}
          {colorMapping}
          bind:data
          bind:chartReady
        />
      </g>
      {#if chartReady}
        <Annotations {xScale} {yScale} {data} {totals} {formatNumber} />
      {/if}
    </svg>
  </div>
  <Source />
</main>

<style>
  main {
    background-color: #333;
    color: #f8f8f8;
    font-family: Lato, sans-serif;
    padding: 1rem;
  }
  h1 {
    font-size: 3rem;
    font-weight: 800;
    margin: 0 0 1rem 0;
  }
  h2 {
    font-size: 1.2rem;
    margin: 1rem 0;
  }
</style>
