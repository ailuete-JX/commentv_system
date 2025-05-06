<template>
  <div class="topics-analysis">
    <el-row :gutter="20" class="chart-row">
      <el-col :span="24">
        <el-card class="chart-card">
          <div class="chart-container" ref="barChartRef"></div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="chart-row">
      <el-col :span="24">
        <el-card class="chart-card">
          <div class="chart-container" ref="lineChartRef"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts/core'
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import { LineChart, BarChart } from 'echarts/charts'
import { UniversalTransition } from 'echarts/features'
import { SVGRenderer } from 'echarts/renderers'

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  BarChart,
  SVGRenderer,
  UniversalTransition
])

const barChartRef = ref(null)
const lineChartRef = ref(null)

// 堆叠柱状图数据
const stackedBarData = {
  xAxis: ["2023-03", "2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12", "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04"],
  series: [
    {"name": "科沃斯-好评", "type": "bar", "stack": "科沃斯", "emphasis": {"focus": "series"}, "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 102, 15, 276, 622, 99, 137, 166, 934, 864, 1572, 1002, 3067, 1900, 0]},
    {"name": "科沃斯-差评", "type": "bar", "stack": "科沃斯", "emphasis": {"focus": "series"}, "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 9, 36, 95, 42, 30, 23, 152, 205, 210, 156, 130, 64, 0]},
    {"name": "石头-好评", "type": "bar", "stack": "石头", "emphasis": {"focus": "series"}, "data": [0, 27, 16, 6, 1, 0, 93, 40, 287, 105, 68, 34, 13, 5, 164, 200, 8, 16, 137, 839, 1357, 1456, 1493, 3136, 1594, 0]},
    {"name": "石头-差评", "type": "bar", "stack": "石头", "emphasis": {"focus": "series"}, "data": [0, 4, 0, 0, 0, 0, 12, 49, 123, 57, 30, 44, 48, 35, 58, 129, 45, 47, 50, 251, 260, 236, 123, 56, 29, 0]},
    {"name": "小米-好评", "type": "bar", "stack": "小米", "emphasis": {"focus": "series"}, "data": [7, 25, 82, 93, 21, 32, 38, 26, 177, 141, 142, 142, 154, 191, 333, 676, 190, 260, 763, 2174, 1337, 944, 674, 995, 508, 0]},
    {"name": "小米-差评", "type": "bar", "stack": "小米", "emphasis": {"focus": "series"}, "data": [13, 15, 31, 46, 13, 38, 38, 49, 98, 66, 72, 50, 61, 76, 74, 103, 57, 54, 110, 259, 284, 179, 99, 86, 36, 0]},
    {"name": "云鲸-好评", "type": "bar", "stack": "云鲸", "emphasis": {"focus": "series"}, "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 34, 150, 240, 91, 103, 49, 333, 1507, 697, 270, 630, 852, 3145]},
    {"name": "云鲸-差评", "type": "bar", "stack": "云鲸", "emphasis": {"focus": "series"}, "data": [0, 0, 0, 0, 0, 0, 36, 40, 79, 43, 38, 32, 43, 41, 60, 121, 69, 70, 49, 215, 239, 132, 64, 37, 42, 57]},
    {"name": "追觅-好评", "type": "bar", "stack": "追觅", "emphasis": {"focus": "series"}, "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 92, 116, 153, 130, 39, 39, 86, 414, 908, 1124, 608, 864, 1306, 2458]},
    {"name": "追觅-差评", "type": "bar", "stack": "追觅", "emphasis": {"focus": "series"}, "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 5, 6, 4, 1, 3, 40, 120, 74, 36, 25, 43, 47]}
  ]
}

// 折线图数据
const lineChartData = {
  xAxis: ["2023-03", "2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12", "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04"],
  series: [
    {
      name: "云鲸",
      type: "line",
      data: [0, 0, 0, 0, 0, 0, 36, 40, 79, 43, 38, 32, 43, 75, 210, 361, 160, 173, 98, 548, 1746, 829, 334, 667, 894, 3202]
    },
    {
      name: "小米",
      type: "line",
      data: [20, 40, 113, 139, 34, 70, 76, 75, 275, 207, 214, 192, 215, 267, 407, 779, 247, 314, 873, 2433, 1621, 1123, 773, 1081, 544, 0]
    },
    {
      name: "石头",
      type: "line",
      data: [0, 31, 16, 6, 1, 0, 105, 89, 410, 162, 98, 78, 61, 40, 222, 329, 53, 63, 187, 1090, 1617, 1692, 1616, 3192, 1623, 0]
    },
    {
      name: "科沃斯",
      type: "line",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 125, 24, 312, 717, 141, 167, 189, 1086, 1069, 1782, 1158, 3197, 1964, 0]
    },
    {
      name: "追觅",
      type: "line",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 93, 121, 158, 136, 43, 40, 89, 454, 1028, 1198, 644, 889, 1349, 2505]
    }
  ]
}

onMounted(() => {
  initBarChart()
  initLineChart()
})

const initBarChart = () => {
  const barChart = echarts.init(barChartRef.value)
  
  const option = {
    title: {
      text: '各品牌月度好差评分布',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#ccc',
      borderWidth: 1,
      textStyle: {
        color: '#333'
      }
    },
    legend: {
      top: 25,
      textStyle: {
        fontSize: 12
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: 90,
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: stackedBarData.xAxis,
        axisLabel: {
          interval: 2,
          rotate: 45
        },
        axisLine: {
          lineStyle: {
            color: '#999'
          }
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: '评论数量',
        nameTextStyle: {
          padding: [0, 0, 0, 40]
        },
        splitLine: {
          lineStyle: {
            type: 'dashed',
            color: '#DDD'
          }
        },
        axisLine: {
          lineStyle: {
            color: '#999'
          }
        }
      }
    ],
    series: stackedBarData.series.map(item => {
      // 定义每个品牌的基础颜色
      const brandColors = {
        '科沃斯': ['#5470c6', '#ee6666'],  // 蓝色系
        '石头': ['#91cc75', '#ff7875'],     // 绿色系
        '小米': ['#fac858', '#ff9c6e'],     // 黄色系
        '云鲸': ['#73c0de', '#ff7875'],     // 青色系
        '追觅': ['#9a60b4', '#ff85c0']      // 紫色系
      }

      // 获取当前项目的品牌名
      const brand = item.name.split('-')[0]
      const isPositive = item.name.includes('好评')
      
      return {
        ...item,
        itemStyle: {
          borderRadius: [3, 3, 0, 0],
          color: brandColors[brand][isPositive ? 0 : 1]
        }
      }
    })
  }

  barChart.setOption(option)

  window.addEventListener('resize', () => {
    barChart.resize()
  })
}

const initLineChart = () => {
  const lineChart = echarts.init(lineChartRef.value, null, {
    renderer: 'svg'
  })
  
  const option = {
    title: {
      text: '各品牌每月评论数量趋势分析',
      textStyle: {
        fontSize: 16,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#ccc',
      borderWidth: 1,
      textStyle: {
        color: '#333'
      }
    },
    legend: {
      data: ["云鲸", "小米", "石头", "科沃斯", "追觅"],
      top: 25,
      textStyle: {
        fontSize: 12
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: 90,
      containLabel: true
    },
    toolbox: {
      feature: {
        saveAsImage: {
          title: '保存为图片'
        }
      },
      right: 20,
      top: 0
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: lineChartData.xAxis,
      axisLabel: {
        interval: 2,
        rotate: 45
      },
      axisLine: {
        lineStyle: {
          color: '#999'
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '评论数量',
      nameTextStyle: {
        padding: [0, 0, 0, 40]
      },
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: '#DDD'
        }
      },
      axisLine: {
        lineStyle: {
          color: '#999'
        }
      }
    },
    series: lineChartData.series.map(item => {
      const brandColors = {
        '云鲸': '#73c0de',
        '小米': '#fac858',
        '石头': '#91cc75',
        '科沃斯': '#5470c6',
        '追觅': '#9a60b4'
      }
      
      return {
        ...item,
        smooth: true,
        symbolSize: 6,
        lineStyle: {
          width: 2,
          color: brandColors[item.name]
        },
        itemStyle: {
          color: brandColors[item.name]
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: brandColors[item.name]
            },
            {
              offset: 1,
              color: 'rgba(255, 255, 255, 0.2)'
            }
          ]),
          opacity: 0.1
        }
      }
    })
  }

  lineChart.setOption(option)

  window.addEventListener('resize', () => {
    lineChart.resize()
  })
}
</script>

<style scoped>
.topics-analysis {
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.chart-row {
  flex: 1;
  margin-bottom: 20px;
}

.chart-row:last-child {
  margin-bottom: 0;
}

.chart-card {
  height: 100%;
}

.chart-container {
  height: 100%;
  min-height: 300px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.el-card__body) {
  height: calc(100% - 60px);
  padding: 20px !important;
}

:deep(.el-row) {
  margin: 0 !important;
}
</style>