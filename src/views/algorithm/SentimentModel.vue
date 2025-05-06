<template>
  <div class="sentiment-model">
    <div class="page-header">
      <el-switch
        v-model="isEvaluation"
        active-text="模型评估"
        inactive-text="情感分析"
        style="margin-right: 20px;"
      />
      <h2>{{ isEvaluation ? '情感分析模型评估' : '情感分析使用' }}</h2>
    </div>

    <div v-if="isEvaluation" class="evaluation-content">
      <el-row :gutter="20" style="height: 100%;">
        <el-col :span="12" style="height: 100%;">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>模型评估指标</span>
              </div>
            </template>
            <div id="radarChart" ref="radarChartRef"></div>
          </el-card>
        </el-col>
        <el-col :span="12" style="height: 100%;">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>混淆矩阵分析</span>
                <el-select v-model="selectedModel" placeholder="选择模型" style="width: 180px">
                  <el-option label="朴素贝叶斯" value="nb" />
                  <el-option label="BiLSTM" value="bilstm" />
                  <el-option label="TextCNN" value="textcnn" />
                  <el-option label="百度情感分析" value="baidu" />
                  <el-option label="DeepSeek情感分析" value="deepseek" />
                </el-select>
              </div>
            </template>
            <div id="confusionMatrix" ref="confusionMatrixRef"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div v-else class="usage-content">
      <!-- 情感分析使用页面的内容将在后续添加 -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

const isEvaluation = ref(true)
const selectedModel = ref('deepseek')
const radarChartRef = ref(null)
const confusionMatrixRef = ref(null)
let radarChart = null
let confusionChart = null

const modelData = {
  nb: {
    name: '朴素贝叶斯',
    metrics: [90, 90, 90, 90, 95.75],
    confusion: [[1592, 201], [160, 1647]]
  },
  bilstm: {
    name: 'BiLSTM',
    metrics: [89, 89, 89, 89, 94.92],
    confusion: [[1551, 242], [169, 1638]]
  },
  textcnn: {
    name: 'TextCNN',
    metrics: [94.08, 97.78, 90.26, 93.87, 98.72],
    confusion: [[1756, 37], [176, 1631]]
  },
  baidu: {
    name: '百度情感分析',
    metrics: [97, 97, 97, 97, 97.14],
    confusion: [[1731, 69], [34, 1766]]
  },
  deepseek: {
    name: 'DeepSeek情感分析',
    metrics: [98.19, 98.11, 98.28, 98.20, 98.19],
    confusion: [[1766, 34], [31, 1769]]
  }
}

onMounted(async () => {
  await nextTick()
  const initInterval = setInterval(() => {
    if (document.getElementById('radarChart') && document.getElementById('confusionMatrix')) {
      clearInterval(initInterval)
      initCharts()
    }
  }, 100)
})

const initCharts = () => {
  radarChart = echarts.init(document.getElementById('radarChart'))
  confusionChart = echarts.init(document.getElementById('confusionMatrix'))
  
  initRadarChart()
  updateConfusionMatrix()
  
  window.addEventListener('resize', handleResize)
}

const handleResize = () => {
  radarChart?.resize()
  confusionChart?.resize()
}

watch(selectedModel, () => {
  nextTick(() => {
    updateConfusionMatrix()
  })
})

watch(isEvaluation, async () => {
  if (isEvaluation.value) {
    await nextTick()
    initCharts()
  }
})

const initRadarChart = () => {
  const metrics = ['准确率', '精确率', '召回率', 'F1得分', 'AUC']
  
  const option = {
    backgroundColor: '#fff',
    title: {
      text: '模型性能对比',
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      data: Object.values(modelData).map(m => m.name),
      orient: 'vertical',
      right: 0,
      top: 'middle'
    },
    radar: {
      indicator: metrics.map(name => ({ name, max: 100 })),
      center: ['40%', '50%'],
      radius: '60%',
      splitLine: {
        lineStyle: {
          color: '#ddd'
        }
      }
    },
    series: [{
      type: 'radar',
      data: Object.values(modelData).map(model => ({
        name: model.name,
        value: model.metrics,
        symbolSize: 6,
        lineStyle: {
          width: 2
        },
        areaStyle: {
          opacity: 0.2
        }
      }))
    }]
  }
  
  radarChart.setOption(option)
}

const updateConfusionMatrix = () => {
  if (!confusionChart) return
  
  const model = modelData[selectedModel.value]
  const matrix = model.confusion
  
  const option = {
    backgroundColor: '#fff',
    title: {
      text: `${model.name}混淆矩阵`,
      left: 'center',
      textStyle: {
        fontSize: 16
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const types = ['真正例(TP)', '假正例(FP)', '假负例(FN)', '真负例(TN)']
        return `${types[params.dataIndex]}: ${params.value}`
      }
    },
    xAxis: {
      type: 'category',
      data: ['预测结果'],
      axisLabel: { interval: 0 }
    },
    yAxis: {
      type: 'value',
      max: Math.max(...matrix.flat()) * 1.1
    },
    grid: {
      top: '15%',
      left: '10%',
      right: '10%',
      bottom: '10%',
      containLabel: true
    },
    series: [
      {
        name: '混淆矩阵',
        type: 'bar',
        barWidth: '60%',
        stack: 'total',
        data: [
          { value: matrix[0][0], itemStyle: { color: '#67C23A' } },  // TP
          { value: matrix[0][1], itemStyle: { color: '#F56C6C' } },  // FP
          { value: matrix[1][0], itemStyle: { color: '#E6A23C' } },  // FN
          { value: matrix[1][1], itemStyle: { color: '#409EFF' } }   // TN
        ],
        label: {
          show: true,
          position: 'inside',
          color: '#fff',
          fontSize: 12
        }
      }
    ]
  }
  
  confusionChart.setOption(option)
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  radarChart?.dispose()
  confusionChart?.dispose()
})
</script>

<style scoped>
.sentiment-model {
  padding: 20px;
  height: calc(100vh - 40px);
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.evaluation-content {
  flex: 1;
  min-height: 0;
}

.chart-card {
  height: 100%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__header) {
  padding: 0;
}

:deep(.el-card__body) {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

#radarChart, #confusionMatrix {
  flex: 1;
  width: 100%;
  min-height: 300px;
}
</style>