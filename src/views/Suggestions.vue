<template>
  <div class="suggestions">
    <h2>智能改进建议</h2>
    <el-row :gutter="20">
      <el-col :span="8" v-for="(category, index) in categories" :key="index">
        <el-card class="summary-card">
          <template #header>
            <div class="card-header">
              <el-icon>
                <component :is="category.icon"></component>
              </el-icon>
              <span>{{ category.name }}</span>
            </div>
          </template>
          <div class="summary-content">
            <div class="summary-number">{{ category.count }}</div>
            <div class="summary-text">{{ category.description }}</div>
            <el-progress 
              :percentage="category.percentage" 
              :color="category.color"
              :status="category.status"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="suggestions-card">
      <template #header>
        <div class="card-header">
          <span>详细改进建议</span>
          <el-radio-group v-model="currentPriority" size="small">
            <el-radio-button label="high">高优先级</el-radio-button>
            <el-radio-button label="medium">中优先级</el-radio-button>
            <el-radio-button label="low">低优先级</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      
      <el-timeline>
        <el-timeline-item
          v-for="item in filteredSuggestions"
          :key="item.id"
          :type="item.type"
          :color="item.color"
          :timestamp="item.timestamp"
          placement="top"
        >
          <el-card class="suggestion-item">
            <template #header>
              <div class="suggestion-header">
                <h3>{{ item.title }}</h3>
                <el-tag :type="item.tagType">{{ item.priority }}</el-tag>
              </div>
            </template>
            <div class="suggestion-content">
              <h4>问题描述：</h4>
              <p>{{ item.problem }}</p>
              <h4>改进建议：</h4>
              <p>{{ item.suggestion }}</p>
              <h4>预期效果：</h4>
              <p>{{ item.expected }}</p>
              <div class="suggestion-stats">
                <el-tag size="small">关联评论: {{ item.relatedComments }}</el-tag>
                <el-tag size="small" type="success">支持率: {{ item.supportRate }}</el-tag>
              </div>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  Warning,
  Lightning,
  Operation
} from '@element-plus/icons-vue'

const currentPriority = ref('high')

const categories = [
  {
    name: '亟待改进',
    icon: 'Warning',
    count: 5,
    description: '需要立即处理的问题',
    percentage: 70,
    color: '#F56C6C',
    status: 'exception'
  },
  {
    name: '建议优化',
    icon: 'Lightning',
    count: 8,
    description: '可以提升用户体验',
    percentage: 45,
    color: '#E6A23C',
    status: 'warning'
  },
  {
    name: '长期规划',
    icon: 'Operation',
    count: 6,
    description: '未来发展方向',
    percentage: 30,
    color: '#409EFF',
    status: ''
  }
]

const suggestions = [
  {
    id: 1,
    title: '降低工作噪音',
    priority: '高优先级',
    type: 'danger',
    color: '#F56C6C',
    tagType: 'danger',
    timestamp: '2025-05-03',
    problem: '根据用户反馈，当前机型在工作时噪音较大，特别是在夜间使用时会影响休息。',
    suggestion: '1. 优化电机设计，采用低噪音电机\n2. 改进隔音材料\n3. 添加智能降噪模式',
    expected: '降低工作噪音至45分贝以下，提升用户夜间使用体验。',
    relatedComments: 526,
    supportRate: '85%'
  },
  {
    id: 2,
    title: '提升电池续航能力',
    priority: '高优先级',
    type: 'danger',
    color: '#F56C6C',
    tagType: 'danger',
    timestamp: '2025-05-03',
    problem: '大户型清扫时常需要中途充电，影响清扫效率。',
    suggestion: '1. 升级电池容量\n2. 优化能源管理系统\n3. 添加快速充电功能',
    expected: '单次充电可完成150平米以上区域的清扫。',
    relatedComments: 485,
    supportRate: '82%'
  },
  {
    id: 3,
    title: '优化导航算法',
    priority: '中优先级',
    type: 'warning',
    color: '#E6A23C',
    tagType: 'warning',
    timestamp: '2025-05-03',
    problem: '在复杂环境下容易迷路，清扫路线不够优化。',
    suggestion: '1. 升级SLAM算法\n2. 增加深度学习模型\n3. 改进传感器配置',
    expected: '提高复杂环境下的清扫效率，减少重复清扫。',
    relatedComments: 342,
    supportRate: '75%'
  },
  {
    id: 4,
    title: '增强防缠绕能力',
    priority: '中优先级',
    type: 'warning',
    color: '#E6A23C',
    tagType: 'warning',
    timestamp: '2025-05-03',
    problem: '清扫过程中容易被电线、衣物等缠绕。',
    suggestion: '1. 改进滚刷设计\n2. 添加防缠绕传感器\n3. 优化脱困算法',
    expected: '减少90%的缠绕情况，提高清扫可靠性。',
    relatedComments: 289,
    supportRate: '73%'
  },
  {
    id: 5,
    title: '添加远程控制功能',
    priority: '低优先级',
    type: 'info',
    color: '#909399',
    tagType: 'info',
    timestamp: '2025-05-03',
    problem: '用户希望能够远程控制和监控清扫状态。',
    suggestion: '1. 开发手机APP\n2. 添加摄像头模块\n3. 支持语音控制',
    expected: '实现远程控制和实时监控功能，提升用户便利性。',
    relatedComments: 156,
    supportRate: '68%'
  }
]

const filteredSuggestions = computed(() => {
  const priorityMap = {
    high: '高优先级',
    medium: '中优先级',
    low: '低优先级'
  }
  return suggestions.filter(item => item.priority === priorityMap[currentPriority.value])
})
</script>

<style scoped>
.suggestions {
  padding: 20px;
}

.summary-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.summary-content {
  text-align: center;
  padding: 20px 0;
}

.summary-number {
  font-size: 36px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}

.summary-text {
  color: #606266;
  margin-bottom: 15px;
}

.suggestions-card {
  margin-top: 20px;
}

.suggestion-item {
  margin-bottom: 20px;
}

.suggestion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.suggestion-header h3 {
  margin: 0;
}

.suggestion-content {
  h4 {
    color: #606266;
    margin: 15px 0 5px 0;
  }

  p {
    margin: 0;
    color: #303133;
    line-height: 1.6;
  }
}

.suggestion-stats {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}
</style>