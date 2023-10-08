<script>
  // Component Imports
  import Annotations from "$components/Annotations.svelte";
  import AxisX from "$components/AxisX.svelte";
  import Chart from "$components/Chart.svelte";
  import Legend from "$components/Legend.svelte";
  import Source from "$components/Source.svelte";
  import Thresholds from "$components/Thresholds.svelte";
  import Tooltip from "$components/Tooltip.svelte";
  import TooltipLegend from "$components/TooltipLegend.svelte";
  import TooltipYear from "$components/TooltipYear.svelte";

  // D3 and Svelte utilities
  import { scaleBand, scaleSqrt, scaleTime } from "d3-scale";
  import { extent, min, max } from "d3-array";
  import { timeFormat } from "d3-time-format";
  import { onMount } from "svelte";

  // Data-related variables
  let data = [];
  let totals = [];
  let thresholds = [];
  let yearlyByGroup = [];
  let yearTreemap = [];

  let loading = true;
  let minDate = new Date();
  let maxDate = new Date();
  let originalMinDate, originalMaxDate;

  const dataIncidents = "data/data-migration-incidents.json";
  const dataTotals = "data/data-migration-totals.json";
  const dataThresholds = "data/data-migration-thresholds.json";
  const dataYearlyByGroup = "data/data-migration-yearly-by-group.json";
  const dataYearTreemap = "data/data-migration-treemap.json";

  onMount(async () => {
    loadData();
  });

  async function loadData() {
    try {
      // Fetch migration incidents data
      data = await fetchData(dataIncidents);
      data.forEach((d) => {
        d.date = new Date(d.date);
      });

      // Fetch migration thresholds data
      thresholds = await fetchData(dataThresholds);
      thresholds.forEach((d) => {
        d.date = new Date(d.date);
      });

      // Fetch migration totals data
      totals = await fetchData(dataTotals);

      // Fetch migration yearly data by group
      yearlyByGroup = await fetchData(dataYearlyByGroup);

      // Fetch migration treemap data for year
      yearTreemap = await fetchData(dataYearTreemap);

      loading = false;
    } catch (error) {
      console.error("Error fetching data:", error);
      loading = false;
    }
  }

  async function fetchData(url) {
    const response = await fetch(url);
    return await response.json();
  }

  // Viewport and margin settings
  let viewportWidth = window.innerWidth;
  let viewportHeight = window.innerHeight;
  let { width, height } = getChartDimensions(viewportWidth, viewportHeight);
  $: margin = {
    top: calcVw(150),
    right: calcVw(200),
    bottom: calcVw(10),
    left: calcVw(10),
  };
  $: innerWidth = width - margin.left - margin.right;
  $: innerHeight = height - margin.top - margin.bottom;

  // Chart settings
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
  const textColors = {
    "North America": "#fff",
    "Central America": "#000",
    Caribbean: "#000",
    "South America": "#000",
    Mediterranean: "#fff",
    Europe: "#fff",
    "Northern Africa": "#000",
    "Eastern Africa": "#000",
    "Western Africa": "#000",
    "Middle Africa": "#000",
    "Southern Africa": "#000",
    "South-eastern Asia": "#fff",
    "Southern Asia": "#000",
    "Western Asia": "#000",
    "Central Asia": "#000",
    "Eastern Asia": "#000",
  };
  const maxRadius = calcVw(50);
  const minRadius = calcVw(1);
  let chartReady = false;
  let showAnnotations = true;
  let circleHovered;
  let legendHovered;
  let yearHovered;

  // Scales
  $: yScale = scaleBand()
    .domain(Object.keys(colorMapping))
    .range([0, innerHeight])
    .paddingOuter(0);
  $: xScale = scaleTime().domain([minDate, maxDate]).range([0, innerWidth]);
  $: radiusScale = scaleSqrt()
    .domain(extent(data, (d) => d.value))
    .range([minRadius, maxRadius]);

  $: if (!loading && data.length) {
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
  }

  // Formatters
  const formatNumber = new Intl.NumberFormat("en-US", {
    style: "decimal",
  }).format;
  const formatPct = new Intl.NumberFormat("en-US", {
    style: "percent",
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format;
  const formatMonth = timeFormat("%b %Y");
  const formatDate = timeFormat("%e %b %Y");

  // Utility functions
  function calcVw(value) {
    return value * (viewportWidth / 2560);
  }
  function getChartDimensions(viewportWidth, viewportHeight) {
    let aspectRatio = 16 / 9;
    let notSvgHeight = calcVw(270);
    let height;
    let width = viewportWidth;
    let expectedHeight = width / aspectRatio;
    let totalHeight = expectedHeight + notSvgHeight;

    if (totalHeight > viewportHeight) {
      height = viewportHeight - notSvgHeight;
      width = height * aspectRatio;
    } else {
      height = expectedHeight;
    }
    return { width, height };
  }
</script>

<main>
  <!-- If viewport width is larger than 1000px, show interactive version -->
  {#if viewportWidth >= 1000}
    {#if !loading && data.length}
      <h1>
        At least {formatNumber(totals["Total"].value)} migrants went missing since
        2014
      </h1>
      <h2>
        The Missing Migrants Project of the International Organization for
        Migration (IOM) has documented {formatNumber(totals["Total"].value)} cases
        of people who died or went missing during migration. The actual number is
        likely much higher. Each circle in this graph represents an incident where
        at least one migrant died or went missing. The circle's size indicates the
        number of people affected. Color and vertical position denote the region
        of occurrence. Incidents are arranged by date from left to right. (Last included
        incident: {formatDate(originalMaxDate)})
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
          <Thresholds
            {thresholds}
            {xScale}
            {formatNumber}
            {formatMonth}
            {calcVw}
          />
          <g
            class="inner-chart"
            transform="translate({margin.left}, {margin.top})"
          >
            <AxisX bind:yearHovered {xScale} height={innerHeight} />
            <Legend
              {yScale}
              {radiusScale}
              {colorMapping}
              width={innerWidth}
              {totals}
              {formatNumber}
              {calcVw}
              bind:legendHovered
              bind:circleHovered
            />
            <Chart
              {xScale}
              {yScale}
              {radiusScale}
              {colorMapping}
              bind:data
              bind:chartReady
              bind:circleHovered
              {legendHovered}
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
            {colorMapping}
            {textColors}
            width={innerWidth}
            height={innerHeight}
            {margin}
            {calcVw}
            {radiusScale}
            {formatDate}
            {formatNumber}
          />
        {/if}
        {#if legendHovered}
          <TooltipLegend
            data={legendHovered}
            dataYearly={yearlyByGroup[legendHovered]}
            height={innerHeight}
            {margin}
            {totals}
            {formatNumber}
            {formatPct}
            {colorMapping}
            {yScale}
            {calcVw}
            {textColors}
          />
        {/if}
        {#if yearHovered}
          <TooltipYear
            {yearHovered}
            width={innerWidth}
            height={innerHeight}
            {calcVw}
            {xScale}
            {yearTreemap}
            {colorMapping}
            {formatNumber}
          />
        {/if}
      </div>
      <Source />
    {/if}
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
