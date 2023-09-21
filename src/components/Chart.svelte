<script>
  export let data;
  export let xScale;
  export let yScale;
  export let radiusScale;
  export let colorMapping;

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
      .alphaDecay(0.06);
  }

  let nodes = [];

  simulation.on("tick", () => {
    nodes = simulation.nodes();
  });
</script>

<g class="circles">
  {#each nodes as node}
    <circle
      cx={node.x}
      cy={node.y}
      r={radiusScale(node.value)}
      fill={colorMapping[node.group]}
    />
  {/each}
</g>
