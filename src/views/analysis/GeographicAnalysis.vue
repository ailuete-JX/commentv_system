<template>
  <div class="geographic-analysis">
    <el-card class="map-card">
      <div class="control-panel">
        <el-select v-model="selectedBrand" placeholder="选择品牌" class="brand-select">
          <el-option label="全部品牌" value="all" />
          <el-option label="科沃斯" value="science" />
          <el-option label="小米" value="xiaomi" />
          <el-option label="石头" value="roborock" />
          <el-option label="追觅" value="dreame" />
          <el-option label="云鲸" value="narwal" />
        </el-select>
      </div>
      <div ref="chartRef" class="map-container"></div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref(null)
const selectedBrand = ref('all')
let myChart = null
// 词云图
// 真实数据
const mockData = {
  all: [
  { "name": "安徽省", "value": 1348 },
  { "name": "北京市", "value": 2419 },
  { "name": "福建省", "value": 1684 },
  { "name": "甘肃省", "value": 331 },
  { "name": "广东省", "value": 6598 },
  { "name": "广西壮族自治区", "value": 758 },
  { "name": "贵州省", "value": 361 },
  { "name": "海南省", "value": 270 },
  { "name": "河北省", "value": 1329 },
  { "name": "河南省", "value": 1877 },
  { "name": "黑龙江省", "value": 425 },
  { "name": "湖北省", "value": 2019 },
  { "name": "湖南省", "value": 1235 },
  { "name": "吉林省", "value": 395 },
  { "name": "江苏省", "value": 3979 },
  { "name": "江西省", "value": 749 },
  { "name": "辽宁省", "value": 1262 },
  { "name": "内蒙古自治区", "value": 436 },
  { "name": "宁夏回族自治区", "value": 143 },
  { "name": "青海省", "value": 46 },
  { "name": "山东省", "value": 2675 },
  { "name": "山西省", "value": 615 },
  { "name": "陕西省", "value": 1311 },
  { "name": "上海市", "value": 2115 },
  { "name": "四川省", "value": 2903 },
  { "name": "天津市", "value": 927 },
  { "name": "西藏自治区", "value": 25 },
  { "name": "新疆维吾尔自治区", "value": 647 },
  { "name": "云南省", "value": 356 },
  { "name": "浙江省", "value": 2554 },
  { "name": "重庆市", "value": 958 },
  { "name": "港澳", "value": 35 },
  { "name": "海外", "value": 380 }
  ],
  science: [
  { name: '安徽省', value: 219 },
  { name: '北京市', value: 528 },
  { name: '福建省', value: 352 },
  { name: '甘肃省', value: 67 },
  { name: '广东省', value: 1177 },
  { name: '广西壮族自治区', value: 137 },
  { name: '贵州省', value: 76 },
  { name: '海南省', value: 69 },
  { name: '河北省', value: 243 },
  { name: '河南省', value: 239 },
  { name: '黑龙江省', value: 98 },
 {  name: '湖北省', value: 320 },
  { name: '湖南省', value: 205 },
  { name: '吉林省', value: 95 },
  { name: '江苏省', value: 818 },
  { name: '江西省', value: 139 },
  { name: '辽宁省', value: 322 },
  { name: '内蒙古自治区', value: 88 },
  { name: '宁夏回族自治区', value: 21 },
  { name: '青海省', value: 9 },
  { name: '山东省', value: 482 },
  { name: '山西省', value: 108 },
  { name: '陕西省', value: 224 },
  { name: '上海市', value: 472 },
  { name: '四川省', value: 506 },
  { name: '天津市', value: 185 },
  { name: '西藏自治区', value: 7 },
  { name: '新疆维吾尔自治区', value: 110 },
  { name: '云南省', value: 66 },
  { name: '浙江省', value: 493 },
  { name: '重庆市', value: 163 },
  { name: '港澳', value: 5 },
  { name: '海外', value: 53 }
  ],
  roborock: [
  { name: '安徽省', value: 294 },
{ name: '北京市', value: 435 },
{ name: '福建省', value: 362 },
{ name: '甘肃省', value: 72 },
{ name: '广东省', value: 1195 },
{ name: '广西壮族自治区', value: 138 },
{ name: '贵州省', value: 58 },
{ name: '海南省', value: 46 },
{ name: '河北省', value: 283 },
{ name: '河南省', value: 324 },
{ name: '黑龙江省', value: 86 },
{ name: '湖北省', value: 452 },
{ name: '湖南省', value: 293 },
{ name: '吉林省', value: 81 },
{ name: '江苏省', value: 850 },
{ name: '江西省', value: 167 },
{ name: '辽宁省', value: 210 },
{ name: '内蒙古自治区', value: 98 },
{ name: '宁夏回族自治区', value: 31 },
{ name: '青海省', value: 9 },
{ name: '山东省', value: 564 },
{ name: '山西省', value: 146 },
{ name: '陕西省', value: 291 },
{ name: '上海市', value: 355 },
{ name: '四川省', value: 514 },
{ name: '天津市', value: 188 },
{ name: '西藏自治区', value: 3 },
{ name: '新疆维吾尔自治区', value: 126 },
{ name: '云南省', value: 54 },
{ name: '浙江省', value: 551 },
{ name: '重庆市', value: 192 },
{ name: '港澳', value: 4 },
{ name: '海外', value: 86 }
  ],
  xiaomi: [
  { name: '安徽省', value: 307 },
{ name: '北京市', value: 461 },
{ name: '福建省', value: 292 },
{ name: '甘肃省', value: 67 },
{ name: '广东省', value: 1320 },
{ name: '广西壮族自治区', value: 174 },
{ name: '贵州省', value: 75 },
{ name: '海南省', value: 50 },
{ name: '河北省', value: 338 },
{ name: '河南省', value: 671 },
{ name: '黑龙江省', value: 84 },
{ name: '湖北省', value: 469 },
{ name: '湖南省', value: 215 },
{ name: '吉林省', value: 73 },
{ name: '江苏省', value: 812 },
{ name: '江西省', value: 169 },
{ name: '辽宁省', value: 259 },
{ name: '内蒙古自治区', value: 75 },
{ name: '宁夏回族自治区', value: 20 },
{ name: '青海省', value: 13 },
{ name: '山东省', value: 597 },
{ name: '山西省', value: 122 },
{ name: '陕西省', value: 251 },
{ name: '上海市', value: 383 },
{ name: '四川省', value: 613 },
{ name: '天津市', value: 198 },
{ name: '西藏自治区', value: 7 },
{ name: '新疆维吾尔自治区', value: 147 },
{ name: '云南省', value: 91 },
{ name: '浙江省', value: 433 },
{ name: '重庆市', value: 209 },
{ name: '港澳', value: 14 },
{ name: '海外', value: 61 }
  ],
  narwal: [
  { name: '安徽省', value: 324 },
{ name: '北京市', value: 464 },
{ name: '福建省', value: 337 },
{ name: '甘肃省', value: 52 },
{ name: '广东省', value: 1624 },
{ name: '广西壮族自治区', value: 176 },
{ name: '贵州省', value: 83 },
{ name: '海南省', value: 61 },
{ name: '河北省', value: 252 },
{ name: '河南省', value: 345 },
{ name: '黑龙江省', value: 64 },
{ name: '湖北省', value: 434 },
{ name: '湖南省', value: 287 },
{ name: '吉林省', value: 73 },
{ name: '江苏省', value: 726 },
{ name: '江西省', value: 158 },
{ name: '辽宁省', value: 229 },
{ name: '内蒙古自治区', value: 77 },
{ name: '宁夏回族自治区', value: 39 },
{ name: '青海省', value: 7 },
{ name: '山东省', value: 549 },
{ name: '山西省', value: 116 },
{ name: '陕西省', value: 296 },
{ name: '上海市', value: 470 },
{ name: '四川省', value: 668 },
{ name: '天津市', value: 181 },
{ name: '西藏自治区', value: 6 },
{ name: '新疆维吾尔自治区', value: 140 },
{ name: '云南省', value: 65 },
{ name: '浙江省', value: 586 },
{ name: '重庆市', value: 227 },
{ name: '港澳', value: 8 },
{ name: '海外', value: 94 }
  ],
  dreame: [
  { name: '安徽省', value: 204 },
{ name: '北京市', value: 531 },
{ name: '福建省', value: 341 },
{ name: '甘肃省', value: 73 },
{ name: '广东省', value: 1282 },
{ name: '广西壮族自治区', value: 133 },
{ name: '贵州省', value: 69 },
{ name: '海南省', value: 44 },
{ name: '河北省', value: 213 },
{ name: '河南省', value: 298 },
{ name: '黑龙江省', value: 93 },
{ name: '湖北省', value: 344 },
{ name: '湖南省', value: 235 },
{ name: '吉林省', value: 73 },
{ name: '江苏省', value: 773 },
{ name: '江西省', value: 116 },
{ name: '辽宁省', value: 242 },
{ name: '内蒙古自治区', value: 98 },
{ name: '宁夏回族自治区', value: 32 },
{ name: '青海省', value: 8 },
{ name: '山东省', value: 483 },
{ name: '山西省', value: 123 },
{ name: '陕西省', value: 249 },
{ name: '上海市', value: 435 },
{ name: '四川省', value: 602 },
{ name: '天津市', value: 175 },
{ name: '西藏自治区', value: 2 },
{ name: '新疆维吾尔自治区', value: 124 },
{ name: '云南省', value: 80 },
{ name: '浙江省', value: 491 },
{ name: '重庆市', value: 167 },
{ name: '港澳', value: 4 },
{ name: '海外', value: 86 }
  ]
}

