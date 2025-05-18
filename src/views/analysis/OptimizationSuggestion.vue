<template>
  <div class="optimization-suggestion">
    <h2>产品优化建议</h2>
    <div class="input-section">
      <el-input
        v-model="userComment"
        type="textarea"
        :rows="4"
        placeholder="请输入您的使用体验和建议..."
        :maxlength="500"
        show-word-limit
      />
      <div class="button-container">
        <el-button 
          type="primary" 
          @click="getOptimizationSuggestion"
          :loading="loading"
        >
          获取优化建议
        </el-button>
      </div>
    </div>

    <div v-if="suggestion" class="suggestion-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>优化建议分析结果</span>
          </div>
        </template>
        <div class="suggestion-content" v-html="formattedSuggestion"></div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

const userComment = ref('')
const suggestion = ref('')
const loading = ref(false)

const formattedSuggestion = computed(() => {
  if (!suggestion.value) return ''
  return suggestion.value.replace(/\n/g, '<br>')
})

async function getOptimizationSuggestion() {
  if (!userComment.value.trim()) {
    ElMessage.warning('请先输入您的使用体验')
    return
  }

  loading.value = true
  suggestion.value = '' // 清空之前的建议

  try {
    const response = await fetch('/api/get_optimization_suggestion', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        comment: userComment.value
      })
    })

    // 检查网络连接
    if (!navigator.onLine) {
      throw new Error('网络连接已断开，请检查您的网络设置')
    }

    // 检查响应状态
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('API 端点未找到，请确保后端服务正在运行')
      } else if (response.status === 500) {
        throw new Error('服务器内部错误')
      } else {
        throw new Error(`请求失败: ${response.status}`)
      }
    }

    const data = await response.json()
    
    // 检查 API 返回的错误
    if (data.error) {
      throw new Error(data.error)
    }
    
    if (!data.suggestion) {
      throw new Error('未收到有效的优化建议')
    }

    suggestion.value = data.suggestion
    ElMessage.success('优化建议生成成功')
  } catch (error) {
    console.error('获取优化建议失败:', error)
    
    // 根据错误类型显示不同的错误消息
    let errorMessage
    if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
      errorMessage = '无法连接到服务器，请确保后端服务正在运行'
    } else if (error.message.includes('网络连接已断开')) {
      errorMessage = error.message
    } else {
      errorMessage = error.message || '获取优化建议失败，请稍后重试'
    }
    
    ElMessage.error(errorMessage)
    suggestion.value = ''
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.optimization-suggestion {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.input-section {
  margin: 20px 0;
}

.button-container {
  margin-top: 15px;
  display: flex;
  justify-content: flex-start;
}

.suggestion-section {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.suggestion-content {
  white-space: pre-line;
  line-height: 1.6;
  text-align: left;
  padding: 10px;
}
</style>
