<script>
  import { fly, fade } from "svelte/transition";
  import { timeFormat } from "d3";

  export let data;
  export let width;
  export let margin;
  export let radiusScale;
  export let formatNumber;
  export let colorMapping;

  let tooltipWidth;

  let xOffset = 5;
  let yOffset = -20;

  $: xPosition =
    data.x + tooltipWidth + margin.left + radiusScale(data.value) > width
      ? data.x - tooltipWidth
      : data.x + margin.left + radiusScale(data.value);

  $: yPosition = data.y + margin.top - radiusScale(data.value) + yOffset;

  // Function to format dates
  const formatDate = timeFormat("%e %b %Y");

  // Build links from source and url
  let sources;
  let urls;
  let links = [];

  $: {
    if (data.url && data.source) {
      sources = data.source.split(",");
      urls = data.url.split(" ");

      links.length = 0; // Reset links
      for (let i = 0; i < Math.min(sources.length, urls.length); i++) {
        links.push({ text: sources[i].trim(), href: urls[i].trim() });
      }
    }
  }

  // Extract coordinates to build link to Openstreetmap
  let lat, lon;

  $: if (data.coords) {
    [lat, lon] = data.coords
      .split(",")
      .map((coord) => parseFloat(coord.trim()));
  }
</script>

<div
  class="tooltip"
  style="position: absolute; top: {yPosition}px; left: {xPosition}px;"
  in:fly={{ y: 10, duration: 200, delay: 200 }}
  out:fade={{ duration: 600 }}
  bind:clientWidth={tooltipWidth}
>
  <div class="text">
    <p class="region" style="background-color: {colorMapping[data.group]}">
      {data.group}
    </p>
    <p class="number-missing">
      {formatNumber(data.value)}
    </p>
    <p class="text-missing">Dead or missing</p>
    <p class="date">
      <strong>Date:</strong>
      {formatDate(data.date)}
    </p>
    <p class="origin"><strong>Origin:</strong> {data.origin}</p>
    <p class="route"><strong>Migration route:</strong> {data.route}</p>
    {#if lat && lon}
      <p class="location">
        <strong>Location:</strong>
        <a
          href={`https://www.openstreetmap.org/?mlat=${lat}&mlon=${lon}#map=6/${lat}/${lon}&layers=H`}
          title="View on Openstreetmap"
          target="_blank"
          rel="noreferrer">{data.location}</a
        >
      </p>
    {:else}
      <p class="location"><strong>Location:</strong> {data.location}</p>
    {/if}
    <p class="source">
      <strong>Source:</strong>
      {#each links as link}
        <a href={link.href} title={link.text} target="_blank" rel="noreferrer"
          >{link.text}</a
        >{#if link !== links[links.length - 1]}, {/if}
      {/each}
    </p>
    <p class="source-quality">
      <strong>Source quality:</strong>
      {data.quality}
    </p>
    <p class="id">
      <strong>ID:</strong>
      {data.id}
    </p>
  </div>
</div>

<style>
  .tooltip {
    background-color: #fff;
    box-shadow: 2px 3px 8px rgba(0, 0, 0, 0.15);
    padding: 0.3125vw 0.234375vw; /* 8px/6px at 2560 */
    border-radius: 5%;
    align-items: center;
    transition: top 300ms ease, left 300ms ease;
    z-index: 10;
    max-width: 11.71875vw; /* 300px at 2560 */
    word-wrap: break-word;
  }
  .text {
    color: #000;
  }
  .text p {
    font-size: 0.78125vw; /* 20px at 2560 */
    margin: 0.3125vw 0; /* 8px at 2560 */
  }
  .text p.region {
    color: #fff;
    font-weight: 800;
    padding: 0.15625vw; /* 4px at 2560 */
    text-transform: uppercase;
  }
  .text strong {
    font-weight: 600;
  }
  .text p.number-missing {
    font-size: 1.25vw; /* 32px at 2560 */
    font-weight: 800;
    margin-top: 0.625vw; /* 16px at 2560 */
  }
  .text p.text-missing {
    margin-bottom: 0.625vw; /* 16px at 2560 */
  }
  .text a,
  .text a:visited {
    color: #000;
  }
</style>
