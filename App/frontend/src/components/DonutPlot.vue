<script setup>
import * as d3 from 'd3';
import { ref, onMounted } from 'vue';

const width = 600
const height = 400
const margin = { top: 20, right: 20, bottom: 30, left: 40 }

const svgRef = ref(null)


</script>

<template>
  <div>
    <svg ref="donutChart"></svg>
  </div>
</template>

<style scoped>
svg {
  display: block;
  margin: auto;
}
</style>