const initChart = async () => {
  if (!chartRef.value) return
  
  if (myChart) {
    myChart.dispose()
  }

  myChart = echarts.init(chartRef.value)
  myChart.showLoading()

  try {
    const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
    const chinaJson = await response.json()

    echarts.registerMap('china', chinaJson)
    
    const option = {
      backgroundColor: '#FFFFFF',
      tooltip: {
        trigger: 'item',
        formatter: '{b}<br/>评论数量：{c}'
      },
      visualMap: {
        min: 0,
        max: 2500,
        text: ['高', '低'],
        realtime: true,
        calculable: true,
        inRange: {
          color: ['#e0f3f8', '#2171c1']
        },
        textStyle: {
          color: '#666'
        },
        left: 'left',
        top: 'bottom'
      },
      series: [
        {
          name: '评论分布',
          type: 'map',
          map: 'china',
          roam: true,
          zoom: 1.2,
          center: [105, 36],
          label: {
            show: true,
            fontSize: 10
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 12,
              color: '#333'
            },
            itemStyle: {
              areaColor: '#0c91ff'
            }
          },
          data: mockData[selectedBrand.value]
        }
      ]
    }

    myChart.hideLoading()
    myChart.setOption(option)
  } catch (error) {
    console.error('Failed to load map:', error)
    myChart.hideLoading()
  }
}

const updateChart = () => {
  if (!myChart) return
  
  myChart.setOption({
    series: [{
      data: mockData[selectedBrand.value]
    }]
  })
}

watch(selectedBrand, () => {
  updateChart()
})

const handleResize = () => {
  myChart?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  if (myChart) {
    myChart.dispose()
    myChart = null
  }
})
</script>

<style scoped>
.geographic-analysis {
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.map-card {
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
}

.control-panel {
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
  background-color: #fff;
  z-index: 1;
}

.brand-select {
  width: 160px;
}

.map-container {
  flex: 1;
  min-height: 500px;
}

:deep(.el-card__body) {
  height: calc(100% - 60px);
  padding: 0 !important;
  display: flex;
  flex-direction: column;
}
</style>