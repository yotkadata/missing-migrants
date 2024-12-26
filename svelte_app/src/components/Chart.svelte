<script>
  export let data;
  export let xScale;
  export let yScale;
  export let radiusScale;
  export let colorMapping;
  export let chartReady;
  export let circleHovered;
  export let legendHovered;

  import { forceSimulation, forceY, forceX, forceCollide } from "d3-force";

  const simulation = forceSimulation(data);

  $: {
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
      .alphaDecay(0.05) // 0.1 with precomputed positions, 0.05 without
      .on("tick", () => {
        // Don't show animation, just show final result
        if (simulation.alpha() <= simulation.alphaMin()) {
          simulation.stop();
          chartReady = true;
        }
      })
      .restart();
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
              cx={node.x}
              cy={node.y}
              r={radiusScale(node.value)}
              fill={colorMapping[node.group]}
              stroke={circleHovered === node ? "#fff" : "transparent"}
              role="img"
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
{/if}
