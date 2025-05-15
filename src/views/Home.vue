<template>
  <div class="home-container">
    <!-- 顶部数据概览区域 -->
    <div class="overview-section">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="overview-card" shadow="hover">
            <div class="overview-item">
              <el-icon class="overview-icon blue-theme"><ChatLineSquare /></el-icon>
              <div class="overview-content">
                <div class="overview-value">55199</div>
                <div class="overview-label">总评论数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="overview-card" shadow="hover">
            <div class="overview-item">
              <el-icon class="overview-icon green-theme"><Shop /></el-icon>
              <div class="overview-content">
                <div class="overview-value">5</div>
                <div class="overview-label">主要品牌数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="overview-card" shadow="hover">
            <div class="overview-item">
              <el-icon class="overview-icon orange-theme"><Star /></el-icon>
              <div class="overview-content">
                <div class="overview-value">4.51</div>
                <div class="overview-label">平均评分</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 图表展示区域 -->
    <div class="charts-section">
      <el-row :gutter="20" class="chart-row">
        <el-col :span="12">
          <el-card class="chart-card" shadow="hover">
            <div class="chart-header">品牌评论分布</div>
            <div class="chart-wrapper">
              <div ref="brandRoseRef" class="chart-container"></div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="chart-card" shadow="hover">
            <div class="chart-header">评分占比分布</div>
            <div class="chart-wrapper">
              <div ref="ratingPieRef" class="chart-container"></div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import { ChatLineSquare, Shop, Star } from '@element-plus/icons-vue'

const brandRoseRef = ref(null)
const ratingPieRef = ref(null)
let charts = []

const initCharts = () => {
  // 清除现有图表
  charts.forEach(chart => chart?.dispose())
  charts = []

  // 初始化品牌分布玫瑰图
  if (brandRoseRef.value) {
    const brandChart = echarts.init(brandRoseRef.value)
    charts.push(brandChart)
    brandChart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}条评论 ({d}%)'
      },
      legend: {
        top: '85%',
        left: 'center'
      },
      series: [
        {
          name: '品牌评论',
          type: 'pie',
          radius: ['20%', '65%'],
          center: ['50%', '45%'],
          roseType: 'area',
          itemStyle: {
            borderRadius: 8,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            position: 'outside',
            formatter: '{b}\n{c}条'
          },
          data: [
            { value: 11931, name: '科沃斯', itemStyle: { color: '#91cc75' } },
            { value: 12132, name: '小米', itemStyle: { color: '#fac858' } },
            { value: 12781, name: '石头', itemStyle: { color: '#ee6666' } },
            { value: 8747, name: '追觅', itemStyle: { color: '#73c0de' } },
            { value: 9608, name: '云鲸', itemStyle: { color: '#3ba272' } },
          ]
        }
      ]
    })
  }

  // 初始化评分分布饼图
  if (ratingPieRef.value) {
    const ratingChart = echarts.init(ratingPieRef.value)
    charts.push(ratingChart)
    ratingChart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}%'
      },
      legend: {
        orient: 'vertical',
        right: '5%',
        top: 'middle',
        itemWidth: 10,
        itemHeight: 10
      },      series: [
        {
          name: '评分占比',
          type: 'pie',
          radius: ['35%', '60%'],
          center: ['40%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            position: 'outside',
            formatter: '{b}\n{c}条\n{d}%',
            textStyle: {
              fontSize: 12
            }
          },
          labelLine: {
            show: true,
            length: 15,
            length2: 15,
            smooth: true
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 14,
              fontWeight: 'bold'
            }
          },
          data: [
            { value: 36856, name: '5星', itemStyle: { color: '#67C23A' } },
            { value: 266, name: '4星', itemStyle: { color: '#95d475' } },
            { value: 1306, name: '3星', itemStyle: { color: '#e6a23c' } },
            { value: 688, name: '2星', itemStyle: { color: '#f56c6c' } },
            { value: 4052, name: '1星', itemStyle: { color: '#909399' } }
          ]
        }
      ]
    })
  }
}

const handleResize = () => {
  charts.forEach(chart => chart?.resize())
}

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  charts.forEach(chart => chart?.dispose())
  charts = []
})
</script>

<style scoped>
.home-container {
  height: 100%;
  padding: 16px;
  box-sizing: border-box;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.overview-section {
  flex: 0 0 auto;
  margin-bottom: 8px;
}

.overview-card {
  height: 100px;
  transition: all 0.3s;
}

.overview-card:hover {
  transform: translateY(-2px);
}

.overview-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  height: 100%;
}

.overview-icon {
  font-size: 32px;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.blue-theme {
  color: #409EFF;
  background-color: rgba(64, 158, 255, 0.1);
}

.green-theme {
  color: #67C23A;
  background-color: rgba(103, 194, 58, 0.1);
}

.orange-theme {
  color: #E6A23C;
  background-color: rgba(230, 162, 60, 0.1);
}

.overview-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.overview-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
}

.overview-label {
  font-size: 14px;
  color: #909399;
}

.charts-section {
  flex: 1;
  display: flex;
  margin-top: 16px;
}

.chart-row {
  flex: 1;
  margin: 0 !important;
}

.chart-card {
  height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
}

.chart-header {
  padding: 12px 16px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  border-bottom: 1px solid #ebeef5;
}

.chart-wrapper {
  flex: 1;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
}

:deep(.el-card) {
  height: 100%;
}

:deep(.el-card__body) {
  height: 100%;
  padding: 0 !important;
  display: flex;
  flex-direction: column;
}

:deep(.el-col) {
  height: 100%;
}
</style>