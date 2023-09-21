<script>
  import data from "$data/data-migration-incidents.json";
  //import data from "$data/data-migration-individual.json";

  // Convert date strings to Date objects
  data.forEach((d) => {
    d.date = new Date(d.date);
  });

  import AxisX from "$components/AxisX.svelte";
  import Chart from "$components/Chart.svelte";
  import Legend from "$components/Legend.svelte";
  import Thresholds from "$components/Thresholds.svelte";

  import { scaleBand, scaleSqrt, scaleTime } from "d3-scale";
  import { extent, min, max } from "d3-array";

  const colorMapping = {
    "North America": "hsla(181, 88%, 80%, 1)",
    "Central America": "hsla(181, 88%, 60%, 1)",
    Caribbean: "hsla(181, 88%, 40%, 1)",
    "South America": "hsla(181, 88%, 31%, 1)",
    Mediterranean: "hsla(5, 81%, 50%, 1)",
    Europe: "hsla(5, 81%, 38%, 1)",
    "South-eastern Asia": "hsla(30, 98%, 40%, 1)",
    "Southern Asia": "hsla(30, 98%, 50%, 1)",
    "Western Asia": "hsla(30, 98%, 60%, 1)",
    "Central Asia": "hsla(30, 98%, 70%, 1)",
    "Eastern Asia": "hsla(30, 98%, 80%, 1)",
    "Northern Africa": "hsla(39, 100%, 47%, 1)",
    "Eastern Africa": "hsla(39, 100%, 55%, 1)",
    "Western Africa": "hsla(39, 100%, 60%, 1)",
    "Middle Africa": "hsla(39, 100%, 70%, 1)",
    "Southern Africa": "hsla(39, 100%, 80%, 1)",
    Other: "rgba(0, 0, 0, 0.5)",
  };

  $: margin = {
    top: 0,
    right: 100,
    bottom: 25,
    left: 25,
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
    .paddingOuter(2);

  // Get min date and set to Jan 1 of the year
  const minDate = min(data.map((d) => d.date));
  minDate.setMonth(0);
  minDate.setDate(1);

  // // Get max date set to Dec 31 of the year
  const maxDate = max(data.map((d) => d.date));
  maxDate.setMonth(11);
  maxDate.setDate(31);

  $: xScale = scaleTime().domain([minDate, maxDate]).range([0, innerWidth]);

  $: radiusScale = scaleSqrt()
    .domain(extent(data, (d) => d.value))
    .range([minRadius, maxRadius]);
</script>

<main>
  <h1>Missing Migrants 2014-2023</h1>

  <div class="chart-container" bind:clientWidth={width}>
    <svg {width} {height}>
      <AxisX {xScale} height={innerHeight} />
      <Legend {yScale} {colorMapping} />
      <Thresholds {xScale} />
      <Chart {xScale} {yScale} {radiusScale} {colorMapping} {data} />
    </svg>
  </div>
</main>

<style>
  main {
    background-color: #333;
    color: #f8f8f8;
    font-family: Lato, sans-serif;
  }
  h1 {
    font-size: 2rem;
    padding: 10px 0 20px 0;
    font-weight: 800;
    text-align: center;
  }
  :global(.tick text) {
    font-size: 0.8rem;
    fill: hsla(212, 10%, 53%, 1);
    font-weight: 400;
  }
  :global(.axis-title) {
    font-size: 12px;
    font-weight: 400;
    fill: hsla(212, 10%, 53%, 1);
    user-select: none; /* Prevents text from being selected */
  }
</style>
