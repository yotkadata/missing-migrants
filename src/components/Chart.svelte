<script>
  export let data;
  export let xScale;
  export let yScale;
  export let radiusScale;
  export let colorMapping;
  export let chartReady;
  export let circleHovered;

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
      .alphaDecay(0.05)
      .on("tick", () => {
        // Don't show animation, just show final result
        if (simulation.alpha() <= simulation.alphaMin()) {
          simulation.stop();
          chartReady = true;
        }
      })
      .restart();
  }
</script>

{#if chartReady}
  <g class="circles">
    {#each data as node}
      <circle
        cx={node.x}
        cy={node.y}
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
    {/each}
  </g>
{:else}
  <g
    class="calculating"
    transform="translate({xScale(new Date('2018-06-01'))}, {yScale(
      'Northern Africa'
    )})"
  >
    <text fill="#fff" text-anchor="middle">Calculating positions ...</text>
  </g>
{/if}
