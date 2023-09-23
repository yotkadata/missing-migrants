<script>
  export let xScale;
  export let yScale;
  export let data;

  import { annotation, annotationCalloutElbow } from "d3-svg-annotation";
  import { select } from "d3-selection";
  import { onMount } from "svelte";

  const getCoords = (d, id) => {
    // From d, get element with id
    const record = d.find((obj) => obj.id == id);

    // Get x and y
    const x = record["x"];
    const y = record["y"];
    return { x, y };
  };

  onMount(() => {
    const annotations = [
      {
        note: {
          title: "Deadliest incident",
          label: "18 April 2015: 1,022 dead or missing",
          wrap: 150,
          align: "left",
        },
        x: getCoords(data, "2015.MMP00108")["x"],
        y: getCoords(data, "2015.MMP00108")["y"],
        dx: -150,
        dy: 110,
      },
      {
        note: {
          title: "Deadliest region",
          label:
            "Most people (28,073) died or went missing in the Mediterranean due to numerous large incidents.",
          wrap: 200,
          align: "left",
        },
        x: xScale(new Date("2023-12-31")) + 20,
        y: yScale("Mediterranean"),
        dx: -220,
        dy: 150,
      },
    ].map(function (d) {
      d.color = "#fff";
      return d;
    });

    const makeAnnotations = annotation()
      .type(annotationCalloutElbow)
      .annotations(annotations);

    select(".inner-chart")
      .append("g")
      .attr("class", "annotation-group")
      .call(makeAnnotations);
  });
</script>

<style>
  :global(rect.annotation-note-bg) {
    fill: #333;
    fill-opacity: 0.5;
  }
</style>
