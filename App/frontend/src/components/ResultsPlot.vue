<script setup>
import * as d3 from "d3";
import {onMounted, ref} from "vue";
import _ from "lodash";
import FormRadioField from "@/components/FormRadioField.vue";
import {removeStopwords} from "stopword/dist/stopword.esm.mjs";
import cloud from "d3-cloud";


const stats = ref(JSON.parse(localStorage.getItem('depressed')))
const text = ref(JSON.parse(localStorage.getItem('text')))
const choose_plot = ref(0)


const createHist = () => {
  const marginTop = 100
  const marginRight = 50
  const marginBottom = 50
  const marginLeft = 100
  const width = 600
  const height = 600
  const svg = d3.select('#hist').attr('viewBox', [0, 0, width, height])
  const scaled = _.map(stats.value, (num) => { return num * 100 })

  const bins = d3.bin()
      .domain([0, 100])
      .thresholds(10)
      (scaled)

  const x = d3.scaleLinear()
      .domain([0, 100])
      .range([marginLeft, width - marginRight])

  const y = d3.scaleLinear()
      .domain([0, d3.max(bins, (d) => d.length) + 10])
      .range([height - marginBottom, marginTop])

  svg.append('g')
      .attr('fill', 'black')
    .selectAll()
    .data(bins)
    .join('rect')
      .attr('x', (d) => x(d.x0) + 1)
      .attr('width', (d) => x(d.x1) - x(d.x0) - 1)
      .attr('height', 0)
      .attr('y', (d) => y(d.length))

  svg.append('g')
      .attr('transform', `translate(0,${height - marginBottom})`)
      .attr('font-size', 12)
      .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))
      .call((g) => g.append('text')
        .attr('x', width / 2 + marginRight)
        .attr('y', marginBottom / 1.5)
        .attr('fill', 'currentColor')
        .attr('text-anchor', 'center')
        .attr('font-size', 12)
        .text('Przedziały depresji (%)'))

  svg.append('g')
      .attr('transform', `translate(${marginLeft},0)`)
      .attr('font-size', 12)
      .call(d3.axisLeft(y).ticks(height / 40))
      .call((g) => g.append('text')
        .attr('x', -(height / 2 - marginTop))
        .attr('y', -marginRight / 1.5)
        .attr('fill', 'currentColor')
        .attr('text-anchor', 'center')
        .attr('font-size', 12)
        .attr('style', 'transform: rotate(-90deg);')
        .text('Liczebność w przedziale depresji'))

  svg.selectAll('rect')
      .transition()
      .duration(1500)
      .ease(d3.easeBounceOut)
      .attr('height', (d) => y(0) - y(d.length))
      .delay((_, i) => i * 100)
}

const createDonut = () => {
  const avg_depressed = _.round(_.mean(stats.value) * 100, 2)
  const data = [
    { 'name': 'depresja', 'value': avg_depressed },
    { 'name': 'brak depresji', 'value': _.round(100 - avg_depressed, 2) }
  ]

  const width = 300
  const height = 300
  const radius = Math.min(width, height) / 2
  const svg = d3.select('#donut')
      .attr('viewBox', [-width / 2, -height / 2, width, height])

  const inner_arc = d3.arc()
      .innerRadius(radius * 0.25)
      .outerRadius(radius * 0.7)

  const outer_arc = d3.arc()
      .innerRadius(radius * 0.85)
      .outerRadius(radius * 0.85)

  const pie = d3.pie()
      .padAngle(1 / radius)
      .sort(null)
      .value((d) => d.value)

  const entries = pie(data)

  const color = d3.scaleOrdinal(['black', 'white'])

  svg.append('g')
      .selectAll()
      .data(entries)
      .join('path')
      .attr('fill', (d) => color(d.data))
      .attr('stroke', 'black')
      .attr('stroke-width', 1)
      .attr('d', inner_arc)
      .append('title')
      .text((d) => `${d.data}: ${d.data['value']}`)

  svg.append('g')
      .attr('font-size', 12)
      .attr('text-anchor', 'middle')
      .selectAll()
      .data(entries)
      .join('text')
      .attr('transform', (d) => `translate(${outer_arc.centroid(d)})`)
      .call(text => text.append('tspan')
          .attr('y', '-0.4em')
          .attr('font-weight', 'bold')
          .text((d) => d.data['name']))
      .call(text => text.append('tspan')
          .attr('x', 0)
          .attr('y', '0.7em')
          .attr('fill-opacity', 0.7)
          .text((d) => d.data['value'] + '%'))

  svg.selectAll('path')
      .transition()
      .duration(1500)
      .ease(d3.easeBounceOut)
      .attrTween('d', (d) => {
        const i = d3.interpolate({ startAngle: 0, endAngle: 0 }, d)
        return function (t) {
          return inner_arc(i(t))
        }
      })
}

const createWordCloud = () => {
  let words = _.split(_.join(text.value, ' '), ' ')

  words = removeStopwords(words)
  for (let i = 0; i < words.length; i++) {
    words[i] = words[i].split('').filter((char) => { return /[a-zA-Z0-9]/.test(char) }).join('')
  }
  words = _.filter(words, (value) => value.length !== 0)
  words = _.map(words, (word) => word.toLowerCase())

  let unique = _.countBy(words)
  unique = _.pickBy(unique, (_, key) => (key.length < 50) && (key.length > 3))
  unique = _.map(unique, (value, key) => [key, value])
  const min = _.minBy(unique, (row) => row[1]), max = _.maxBy(unique, (row) => row[1])
  const max_font = 50
  const min_font = 10
  for (let i = 0; i < unique.length; i++) {
    const word = unique[i].at(0)
    const size = (unique[i].at(1) - min[1]) / (max[1] - min[1]) * (max_font - min_font) + min_font
    unique[i] = {'text': word, 'size': size}
  }

  const width = 400
  const height = 400
  const svg = d3.select('#wordcloud')
      .attr('viewBox', [0, 0, width, height])

  const layout = cloud()
      .size([width, height])
      .words(unique)
      .rotate(function() { return ~~(Math.random() * 2) * 45 })
      .font('Rubik')
      .fontSize((d) => d.size)
      .on('end', draw)

  layout.start()

  svg.selectAll('text')
      .transition()
      .ease(d3.easeLinear)
      .style('opacity', 1)
      .delay((_, i) => i * 20)

  function draw(words) {
    svg.append('g')
        .attr('transform', 'translate(' + layout.size()[0] / 2 + ',' + layout.size()[1] / 2 + ')')
      .selectAll()
        .data(words)
        .join('text')
        .style('font-size', (d) => d.size)
        .style('font-family', 'Rubik')
        .style('opacity', 0)
        .attr('text-anchor', 'middle')
        .attr('transform', (d) => 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')')
        .text((d) => d.text)
  }
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
      <h4 v-if="choose_plot === 0">Liczba przypadków depresji w poszczególnych przedziałach</h4>
      <h4 v-else-if="choose_plot === 1">Średnia wartość depresji</h4>
      <h4 v-else>Chmura najczęściej występujących słów</h4>

      <svg id="hist" v-if="choose_plot === 0" preserveAspectRatio="xMidYMid meet"></svg>
      <svg id="donut" v-else-if="choose_plot === 1" preserveAspectRatio="xMidYMid meet"></svg>
      <svg id="wordcloud" v-else preserveAspectRatio="xMidYMid meet"></svg>
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
h4 {
  text-align: center;
}

.form-row {
  height: 50%;
}

svg {
  width: 100%;
}

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
    height: 70%;
  }

  .form {
    width: 100%;
    height: 30%;
  }
}
</style>