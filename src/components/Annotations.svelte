<script>
  export let xScale;
  export let yScale;
  export let data;
  export let totals;
  export let formatNumber;
  export let showAnnotations;
  export let calcVw;

  import { annotation, annotationCalloutElbow } from "d3-svg-annotation";
  import { select } from "d3-selection";

  const getCoords = (d, id) => {
    // From d, get element with id
    const record = d.find((obj) => obj.id == id);

    // Get x and y
    const x = record["x"];
    const y = record["y"];
    return { x, y };
  };

  const annotations = [
    {
      note: {
        title: "Deadliest incident",
        label: "18 April 2015: 1,022 dead or missing",
        wrap: calcVw(150),
        align: "right",
      },
      x: getCoords(data, "2015.MMP00108")["x"],
      y: getCoords(data, "2015.MMP00108")["y"],
      dx:
        xScale(new Date("2015-01-01")) - getCoords(data, "2015.MMP00108")["x"],
      dy:
        yScale("Western Africa") -
        getCoords(data, "2015.MMP00108")["y"] +
        calcVw(20),
    },
    {
      note: {
        title: "Deadliest region",
        label: `Most people (${formatNumber(
          totals["Mediterranean"].value
        )}) died or went missing in the Mediterranean due to numerous large incidents.`,
        wrap: calcVw(200),
        align: "right",
      },
      x: xScale(new Date("2023-12-31")) + calcVw(20),
      y: yScale("Mediterranean"),
      dx: calcVw(-60),
      dy: yScale("Middle Africa") - yScale("Mediterranean") - calcVw(20),
    },
  ].map(function (d) {
    d.color = "#fff";
    return d;
  });
  $: {
    // Before appending the annotations, remove any existing ones
    const chart = select(".inner-chart");
    chart.selectAll(".annotation-group").remove();

    if (showAnnotations) {
      const makeAnnotations = annotation()
        .type(annotationCalloutElbow)
        .annotations(annotations);

      select(".inner-chart")
        .append("g")
        .attr("class", "annotation-group")
        .call(makeAnnotations);
    }
  }
</script>

<style>
  :global(rect.annotation-note-bg) {
    fill: #333;
    fill-opacity: 0.5;
  }
  :global(.annotation-note) {
    font-size: 0.703125vw; /* 18px at 2560 */
  }
</style>
