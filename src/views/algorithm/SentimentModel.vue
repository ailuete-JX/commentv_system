<template>
  <div class="sentiment-model">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>模型评估指标</span>
            </div>
          </template>
          <div class="chart-wrapper">
            <div id="radarChart" style="width: 100%; height: 100%;"></div>
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
            <div id="confusionMatrix" style="width: 100%; height: 100%;"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

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
  if (!document.getElementById('radarChart')) return
  
  radarChart = echarts.init(document.getElementById('radarChart'))
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
    },    radar: {
      indicator: metrics.map(name => ({ 
        name,
        min: 85,
        max: 100
      })),
      center: ['50%', '55%'],
      radius: '70%',
      axisName: {
        color: '#000000',
        fontSize: 12,
        padding: [3, 5]
      },
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
  if (!document.getElementById('confusionMatrix')) return

  if (!confusionChart) {
    confusionChart = echarts.init(document.getElementById('confusionMatrix'))
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
      top: '15%',
      bottom: '15%',
      left: '15%',
      right: '15%',
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
        color: [
          '#08306B',
          '#f7f7f7',
          '#F5FAFE'
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
  window.addEventListener('resize', handleResize)
  // 使用nextTick确保DOM已经渲染完成
  setTimeout(() => {
    initRadarChart()
    updateConfusionMatrix()
  }, 0)
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
  background-color: #fff;
  height: calc(100vh - 100px);
  box-sizing: border-box;
}

.el-row {
  height: 100%;
}

.el-col {
  height: 100%;
}

.chart-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-wrapper {
  flex: 1;
  min-height: 500px;
  height: calc(100% - 60px);
  padding: 10px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
}

#radarChart, #confusionMatrix {
  width: 100% !important;
  height: 100% !important;
  min-height: 450px;
}

:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__body) {
  flex: 1;
  padding: 0;
  overflow: hidden;
}
</style>