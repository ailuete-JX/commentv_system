<template>
  <div class="optimization-suggestion">
    <h2>产品优化建议</h2>
    <div class="chat-container">
      <!-- 对话内容区域 -->
      <div class="messages-container" ref="messagesContainer">
        <div v-if="messages.length === 0" class="empty-state">
          在左侧输入您的使用体验，点击分析获取优化建议
        </div>
        <div v-else class="message-list">
          <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.type]">
            <div class="message-content">
              <div class="message-header">
                <span class="sender">{{ msg.type === 'user' ? '用户评论' : '优化建议' }}</span>
                <span class="time">{{ msg.time }}</span>
              </div>
              <div class="message-body" v-html="msg.content"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area-fixed">
        <div class="input-container">
          <el-input
            v-model="userComment"
            type="textarea"
            :rows="4"
            placeholder="请输入您的使用体验和建议..."
            :maxlength="500"
            show-word-limit
          />
          <el-button 
            type="primary" 
            @click="getOptimizationSuggestion"
            :loading="loading"
            :disabled="!userComment.trim()"
          >
            获取优化建议
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'

const userComment = ref('')
const suggestion = ref('')
const loading = ref(false)
const messages = ref([])
const messagesContainer = ref(null)

// 格式化时间
function formatTime() {
  const now = new Date()
  return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
}

// 添加消息到对话列表
function addMessage(content, type = 'user') {
  messages.value.push({
    content: type === 'user' ? content : content.replace(/\n/g, '<br>'),
    type,
    time: formatTime()
  })
  // 滚动到底部
  setTimeout(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  }, 100)
}

async function getOptimizationSuggestion() {
  if (!userComment.value.trim()) {
    ElMessage.warning('请先输入您的使用体验')
    return
  }

  // 添加用户消息
  addMessage(userComment.value, 'user')
  
  loading.value = true
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

    if (!navigator.onLine) {
      throw new Error('网络连接已断开，请检查您的网络设置')
    }

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
    if (data.error) {
      throw new Error(data.error)
    }
    
    if (!data.suggestion) {
      throw new Error('未收到有效的优化建议')
    }

    // 添加系统回复
    addMessage(data.suggestion, 'system')
    userComment.value = '' // 清空输入框
    ElMessage.success('优化建议生成成功')
  } catch (error) {
    console.error('获取优化建议失败:', error)
    let errorMessage = error.message || '获取优化建议失败，请稍后重试'
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.optimization-suggestion {
  height: calc(100vh - 100px);
  display: flex;
  flex-direction: column;
  padding: 0 20px 0 20px;
}

h2 {
  margin: 0 0 0px 0; /* 标题下方间距为0 */
  font-size: 18px;
  color: #303133;
  height: 24px;
  line-height: 24px;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  height: 100%;
  position: relative;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px 60px 20px; /* 底部留出输入区域空间 */
  background-color: #fff;
  min-height: 200px; /* 确保内容区域有最小高度 */
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 16px;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  display: flex;
  margin-bottom: 20px;
  width: 100%; /* 添加宽度 */
}

.message.user {
  justify-content: flex-end;
}

.message.system {
  justify-content: flex-start; /* 添加系统消息左对齐 */
}

.message-content {
  max-width: 85%; /* 增加最大宽度，让内容更宽一些 */
  padding: 12px 16px; /* 增加水平内边距 */
  border-radius: 8px;
  background-color: #f4f4f5;
}

.message.user .message-content {
  background-color: #ecf5ff;
}

.message.system .message-content {
  background-color: #f4f4f5;
  text-align: left; /* 确保系统消息文本左对齐 */
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
  color: #909399;
  padding-bottom: 4px; /* 添加一点底部间距 */
  border-bottom: 1px solid #ebeef5; /* 添加一条分隔线 */
}

.message-body {
  color: #303133;
  line-height: 1.6;
  text-align: left; /* 确保消息内容始终左对齐 */
  white-space: pre-wrap; /* 保留换行和空格 */
}

.input-area-fixed {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  background: #fff;
  border-top: 1px solid #ebeef5;
  padding: 4px 12px;
  z-index: 2;
}

.input-container {
  display: flex;
  gap: 4px; /* 进一步缩小输入框和按钮之间的间距 */
  align-items: flex-start;
}

.input-container .el-input {
  flex: 1;
}

.input-container .el-button {
  margin-top: 2px; /* 进一步缩小按钮顶部间距 */
  height: 28px; /* 进一步缩小按钮高度 */
  padding: 0 10px; /* 进一步缩小按钮左右内边距 */
}

/* 滚动条样式 */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-thumb {
  background-color: #dcdfe6;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-track {
  background-color: #f4f4f5;
}
</style>
