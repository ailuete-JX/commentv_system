<template>
  <div class="product-analysis">
    <el-card class="chart-card">
      <!-- 评分变化折线图 -->
      <div class="chart-section">
        <div class="trend-chart" ref="trendChartRef"></div>
      </div>
      <!-- 最终评分对比图 -->
      <div class="chart-section">
        <div class="final-score-chart" ref="finalScoreRef"></div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'

const trendChartRef = ref(null)
const finalScoreRef = ref(null)
let trendChart = null
let finalScoreChart = null

// 评分变化数据
const trendData = {
  dates: ["2023-03", "2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12", "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04"],
  series: [
    {
      name: "科沃斯",
      data: [NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, 3.576923076923077, 2.9166666666666665, 4.527397260273973, 4.462121212121212, 3.6551724137931036, 4.1826923076923075, 4.569230769230769, 4.485990338164251, 4.3336766220391345, 4.409954751131222, 4.386206896551724, 4.881011403073872, 4.900271370420624, NaN]
    },
    {
      name: "石头",
      data: [NaN, NaN, NaN, NaN, NaN, NaN, 4.580952380952381, 2.955056179775281, 3.9414634146341463, 3.802469135802469, 3.938775510204082, 2.91025641025641, 2.216666666666667, 2.0, 1.8103448275862069, 1.403225806451613, 1.75, 2.169491525423729, 3.696, 4.057401812688822, 4.255986787778696, 4.257685352622062, 4.563395810363837, 4.9273579379027534, 4.938931297709924, NaN]
    },
    {
      name: "小米",
      data: [3.2, 3.85, 2.46875, 2.3555555555555556, 2.5384615384615383, 2.966666666666667, 2.276595744680851, 2.590909090909091, 2.888059701492537, 3.382608695652174, 3.4475524475524475, 4.122448979591836, 3.942857142857143, 3.9086538461538463, 4.159090909090909, 4.430656934306569, 4.178743961352657, 4.380228136882129, 4.454918032786885, 4.587165234967155, 4.376601195559351, 4.5, 4.665171898355755, 4.785945945945946, 4.808333333333334, NaN]
    },
    {
      name: "云鲸",
      data: [NaN, NaN, NaN, NaN, NaN, NaN, 1.5555555555555556, 1.3, 1.4683544303797469, 1.627906976744186, 1.4736842105263157, 1.71875, 1.627906976744186, 3.1466666666666665, 4.057142857142857, 3.8310249307479225, 3.40625, 3.5491329479768785, 3.2346938775510203, 3.5875912408759123, 4.5349105597230235, 4.4969325153374236, 4.429012345679013, 4.814173228346457, 4.83645443196005, 4.937142857142857]
    },
    {
      name: "追觅",
      data: [NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, 4.946236559139785, 4.8347107438016526, 4.8924050632911396, 4.845588235294118, 4.651162790697675, 4.9, 4.865168539325842, 4.6784140969163, 4.567120622568093, 4.776293823038397, 4.808846761453396, 4.877427184466019, 4.866174055829228, 4.931901279707495]
    }
  ]
}

// 初始化评分变化折线图
const initTrendChart = () => {
  if (!trendChartRef.value) return
  
  nextTick(() => {
    trendChart = echarts.init(trendChartRef.value)
    
    const option = {
      title: {
        text: '各品牌月度评分变化趋势',
        left: 'center',
        top: '10px',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'axis',
        formatter: function(params) {
          let result = params[0].axisValue + '<br/>'
          params.forEach(param => {
            if (!isNaN(param.value)) {
              result += param.marker + param.seriesName + ': ' + param.value.toFixed(2) + '<br/>'
            }
          })
          return result
        }
      },
      legend: {
        data: trendData.series.map(item => item.name),
        bottom: '5px',
        type: 'scroll',
        textStyle: {
          fontSize: 12
        }
      },
      grid: {
        left: '5%',
        right: '5%',
        bottom: '15%',
        top: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: trendData.dates,
        axisLabel: {
          rotate: 45,
          fontSize: 11,
          interval: 2
        }
      },
      yAxis: {
        type: 'value',
        name: '平均评分',
        min: 1,
        max: 5
      },
      series: trendData.series.map(item => ({
        name: item.name,
        type: 'line',
        smooth: true,
        data: item.data
      }))
    }
    
    trendChart.setOption(option)
  })
}

// 品牌评分数据
const brandScores = [
  { brand: '追觅', score: 4.819165755 },
  { brand: '科沃斯', score: 4.60548419 },
  { brand: '云鲸', score: 4.443648986 },
  { brand: '小米', score: 4.386506449 },
  { brand: '石头', score: 4.325271644 }
]

// 初始化最终评分对比图
const initFinalScoreChart = () => {
  if (!finalScoreRef.value) return
  
  nextTick(() => {
    finalScoreChart = echarts.init(finalScoreRef.value)
    
    const option = {
      title: {
        text: '各品牌最终评分对比',
        left: 'center',
        top: '10px',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: '{b}: {c}分'
      },
      grid: {
        left: '10%',
        right: '10%',
        bottom: '10%',
        top: '20%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: brandScores.map(item => item.brand),
        axisTick: {
          alignWithLabel: true
        },
        axisLabel: {
          interval: 0,
          fontSize: 12
        }
      },
      yAxis: {
        type: 'value',
        min: 4.0,
        max: 5.0,
        interval: 0.2,
        axisLabel: {
          formatter: '{value}分',
          fontSize: 12
        }
      },
      series: [{
        name: '评分',
        type: 'bar',
        data: brandScores.map(item => ({
          value: item.score.toFixed(2),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          }
        })),
        barWidth: '30%',
        label: {
          show: true,
          position: 'top',
          formatter: '{c}分',
          fontSize: 12
        }
      }]
    }
    
    finalScoreChart.setOption(option)
  })
}

// 监听窗口大小变化
const handleResize = () => {
  trendChart?.resize()
  finalScoreChart?.resize()
}

onMounted(() => {
  initTrendChart()
  initFinalScoreChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  trendChart?.dispose()
  finalScoreChart?.dispose()
})
</script>

<style scoped>
.product-analysis {
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chart-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

:deep(.el-card__body) {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chart-section {
  flex: 1;
  position: relative;
  height: calc(50% - 10px);
  min-height: 0;
  margin: 5px 0;
}

.trend-chart,
.final-score-chart {
  width: 100%;
  height: 100%;
  min-height: 0;
}
</style>