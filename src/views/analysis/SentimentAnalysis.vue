<template>
  <div class="word-frequency-analysis">
    <el-card class="chart-card">
      <template #header>
        <div class="card-header">
          <span>{{ showDualChart ? '正负向高频词对比' : '总体高频词分布' }}</span>
          <el-switch
            v-model="showDualChart"
            active-text="正负对比"
            inactive-text="总体分布"
          />
        </div>
      </template>
      <div class="chart-container" ref="barChartRef"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'

const barChartRef = ref(null)
const showDualChart = ref(false)
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

// 正向情感数据
const positiveData = [
  { name: '清洁', value: 0.1770 },
  { name: '干净', value: 0.1613 },
  { name: '颜值', value: 0.1482 },
  { name: '避障', value: 0.1282 },
  { name: '智能', value: 0.1099 },
  { name: '拖地', value: 0.0903 },
  { name: '效果', value: 0.0901 },
  { name: '不错', value: 0.0879 },
  { name: '外观', value: 0.0874 },
  { name: '能力', value: 0.0835 },
  { name: '安装', value: 0.0811 },
  { name: '打扫', value: 0.0750 }
]

// 负向情感数据
const negativeData = [
  { name: '客服', value: 0.1948 },
  { name: '干净', value: 0.0902 },
  { name: '拖布', value: 0.0760 },
  { name: '售后', value: 0.0751 },
  { name: '京东', value: 0.0729 },
  { name: '清洁', value: 0.0728 },
  { name: '拖地', value: 0.0712 },
  { name: '赠品', value: 0.0675 },
  { name: '垃圾', value: 0.0590 },
  { name: '基站', value: 0.0578 },
  { name: '降价', value: 0.0526 },
  { name: '差评', value: 0.0524 }
]

const updateChart = () => {
  if (!barChart || !barChartRef.value) return

  // 强制重新计算图表大小
  barChart.resize()

  if (showDualChart.value) {    // 双向柱状图配置
    const option = {      title: [
        {
          text: '负面情感倾向评论',
          left: '30%',
          top: 5,
          textStyle: {
            fontSize: 13,
            fontWeight: 'normal',
            color: '#666'
          }
        },
        {          text: '正面情感倾向评论',
          left: '57%',
          top: 5,
          textStyle: {
            fontSize: 13,
            fontWeight: 'normal',
            color: '#666'
          }
        }
      ],
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        formatter: function(params) {
          return `${params[0].name}: ${params[0].value}`;
        }
      },      grid: [
        {
          top: '7%',
          bottom: '8%',
          right: '54%',
          width: '38%'
        },
        {
          top: '7%',
          bottom: '8%',
          left: '54%',
          width: '38%'
        }
      ],
      xAxis: [{        type: 'value',
        inverse: true,
        position: 'bottom',
        max: 0.25,
        splitLine: { show: false },
        axisTick: { show: false },
        axisLabel: {
          formatter: '{value}',
          color: '#F56C6C'
        }
      }, {
        gridIndex: 1,
        type: 'value',
        position: 'bottom',
        max: 0.25,
        splitLine: { show: false },
        axisTick: { show: false },
        axisLabel: {
          formatter: '{value}',
          color: '#546DB5'
        }
      }],
      yAxis: [{
        type: 'category',
        inverse: true,
        position: 'right',
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: {
          align: 'left',
          margin: 0,
          fontSize: 12,
          color: '#666'
        },
        data: negativeData.map(item => item.name)
      }, {
        gridIndex: 1,
        type: 'category',
        inverse: true,
        position: 'left',
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: {
          align: 'right',
          margin: 0,
          fontSize: 12,
          color: '#666'
        },
        data: positiveData.map(item => item.name)
      }],
      series: [{
        name: '负面情感倾向评论',
        type: 'bar',        xAxisIndex: 0,
        yAxisIndex: 0,        label: {
          show: true,
          position: 'left',
          formatter: function(params) {
            return params.value.toString();
          },
          color: '#F56C6C',
          fontSize: 12
        },
        barWidth: '60%',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [{
            offset: 0,
            color: '#ff9696'
          }, {
            offset: 1,
            color: '#F56C6C'
          }])
        },
        data: negativeData.map(item => item.value.toFixed(4))
      }, {
        name: '正面情感倾向评论',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        label: {
          show: true,
          position: 'right',
          formatter: function(params) {
            return params.value.toString();
          },
          color: '#546DB5',
          fontSize: 12
        },
        barWidth: '60%',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [{
            offset: 0,
            color: '#73ADD5'
          }, {
            offset: 1,
            color: '#546DB5'
          }])
        },
        data: positiveData.map(item => item.value.toFixed(4))
      }]
    }
    barChart.setOption(option, true)
  } else {
    // 总体柱状图配置
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },      grid: {
        top: '3%',
        bottom: '5%',
        left: '2%',
        right: '2%',
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
        name: '出现次数',
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
    barChart.setOption(option, true)
  }
}

// 监听图表切换
watch(showDualChart, () => {
  updateChart()
})

onMounted(() => {
  // 确保DOM完全挂载后再初始化图表
  nextTick(() => {
    barChart = echarts.init(barChartRef.value)
    updateChart()
    
    // 添加窗口大小变化监听，实现自适应
    const resizeHandler = () => {
      if (barChart) {
        barChart.resize()
      }
    }
    window.addEventListener('resize', resizeHandler)

    // 组件卸载时移除监听器
    onUnmounted(() => {
      window.removeEventListener('resize', resizeHandler)
    })
  })
})
</script>

<style scoped>
.word-frequency-analysis {
  height: 80vh;
  padding: 0 0.5vw;
  box-sizing: border-box;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  margin: 0.5vh auto;
  max-width: 99%;
}

.chart-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin: 0;
  overflow: hidden;
  height: 100%;
  max-height: 82vh;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 4px;
  height: 24px;
  flex-shrink: 0;
}

.chart-container {
  flex: 1;
  width: 99%;
  margin: 0 auto;
  height: 100%;
  position: relative;
  overflow: hidden;
  max-height: calc(80vh - 28px);
}

:deep(.el-card__body) {
  flex: 1;
  padding: 0 !important;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
}

:deep(.el-switch) {
  margin-left: 6px;
}

@media screen and (max-width: 768px) {
  .word-frequency-analysis {
    padding: 0 0.5vw;
  }
  .chart-container {
    width: 100%;
  }
  :deep(.el-card__body) {
    padding: 2px 0 0 0 !important;
  }
}
</style>