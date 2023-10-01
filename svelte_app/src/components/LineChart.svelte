<script>
  import { scaleBand, scaleLinear } from "d3-scale";
  import { line } from "d3-shape";

  // Receive plot data as prop.
  export let data;
  export let width;
  width = 300;

  let height = parseInt((width / 16) * 9);

  // Extract years and values
  const years = Object.keys(data);
  const values = Object.values(data).map((value) => parseInt(value));

  //let chartData = years.map((year, index) => ({ year, value: values[index] }));

  // Setting up xScale
  const xScale = scaleBand().domain(years).range([0, width]);

  // Setting up yScale
  const yScale = scaleLinear().domain(+values).range([height, 0]);

  const linePath = line()
    .x(xScale(years) + xScale.bandwidth() / 2) // Center the point in the band
    .y(yScale(+values));
  console.log("data", data);
  console.log("width", width);
  console.log("height", height);
</script>

<svg {width} {height}>
  <!-- X-Axis -->
  <g class="axis x" transform="translate(0, {height})">
    <line stroke="currentColor" x1={-6} x2={width} />

    {#each years as year}
      <!-- X-Axis Ticks -->
      <line
        stroke="currentColor"
        x1={xScale(year)}
        x2={xScale(year)}
        y1={0}
        y2={6}
      />

      <!-- X-Axis Tick Labels -->
      <text fill="currentColor" text-anchor="middle" x={xScale(year)} y={22}>
        {year}
      </text>
    {/each}
  </g>

  <!-- Y-Axis and Grid Lines -->
  <g transform="translate(0,0)">
    {#each yScale.ticks() as tick}
      {#if tick !== 0}
        <!-- 
            Grid Lines. 
            Note: First line is skipped since the x-axis is already present at 0. 
          -->
        <line
          stroke="currentColor"
          stroke-opacity="0.1"
          x1={0}
          x2={width}
          y1={yScale(tick)}
          y2={yScale(tick)}
        />

        <!-- 
            Y-Axis Ticks. 
            Note: First tick is skipped since the x-axis already acts as a tick. 
          -->
        <line
          stroke="currentColor"
          x1={0}
          x2={-6}
          y1={yScale(tick)}
          y2={yScale(tick)}
        />
      {/if}

      <!-- Y-Axis Tick Labels -->
      <text
        fill="currentColor"
        text-anchor="end"
        dominant-baseline="middle"
        x={-9}
        y={yScale(tick)}
      >
        {tick}
      </text>
    {/each}

    <!-- Y-Axis Label -->
    <text fill="currentColor" text-anchor="start" x={0} y={15}>
      ↑ Daily close ($)
    </text>
  </g>

  <path fill="none" stroke="steelblue" stroke-width="1.5" d={linePath(data)} />
</svg>
