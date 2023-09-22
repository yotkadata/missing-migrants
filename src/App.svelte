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
    Other: "rgba(0, 0, 0, 0.5)",
  };

  $: margin = {
    top: 30,
    right: 180,
    bottom: 25,
    left: 40,
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
  <h1>Almost 60,000 migrants died or went missing since 2014</h1>
  <h2>
    The <strong>Missing Migrants Project</strong> of the International Organisation
    for Migration (IOM) has documented migrants who died or went missing during migration.
  </h2>

  <div class="chart-container" bind:clientWidth={width}>
    <svg {width} {height}>
      <g class="inner-chart" transform="translate({margin.left}, {margin.top})">
        <AxisX {xScale} height={innerHeight} />
        <Legend
          {yScale}
          {radiusScale}
          {colorMapping}
          width={innerWidth}
          height={innerHeight}
        />
        <Thresholds {xScale} />
        <Chart {xScale} {yScale} {radiusScale} {colorMapping} {data} />
      </g>
    </svg>
  </div>
  <div class="source">
    <p>
      <strong>Graph:</strong> Jan Kühn,
      <a href="https://yotka.org">https://yotka.org</a> <strong>Data:</strong>
      <a href="https://missingmigrants.iom.int/">Missing Migrants Project</a>
      <strong>License:</strong>
      <a href="http://creativecommons.org/licenses/by/4.0/">CC by-sa-nd 4.0</a>
    </p>
  </div>
</main>

<style>
  main {
    background-color: #333;
    color: #f8f8f8;
    font-family: Lato, sans-serif;
    padding: 1rem;
  }
  h1 {
    font-size: 2rem;
    padding: 0 0 10px 0;
    font-weight: 800;
  }
  div.source {
    font-size: 0.8rem;
    padding-top: 1rem;
    text-align: right;
  }
  div.source a,
  div.source a:visited {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
  }
  div.source strong {
    font-weight: 800;
  }
</style>
