//https://observablehq.com/d/863ed7e82c329eca
// https://observablehq.com/@saikatmondal?tab=recents

chart = {
  // Specify the chart’s dimensions.
  const width = 800;
  const height = width;
  const cx = width * 0.5; // adjust as needed to fit
  const cy = height * 0.5; // adjust as needed to fit
  const radius = Math.min(width, height) / 2 - 320;

  // Color scale for different categories.
  const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

  // Create a radial cluster layout. The layout’s first dimension (x)
  // is the angle, while the second (y) is the radius.
  const tree = d3.cluster()
      .size([2 * Math.PI, radius])
      .separation((a, b) => (a.parent == b.parent ? 1 : 2) / a.depth);

  // Sort the tree and apply the layout.
  const root = tree(d3.hierarchy(rq1_data_v2)
      .sort((a, b) => d3.ascending(a.data.name, b.data.name)));

  // Creates the SVG container.
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-cx, -cy, width, height])
      .attr("style", "width: 100%; height: auto; font: 10px sans-serif;");

  // Append links (with percentages and colors).
  svg.append("g")
      .attr("fill", "none")
      .attr("stroke-opacity", 0.8)
      .attr("stroke-width", 1.5)
    .selectAll("path")
    .data(root.links())
    .join("path")
      .attr("d", d3.linkRadial()
          .angle(d => d.x)
          .radius(d => d.y))
      .attr("stroke", d => colorScale(d.source.data.id)) // Color based on category id
      // .attr("data-percent", d => `${d.target.data.percent}%`) // Add percentage to the link
      .each(function(d) {
        // Get the midpoint of the path to place the percentage
        const length = this.getTotalLength();
        const midPoint = this.getPointAtLength(length / 2);
        
        // Append percentage text on the path
        svg.append("text")
          .attr("x", midPoint.x)
          .attr("y", midPoint.y)
          .attr("dy", "-0.5em")
          .attr("fill", "#333")
          .style("font-size", "10px")
          // .text(`${d.target.data.percent}%`);
      });

  // Append nodes.
  svg.append("g")
    .selectAll("circle")
    .data(root.descendants())
    .join("circle")
      .attr("transform", d => `rotate(${d.x * 180 / Math.PI - 90}) translate(${d.y},0)`)
      .attr("fill", d => d.children ? "#555" : "#999")
      .attr("r", 2.5);

  // Append labels.
svg.append("g")
  .attr("stroke-linejoin", "round")
  .attr("stroke-width", 3)
  .selectAll("text")
  .data(root.descendants()) // Select all nodes
  .join("text")
    .attr("transform", d => `
      rotate(${d.x * 180 / Math.PI - 90})
      translate(${d.y},0)
      rotate(${d.x >= Math.PI ? 180 : 0})
    `)
    .attr("dy", "0.31em")
    .attr("x", d => d.x < Math.PI ? 6 : -6)
    .attr("text-anchor", d => d.x < Math.PI ? "start" : "end")
    .attr("paint-order", "stroke")
    .attr("stroke", "white")
    .attr("fill", "currentColor")
    .text(d => d.children ? d.data.name : `${d.data.name}`);
  
  return svg.node();
}
