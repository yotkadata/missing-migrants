<script>
  import { forceSimulation, forceY, forceX, forceCollide } from "d3-force";

  export let data;
  export let xScale;
  export let yScale;
  export let radiusScale;
  export let colorMapping;
  export let chartReady;
  export let circleHovered;
  export let legendHovered;
  export let calcVw;
  export let calcVh;

  let allHaveXAndY = data.every(
    (item) => item.hasOwnProperty("x") && item.hasOwnProperty("y")
  );

  $: {
    if (allHaveXAndY) {
      chartReady = true;
    } else {
      const simulation = forceSimulation(data);

      simulation
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
        )
        .alpha(1)
        .alphaDecay(0.4) // 0.1 with precomputed positions, 0.05 without
        .on("tick", () => {
          // Don't show animation, just show final result
          if (simulation.alpha() <= simulation.alphaMin()) {
            simulation.stop();
            chartReady = true;
          }
        })
        .restart();
    }
  }
  // Get unique values in data.group as array
  const groups = [...new Set(data.map((d) => d.group))];
</script>

{#if chartReady}
  <g class="circles">
    {#each groups as group}
      <g
        class="group-{group}"
        opacity={legendHovered ? (legendHovered === group ? 1 : 0.3) : 1}
      >
        {#each data as node}
          {#if node.group === group}
            <circle
              cx={calcVw(node.x)}
              cy={calcVh(node.y)}
              r={radiusScale(node.value)}
              fill={colorMapping[node.group]}
              stroke={circleHovered === node ? "#fff" : "transparent"}
              on:mouseover={() => {
                circleHovered = node;
              }}
              on:focus={() => {
                circleHovered = node;
              }}
            />
          {/if}
        {/each}
      </g>
    {/each}
  </g>
  <circle cx="0" cy="0" r="5" fill="red" />
  <text x="7" y="0" fill="red">0, 0</text>

  <circle cx={xScale.range()[1]} cy={yScale.range()[1]} r="5" fill="red" />
  <text x={xScale.range()[1] - 30} y={yScale.range()[1] - 10} fill="red"
    >{xScale.range()[1]}, {yScale.range()[1]}</text
  >

  <circle
    cx={xScale(new Date("2023-08-01"))}
    cy={yScale("Mediterranean")}
    r="5"
    fill="red"
  />
  <text
    x={xScale(new Date("2023-08-01")) - 30}
    y={yScale("Mediterranean") - 10}
    fill="red">{xScale(new Date("2023-08-01"))}, {yScale("Mediterranean")}</text
  >
{/if}
