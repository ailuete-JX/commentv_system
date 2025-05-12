<template>
  <div class="keywords-analysis">
    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>关键词词云图</span>
              <div class="selectors">
                <el-select v-model="selectedBrand" placeholder="选择品牌" style="width: 150px; margin-right: 10px">
                  <el-option label="总体" value="总体" />
                  <el-option label="科沃斯" value="科沃斯" />
                  <el-option label="小米" value="小米" />
                  <el-option label="石头" value="石头" />
                  <el-option label="追觅" value="追觅" />
                  <el-option label="云鲸" value="云鲸" />
                </el-select>
                <el-select v-model="selectedSentiment" placeholder="选择情感倾向" style="width: 150px">
                  <el-option label="正向评价" value="positive" />
                  <el-option label="负向评价" value="negative" />
                </el-select>
              </div>
            </div>
          </template>
          <div class="chart-container" ref="wordCloudRef"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>Top 10关键词</span>
            </div>
          </template>
          <div class="chart-container" ref="barChartRef"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import * as XLSX from 'xlsx'

const wordCloudRef = ref(null)
const barChartRef = ref(null)
const selectedBrand = ref('总体')
const selectedSentiment = ref('positive')
let wordCloudChart = null
let barChart = null
let excelData = {
  positive: {},
  negative: {}
}

// 读取Excel文件数据
const loadExcelData = async () => {
  try {    console.log('开始加载Excel文件...')
    const response = await fetch('/中期后_正负向情感关键词统计.xlsx')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const arrayBuffer = await response.arrayBuffer()
    console.log('Excel文件加载成功，开始解析...')
    
    const workbook = XLSX.read(arrayBuffer)
    console.log('工作簿解析成功，可用表格:', workbook.SheetNames)
    
    // 读取正向表数据
    const positiveSheet = workbook.Sheets['正向']
    if (!positiveSheet) {
      throw new Error('未找到"正向"表格')
    }
    const positiveData = XLSX.utils.sheet_to_json(positiveSheet)
    console.log('正向数据解析成功，行数:', positiveData.length)
    
    // 读取负向表数据
    const negativeSheet = workbook.Sheets['负向']
    if (!negativeSheet) {
      throw new Error('未找到"负向"表格')
    }
    const negativeData = XLSX.utils.sheet_to_json(negativeSheet)
    console.log('负向数据解析成功，行数:', negativeData.length)
    
    // 处理数据
    const brands = ['总体', '科沃斯', '小米', '石头', '追觅', '云鲸']
    brands.forEach(brand => {
      // 处理正向数据
      const positiveWords = positiveData.map(row => ({
        name: row[`${brand}_正向`],
        value: parseFloat(row[`${brand}_正权重`])
      })).filter(item => item.name && !isNaN(item.value))
      
      // 处理负向数据
      const negativeWords = negativeData.map(row => ({
        name: row[`${brand}_负向`],
        value: parseFloat(row[`${brand}_负权重`])
      })).filter(item => item.name && !isNaN(item.value))
      
      // 只取前35个词
      excelData.positive[brand] = positiveWords.slice(0, 35)
      excelData.negative[brand] = negativeWords.slice(0, 35)
      
      console.log(`${brand}数据处理完成:`, 
        `正向词数量: ${excelData.positive[brand].length}`,
        `负向词数量: ${excelData.negative[brand].length}`)
    })
    
    console.log('所有数据处理完成，开始更新词云图...')
    updateCharts()
  } catch (error) {
    console.error('处理Excel文件时出错:', error)
  }
}

