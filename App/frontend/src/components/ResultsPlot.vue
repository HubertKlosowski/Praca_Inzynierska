<script setup>
import * as d3 from "d3";
import {onMounted, ref} from "vue";
import _ from "lodash";
import FormRadioField from "@/components/FormRadioField.vue";


const stats = ref(JSON.parse(localStorage.getItem('depressed')))
const choose_plot = ref(0)


const createHist = () => {
  const marginTop = 100
  const marginRight = 50
  const marginBottom = 50
  const marginLeft = 100
  const svg = d3.select('#hist')
  const width = parseInt(svg.style('width'))
  const height = parseInt(svg.style('height'))

  const scaled = _.map(stats.value, (num) => { return num * 100 })

  const bins = d3
      .bin()
      .domain([0, 100])
      .thresholds(10)
      (scaled)

  const x = d3
      .scaleLinear()
      .domain([0, 100])
      .range([marginLeft, width - marginRight])

  const y = d3.scaleLinear()
      .domain([0, d3.max(bins, (d) => d.length) + 10])
      .range([height - marginBottom, marginTop])

  svg.append("g")
      .attr("fill", "steelblue")
    .selectAll()
    .data(bins)
    .join("rect")
      .attr("x", (d) => x(d.x0) + 1)
      .attr("width", (d) => x(d.x1) - x(d.x0) - 1)
      .attr("y", (d) => y(d.length))
      .attr("height", (d) => y(0) - y(d.length))

  svg.append("g")
      .attr("transform", `translate(0,${height - marginBottom})`)
      .attr("style", "font-size: 1.5vw")
      .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))
      .call((g) => g.append("text")
          .attr("x", width / 2 + marginRight)
          .attr("y", marginBottom)
          .attr("fill", "currentColor")
          .attr("text-anchor", "center")
          .attr("style", "font-size: 1.5vw;")
          .text("Kategorie depresji"))

  svg.append("g")
      .attr("transform", `translate(${marginLeft},0)`)
      .attr("style", "font-size: 1.5vw")
      .call(d3.axisLeft(y).ticks(height / 40))
      .call((g) => g.append("text")
          .attr("x", -(height / 2 - marginTop))
          .attr("y", -marginRight)
          .attr("fill", "currentColor")
          .attr("text-anchor", "center")
          .attr("style", "font-size: 1.5vw; transform: rotate(-90deg);")
          .text("Liczebność kategorii depresji"))
}

const createDonut = () => {

}

const createWordCloud = () => {

}

const setPlot = () => {
  if (choose_plot.value === 0) {
    createHist()
  } else if (choose_plot.value === 1) {
    createDonut()
  } else {
    createWordCloud()
  }
}

onMounted(() => {
  setPlot()
})
</script>

<template>
  <div class="plot">
    <div class="plots">
      <svg id="hist" v-if="choose_plot === 0" preserveAspectRatio="xMinYMid meet" viewBox="0 0 1000 500" width="100%" height="100%"></svg>
      <svg id="donut" v-else-if="choose_plot === 1" preserveAspectRatio="xMinYMid meet" viewBox="0 0 1000 500" width="100%" height="100%"></svg>
      <svg id="wordcloud" v-else viewBox="0 0 800 600"></svg>
    </div>
    <div class="form">
      <form @change.prevent="setPlot">

        <FormRadioField
            v-model:input_value="choose_plot"
            :title="'Wykres'"
            :options="['histogram', 'kołowy', 'wordcloud']"
            :values="[0, 1, 2]"
        ></FormRadioField>

      </form>
    </div>
  </div>
</template>

<style scoped>
.plot {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.plots {
  width: 70%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.form {
  width: 30%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
}

form {
  width: 100%;
  margin: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
}

@media (max-width: 700px) {
  .plot {
    flex-direction: column-reverse;
  }

  .plots {
    width: 100%;
    height: 80%;
  }

  .form {
    width: 100%;
    height: 20%;
  }

  svg {
    font-size: 2.5vh;
  }
}
</style>