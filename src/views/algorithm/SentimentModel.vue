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
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="card-header">
                <span>模型评估指标</span>
              </div>
            </template>
            <div class="chart-wrapper">
              <div id="radarChart" style="width: 100%; height: 400px;"></div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="card-header">
                <span>混淆矩阵分析</span>
                <el-select v-model="selectedModel" placeholder="选择模型" size="default">
                  <el-option label="朴素贝叶斯" value="nb" />
                  <el-option label="BiLSTM" value="bilstm" />
                  <el-option label="TextCNN" value="textcnn" />
                  <el-option label="百度情感分析" value="baidu" />
                  <el-option label="DeepSeek情感分析" value="deepseek" />
                </el-select>
              </div>
            </template>
            <div class="chart-wrapper">
              <div id="confusionMatrix" style="width: 100%; height: 400px;"></div>
            </div>
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
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const isEvaluation = ref(true)
const selectedModel = ref('deepseek')
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

const initRadarChart = () => {
  const radarDom = document.getElementById('radarChart')
  if (!radarDom) return

  radarChart = echarts.init(radarDom)
  const metrics = ['准确率', '精确率', '召回率', 'F1得分', 'AUC']
  
  const option = {
    title: {
      text: '模型性能对比',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      data: Object.values(modelData).map(m => m.name),
      orient: 'horizontal',
      top: 25,
      left: 'center'
    },
    radar: {
      indicator: metrics.map(name => ({ 
        name, 
        min: 85,  // 设置最小值为85，使差异更明显
        max: 100 
      })),
      center: ['50%', '60%'],
      radius: '60%',
      splitLine: {
        lineStyle: {
          color: '#ddd'
        }
      },
      axisLine: {
        lineStyle: {
          color: '#ddd'
        }
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['#fff']
        }
      }
    },
    series: [{
      type: 'radar',
      data: Object.values(modelData).map(model => ({
        name: model.name,
        value: model.metrics,
        symbolSize: 4,
        lineStyle: { width: 2 },
        areaStyle: { opacity: 0.2 }
      }))
    }]
  }
  
  radarChart.setOption(option)
}

const updateConfusionMatrix = () => {
  const matrixDom = document.getElementById('confusionMatrix')
  if (!matrixDom) return

  if (!confusionChart) {
    confusionChart = echarts.init(matrixDom)
  }
  
  const model = modelData[selectedModel.value]
  const matrix = model.confusion
  const total = matrix[0][0] + matrix[0][1] + matrix[1][0] + matrix[1][1]
  
  const option = {
    title: {
      text: `${model.name}混淆矩阵`,
      left: 'center',
      top: 10
    },
    tooltip: {
      position: 'top',
      formatter: function (params) {
        const value = params.data.value[2]
        const percentage = ((value / total) * 100).toFixed(2)
        return `数量: ${value}<br/>占比: ${percentage}%`
      }
    },
    grid: {
      top: 60,
      bottom: 80,  // 增加底部空间以容纳颜色条
      left: 80,    // 缩小左边距
      right: 60,   // 缩小右边距
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['预测正向', '预测负向'],
      splitArea: {
        show: true
      },
      axisLabel: {
        interval: 0,
        fontSize: 12
      }
    },
    yAxis: {
      type: 'category',
      data: ['实际正向', '实际负向'],
      splitArea: {
        show: true
      },
      axisLabel: {
        interval: 0,
        rotate: 90,
        fontSize: 12,
        margin: 4
      }
    },
    visualMap: {
      min: 0,
      max: Math.max(...matrix.flat()),
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      inRange: {
        // 使用经典的混淆矩阵颜色方案
        color: [
          '#08306B',  // 深蓝色（真负例）
          '#f7f7f7',  // 白色（过渡色）
          '#F5FAFE'   // 灰白色（真正例）
        ]
      },
      textStyle: {
        fontSize: 12
      }
    },
    series: [{
      name: '混淆矩阵',
      type: 'heatmap',
      data: [
        {
          value: [0, 0, matrix[0][0]],
          itemStyle: { color: '#08306B' },
          label: { color: '#FFFFFF' }
        },
        {
          value: [0, 1, matrix[0][1]],
          itemStyle: { color: '#F5FAFE' },
          label: { color: '#000000' }
        },
        {
          value: [1, 0, matrix[1][0]],
          itemStyle: { color: '#F5FAFE' },
          label: { color: '#000000' }
        },
        {
          value: [1, 1, matrix[1][1]],
          itemStyle: { color: '#08306B' },
          label: { color: '#FFFFFF' }
        }
      ],
      label: {
        show: true,
        formatter: function(params) {
          const value = params.data.value[2]
          const percentage = ((value / total) * 100).toFixed(1)
          return `${value}\n(${percentage}%)`
        },
        fontSize: 11,
        fontWeight: 'bold'
      }
    }]
  }
  
  confusionChart.setOption(option)
}

const handleResize = () => {
  radarChart?.resize()
  confusionChart?.resize()
}

onMounted(() => {
  // 使用setTimeout确保DOM已完全渲染
  setTimeout(() => {
    initRadarChart()
    updateConfusionMatrix()
    window.addEventListener('resize', handleResize)
  }, 300)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  radarChart?.dispose()
  confusionChart?.dispose()
})

watch(selectedModel, updateConfusionMatrix)
</script>

<style scoped>
.sentiment-model {
  padding: 20px;
  background-color: #f5f7fa;
  height: calc(100vh - 84px);
  overflow: hidden;
  box-sizing: border-box;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  height: 32px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.evaluation-content {
  height: calc(100% - 52px);
  overflow: hidden;
}

.el-row {
  margin: 0 !important;
  height: 100%;
}

.el-col {
  height: 100%;
  padding: 0 10px !important;
}

.chart-card {
  height: 100%;
  margin: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-wrapper {
  padding: 5px;
  height: calc(100% - 51px);
}

:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  padding: 0;
  height: calc(100% - 51px);
}

#radarChart, #confusionMatrix {
  width: 100%;
  height: 100%;
}
</style>