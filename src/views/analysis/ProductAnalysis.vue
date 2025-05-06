<template>
  <div class="product-analysis">
    <el-card class="chart-card">
      <div class="chart-container" ref="sunburstRef"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import * as XLSX from 'xlsx'

const sunburstRef = ref(null)
let sunburstChart = null

// 处理Excel数据，转换为旭日图所需的格式
const processExcelData = (data) => {
  // 创建数据结构
  const platforms = {}
  data.forEach(row => {
    const platform = row['平台'] === 'JD' ? '京东' : '淘宝'
    if (!platforms[platform]) {
      platforms[platform] = {
        name: platform,
        children: []
      }
    }
  })

  // 为每个平台创建品牌层级
  Object.keys(platforms).forEach(platform => {
    const brandMap = {}
    data.filter(row => (row['平台'] === 'JD' ? '京东' : '淘宝') === platform)
      .forEach(row => {
        const brand = row['品牌']
        if (!brandMap[brand]) {
          brandMap[brand] = {
            name: brand,
            children: []
          }
        }
      })

    // 为每个品牌创建产品型号层级
    Object.keys(brandMap).forEach(brand => {
      const modelMap = {}
      data.filter(row => 
        (row['平台'] === 'JD' ? '京东' : '淘宝') === platform && 
        row['品牌'] === brand
      ).forEach(row => {
        const model = row['产品型号']
        if (!modelMap[model]) {
          modelMap[model] = {
            name: model,
            value: 0
          }
        }
        modelMap[model].value++
      })
      
      brandMap[brand].children = Object.values(modelMap)
      // 计算品牌总评论数
      brandMap[brand].value = brandMap[brand].children.reduce((sum, model) => sum + model.value, 0)
    })
    
    platforms[platform].children = Object.values(brandMap)
    // 计算平台总评论数
    platforms[platform].value = platforms[platform].children.reduce((sum, brand) => sum + brand.value, 0)
  })

  return Object.values(platforms)
}

// 读取Excel文件数据
const loadExcelData = async () => {
  try {
    console.log('开始加载Excel文件...')
    const response = await fetch('/public/中期后_情感分析后完整数据集.xlsx')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const arrayBuffer = await response.arrayBuffer()
    const workbook = XLSX.read(arrayBuffer)
    
    // 获取第一个工作表的数据
    const sheetName = workbook.SheetNames[0]
    const worksheet = workbook.Sheets[sheetName]
    const data = XLSX.utils.sheet_to_json(worksheet)
    
    return processExcelData(data)
  } catch (error) {
    console.error('处理Excel文件时出错:', error)
    return null
  }
}

const initSunburstChart = (data) => {
  if (!sunburstRef.value) return
  
  sunburstChart = echarts.init(sunburstRef.value)
  
  // 计算最大值用于视觉映射
  const getMaxValue = (data) => {
    let max = 0
    data.forEach(item => {
      if (item.value) {
        max = Math.max(max, item.value)
      }
      if (item.children) {
        item.children.forEach(child => {
          if (child.value) {
            max = Math.max(max, child.value)
          }
          if (child.children) {
            child.children.forEach(grandChild => {
              if (grandChild.value) {
                max = Math.max(max, grandChild.value)
              }
            })
          }
        })
      }
    })
    return max
  }

  const maxValue = getMaxValue(data)
  
  const option = {
    visualMap: {
      type: 'continuous',
      min: 0,
      max: maxValue,
      inRange: {
        color: ['#2F93C8', '#AEC48F', '#FFDB5C', '#F98862']
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const value = params.value || 0
        let percent = ''
        if (params.treePathInfo && params.treePathInfo.length > 1) {
          const parentValue = params.treePathInfo[params.treePathInfo.length - 2].value
          percent = ` (${((value / parentValue) * 100).toFixed(1)}%)`
        }
        return `${params.name}: ${value}条评论${percent}`
      }
    },
    series: {
      type: 'sunburst',
      data: data,
      radius: [0, '90%'],
      label: {
        rotate: 'radial',
        minAngle: 15
      },
      emphasis: {
        focus: 'ancestor'
      },
      levels: [
        {},
        {
          r0: '0%',
          r: '30%',
          label: {
            rotate: 0
          }
        },
        {
          r0: '30%',
          r: '60%',
          label: {
            rotate: 0
          }
        },
        {
          r0: '60%',
          r: '90%',
          label: {
            rotate: 'tangential'
          }
        }
      ]
    }
  }

  sunburstChart.setOption(option)
}

onMounted(async () => {
  const data = await loadExcelData()
  if (data) {
    initSunburstChart(data)
    
    window.addEventListener('resize', () => {
      sunburstChart?.resize()
    })
  }
})
</script>

<style scoped>
.product-analysis {
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.chart-card {
  height: 100%;
}

.chart-container {
  height: calc(100% - 20px);
  min-height: 500px;
  width: 100%;
}

:deep(.el-card__body) {
  height: calc(100% - 20px);
  padding: 20px !important;
}
</style>