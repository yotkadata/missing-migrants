<script>
  // Based on https://svelte.dev/repl/3e4e05c17043416da6a9ab5962572979?version=4.1.1
  import * as d3 from "d3";

  export let data;
  export let colorMapping;
  export let formatNumber;
  export let width;
  export let height;

  // Compute the layout.
  $: root = d3
    .treemap()
    .tile(d3.treemapSquarify)
    .size([width, height])
    .padding(1)
    .round(true)(
    d3
      .hierarchy(data)
      .sum((d) => d.value)
      .sort((a, b) => b.value - a.value)
  );
</script>

<svg
  {width}
  {height}
  viewBox="0 0 {width} {height}"
  style="max-width: 100%; height: auto;"
>
  {#each root.leaves() as leaf, leafIndex}
    <!-- Get nodes of current leaf -->
    {@const nodes = leaf.data.name
      .split(/(?=[A-Z][a-z])|\s+/g)
      .concat(formatNumber(leaf.value))}

    <!-- Add a cell for each leaf of the hierarchy -->
    <g transform="translate({leaf.x0},{leaf.y0})">
      <!-- Add a tooltip -->
      <title>
        {`${leaf
          .ancestors()
          .reverse()
          .map((leaf) => leaf.data.name)
          .join(".")}\n${formatNumber(leaf.value)}`}
      </title>

      <!-- Add a color rectangle -->
      <rect
        id="rect-{leafIndex}"
        fill={colorMapping[leaf.data.name]}
        fill-opacity={0.8}
        width={leaf.x1 - leaf.x0}
        height={leaf.y1 - leaf.y0}
      />

      <!-- Add a clipPath to ensure text does not overflow -->
      <clipPath id="clip-{leafIndex}">
        <use href="#rect-{leafIndex}" />
      </clipPath>

      <!-- Add multiline text. The last line shows the value and has a specific formatting. -->
      <text clip-path="url(#clip-{leafIndex})">
        {#each nodes as node, nodeIndex}
          <tspan
            x="3"
            y="{(nodeIndex === nodes.length - 1) * 0.3 +
              1.1 +
              nodeIndex * 0.9}em"
            fill-opacity={nodeIndex === nodes.length - 1 ? 0.7 : null}
          >
            {node}
          </tspan>
        {/each}
      </text>
    </g>
  {/each}
</svg>