const updateWordCloud = () => {
  if (!wordCloudChart) {
    console.error('词云图实例未初始化')
    return
  }
  
  const sentiment = selectedSentiment.value === 'positive' ? 'positive' : 'negative'
  const brand = selectedBrand.value
  const data = excelData[sentiment][brand] || []
  
  console.log('更新词云图:', 
    `品牌: ${brand}`, 
    `情感: ${sentiment}`, 
    `数据量: ${data.length}`,
    '数据示例:', data.slice(0, 3))
  
  const option = {
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '95%',
      height: '95%',
      right: null,
      bottom: null,
      sizeRange: [
        Math.max(20, Math.min(20, wordCloudRef.value.clientWidth / 40)),
        Math.max(45, Math.min(80, wordCloudRef.value.clientWidth / 10))
      ],
      rotationRange: [-45, 45],
      rotationStep: 5,
      gridSize: Math.max(8, Math.min(16, wordCloudRef.value.clientWidth / 60)),
      drawOutOfBound: false,
      layoutAnimation: true,
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: function() {
          const colors = selectedSentiment.value === 'positive' 
            ? ['#91cc75', '#67b35c', '#4d9f3f', '#3c8a2e', '#2b751d'] 
            : ['#ee6666', '#d64646', '#c32626', '#b00606', '#9d0505']
          return colors[Math.floor(Math.random() * colors.length)]
        }
      },
      emphasis: {
        focus: 'self',
        textStyle: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data: data
    }]
  }

  try {
    wordCloudChart.setOption(option, true)
    console.log('词云图更新成功')
  } catch (error) {
    console.error('更新词云图时出错:', error)
  }
}

const updateBarChart = () => {
  if (!barChart) {
    console.error('柱状图实例未初始化')
    return
  }
  
  const sentiment = selectedSentiment.value === 'positive' ? 'positive' : 'negative'
  const brand = selectedBrand.value
  const data = [...(excelData[sentiment][brand] || [])]
    .sort((a, b) => b.value - a.value)
    .slice(0, 10)
    .reverse()
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      top: '3%',
      left: '3%',
      right: '12%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '权重',
      nameGap: 5,
      nameTextStyle: {
        fontSize: 10
      },
      axisLabel: {
        fontSize: 10
      }
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLabel: {
        interval: 0,
        fontSize: 10,
        width: 60,
        overflow: 'truncate'
      }
    },
    series: [
      {
        name: '权重',
        type: 'bar',
        data: data.map(item => ({
          value: item.value,
          itemStyle: {
            color: selectedSentiment.value === 'positive' 
              ? '#91cc75'
              : '#ee6666'
          }
        })),
        label: {
          show: true,
          position: 'right',
          formatter: '{c}',
          fontSize: 10
        }
      }
    ]
  }

  barChart.setOption(option)
}

const updateCharts = () => {
  updateWordCloud()
  updateBarChart()
}

watch([selectedBrand, selectedSentiment], () => {
  console.log('选项变更:', 
    `品牌: ${selectedBrand.value}`, 
    `情感: ${selectedSentiment.value}`)
  updateCharts()
})

onMounted(async () => {
  console.log('组件挂载，初始化图表...')
  try {
    wordCloudChart = echarts.init(wordCloudRef.value)
    barChart = echarts.init(barChartRef.value)
    await loadExcelData()
    
    window.addEventListener('resize', () => {
      wordCloudChart?.resize()
      barChart?.resize()
    })
  } catch (error) {
    console.error('初始化图表时出错:', error)
  }
})
</script>

<style scoped>
.keywords-analysis {
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.chart-row {
  height: 100%;
}

.chart-card {
  height: 100%;
}

.chart-container {
  height: calc(100% - 60px);
  min-height: 300px;
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.selectors {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

:deep(.el-card__body) {
  height: calc(100% - 60px);
  padding: 10px !important;
}

:deep(.el-row) {
  height: 100%;
  margin: 0 !important;
}

@media screen and (max-width: 1200px) {
  .chart-container {
    min-height: 250px;
  }
  
  .selectors {
    width: 100%;
    justify-content: flex-end;
  }
}

@media screen and (max-width: 768px) {
  .keywords-analysis {
    padding: 5px;
  }
  
  :deep(.el-card__body) {
    padding: 5px !important;
  }
  
  .chart-container {
    min-height: 200px;
  }
}
</style>