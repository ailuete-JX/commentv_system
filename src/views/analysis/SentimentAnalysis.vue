<template>
  <div class="word-frequency-analysis">
    <el-card class="chart-card">
      <div class="chart-container" ref="barChartRef"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const barChartRef = ref(null)
let barChart = null

// 词频统计数据
const wordFrequencyData = [
  { word: "清洁", value: 25196 },
  { word: "干净", value: 23958 },
  { word: "能力", value: 17045 },
  { word: "效果", value: 15281 },
  { word: "智能", value: 15231 },
  { word: "不错", value: 13940 },
  { word: "安装", value: 12572 },
  { word: "买", value: 12259 },
  { word: "颜值", value: 12126 },
  { word: "拖", value: 11582 },
  { word: "外观", value: 11097 },
  { word: "避障", value: 10846 },
  { word: "解放双手", value: 10050 },
  { word: "家里", value: 9702 },
  { word: "打扫", value: 9568 },
  { word: "拖地", value: 9035 },
  { word: "功能", value: 8847 },
  { word: "噪音", value: 8780 },
  { word: "清扫", value: 8552 },
  { word: "续航", value: 8010 },
  { word: "师傅", value: 7548 },
  { word: "满意", value: 7421 },
  { word: "高", value: 7395 },
  { word: "真的", value: 7367 },
  { word: "声音", value: 7319 },
  { word: "自动", value: 6714 },
  { word: "扫地", value: 6459 },
  { word: "程度", value: 6393 }
]

const initBarChart = () => {
  if (!barChartRef.value) return
  
  barChart = echarts.init(barChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      top: '3%',
      left: '8%',
      right: '4%',
      bottom: '8%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: wordFrequencyData.map(item => item.word),
      axisLabel: {
        interval: 0,
        rotate: 45,
        fontSize: 12,
        color: '#666'
      },
      axisTick: {
        alignWithLabel: true
      }
    },
    yAxis: {
      type: 'value',
      name: '',
      nameTextStyle: {
        color: '#666',
        fontSize: 12,
        padding: [0, 0, 0, 30]
      },
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: '#DDD'
        }
      }
    },
    series: [
      {
        name: '出现次数',
        type: 'bar',
        barWidth: '60%',
        data: wordFrequencyData.map(item => ({
          value: item.value,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#73ADD5' },
              { offset: 0.5, color: '#546DB5' },
              { offset: 1, color: '#3A4A8A' }
            ])
          }
        })),
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#95C0ED' },
              { offset: 0.7, color: '#73ADD5' },
              { offset: 1, color: '#546DB5' }
            ])
          }
        }
      }
    ]
  }

  barChart.setOption(option)
}

onMounted(() => {
  initBarChart()
  window.addEventListener('resize', () => {
    barChart?.resize()
  })
})
</script>

<style scoped>
.word-frequency-analysis {
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.chart-card {
  height: calc(100% - 40px);
  margin: 0;
}

.chart-container {
  height: 100%;
  width: 100%;
}

:deep(.el-card__body) {
  height: 100%;
  padding: 20px !important;
}
</style>