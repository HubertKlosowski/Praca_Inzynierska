<script setup>
import * as d3 from "d3";
import {onMounted, ref} from "vue";
import _ from "lodash";

const stats = ref(JSON.parse(localStorage.getItem('stats'))['depressed'])

const createHist = (width, height) => {
  const marginTop = 20
  const marginRight = 20
  const marginBottom = 30
  const marginLeft = 40

  stats.value = _.map(stats.value, (num) => { return num * 100 })

  const bins = d3
      .bin()
      .domain([0, 100])
      .thresholds(10)
      (stats.value)

  // Declare the x (horizontal position) scale.
  const x = d3
      .scaleLinear()
      .domain([0, 100])
      .range([marginLeft, width - marginRight])

  // Declare the y (vertical position) scale.
  const y = d3.scaleLinear()
      .domain([0, d3.max(bins, (d) => d.length) + 10])
      .range([height - marginBottom, marginTop])

  // Create the SVG container.
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("style", "max-width: 100%; height: auto;")

  // Add a rect for each bin.
  svg.append("g")
      .attr("fill", "steelblue")
    .selectAll()
    .data(bins)
    .join("rect")
      .attr("x", (d) => x(d.x0) + 1)
      .attr("width", (d) => x(d.x1) - x(d.x0) - 1)
      .attr("y", (d) => y(d.length))
      .attr("height", (d) => y(0) - y(d.length))

  // Add the x-axis and label.
  svg.append("g")
      .attr("transform", `translate(0,${height - marginBottom})`)
      .attr("style", "font-size: 15px")
      .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))
      .call((g) => g.append("text")
          .attr("x", width)
          .attr("y", 1.5 * marginBottom)
          .attr("fill", "currentColor")
          .attr("text-anchor", "end")
          .attr("style", "font-size: 15px")
          .text("Kategorie depresji"))

  // Add the y-axis and label
  svg.append("g")
      .attr("transform", `translate(${marginLeft},0)`)
      .attr("style", "font-size: 15px")
      .call(d3.axisLeft(y).ticks(height / 40))
      .call((g) => g.append("text")
          .attr("x", -marginLeft)
          .attr("y", 10)
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .attr("style", "font-size: 15px")
          .text("Liczebność kategorii depresji"))

  return svg.node()
}

const createDonut = () => {

}

onMounted(() => {
  const histplot = document.querySelector('.histplot')

  histplot.appendChild(createHist(window.innerWidth / 2, window.innerHeight / 2))
})
</script>

<template>
  <div class="plot">
    <div class="donut"></div>
    <div class="histplot"></div>
  </div>
</template>

<style scoped>
.plot {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  background-color: lightgray;
  overflow-y: auto;
}
</style>