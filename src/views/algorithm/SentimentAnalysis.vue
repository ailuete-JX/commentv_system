<template>
  <div class="sentiment-analysis-usage">
    <h2 class="page-title">情感分析</h2>
    
    <el-card class="input-card">
      <template #header>
        <div class="card-header">
          <h3>单条评论分析</h3>
        </div>
      </template>
      <el-input
        v-model="singleComment"
        type="textarea"
        :rows="4"
        placeholder="请输入要分析的评论内容..."
      />
      <div class="button-container">
        <el-button type="primary" @click="analyzeSingleComment" :loading="singleAnalyzing">
          分析
        </el-button>
      </div>
      
      <div v-if="singleResult" class="result-container">
        <el-descriptions border>
          <el-descriptions-item label="情感倾向" :span="2">
            <el-tag :type="getSentimentType(singleResult.sentiment)">
              {{ getSentimentText(singleResult.sentiment) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="置信度" :span="2">
            {{ (singleResult.confidence * 100).toFixed(2) }}%
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>

    <el-card class="batch-card">
      <template #header>
        <div class="card-header">
          <h3>批量评论分析</h3>
        </div>
      </template>
      <div class="upload-container">
        <el-upload
          class="upload-excel"
          accept=".xlsx"
          :auto-upload="false"
          :on-change="handleFileChange"
          :show-file-list="true"
          :limit="1"
        >
          <template #trigger>
            <el-button type="primary">选择文件</el-button>
          </template>
          <el-button 
            type="success" 
            @click="analyzeBatchComments" 
            :disabled="!excelFile"
            :loading="batchAnalyzing"
          >
            开始分析
          </el-button>
        </el-upload>
        <div class="file-info" v-if="excelFile">
          已选择文件: {{ excelFile.name }}
        </div>
      </div>

      <div v-if="batchResults.length > 0" class="batch-results">
        <div class="table-operations">
          <el-button type="success" @click="exportToExcel">
            导出为Excel
          </el-button>
        </div>
        
        <el-table
          :data="batchResults"
          style="width: 100%"
          border
          stripe
          height="400"
        >
          <el-table-column prop="comment" label="评论内容" min-width="300" show-overflow-tooltip />
          <el-table-column prop="sentiment" label="情感倾向" width="120">
            <template #default="scope">
              <el-tag :type="getSentimentType(scope.row.sentiment)">
                {{ getSentimentText(scope.row.sentiment) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="confidence" label="置信度" width="120">
            <template #default="scope">
              {{ (scope.row.confidence * 100).toFixed(2) }}%
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as XLSX from 'xlsx'
import { ElMessage } from 'element-plus'

const router = useRouter()
const singleComment = ref('')
const singleResult = ref(null)
const singleAnalyzing = ref(false)
const batchAnalyzing = ref(false)
const excelFile = ref(null)
const batchResults = ref([])

// API基础URL配置
const API_BASE_URL = 'http://localhost:5000'

// API请求函数封装
const fetchWithRetry = async (url, options = {}, maxRetries = 3) => {
  let lastError = null
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), options.timeout || 10000)
      
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          ...options.headers
        },
        mode: 'cors'  // 显式启用CORS
      })
      
      clearTimeout(timeoutId)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      return data
      
    } catch (error) {
      console.error(`第${i + 1}次请求失败:`, error)
      lastError = error
      
      if (error.name === 'AbortError') {
        throw new Error('请求超时，请检查服务器是否正在运行')
      }
      
      // 如果不是最后一次重试，则等待后继续
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)))
        continue
      }
    }
  }
  
  throw new Error(`多次请求失败: ${lastError?.message || '未知错误'}`)
}

// 页面加载时预先获取token
onMounted(async () => {
  try {
    const token = await getAccessToken()
    if (token) {
      console.log('成功预获取access_token')
    }
  } catch (error) {
    console.error('预获取token失败:', error)
  }
})

// 获取access_token的函数
const getAccessToken = async () => {
  try {
    console.log('开始请求access token')
    const data = await fetchWithRetry(`${API_BASE_URL}/api/token`, {
      method: 'GET',
      timeout: 15000
    })
    
    if (!data.access_token) {
      throw new Error('返回数据中没有access_token')
    }
    
    console.log('成功获取access token')
    return data.access_token
    
  } catch (error) {
    console.error('获取token失败:', error)
    ElMessage.error(error.message)
    throw error
  }
}

// 情感分析函数
const analyzeSentiment = async (text, access_token) => {
  try {
    console.log('开始发送情感分析请求')
    const data = await fetchWithRetry(`${API_BASE_URL}/api/sentiment`, {
      method: 'POST',
      body: JSON.stringify({ text, access_token }),
      timeout: 20000
    })
    
    if (!data.items || data.items.length === 0) {
      throw new Error('分析结果为空')
    }
    
    console.log('成功获取情感分析结果')
    return data.items[0]
    
  } catch (error) {
    console.error('情感分析失败:', error)
    ElMessage.error(error.message)
    throw error
  }
}

// 分析单条评论
const analyzeSingleComment = async () => {
  if (!singleComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  singleAnalyzing.value = true
  
  try {
    const access_token = await getAccessToken()
    if (!access_token) {
      throw new Error('无法获取访问令牌')
    }
    
    const result = await analyzeSentiment(singleComment.value, access_token)
    if (result) {
      singleResult.value = result
      ElMessage.success('分析完成')
    }
  } catch (error) {
    console.error('分析失败:', error)
    ElMessage.error(`分析失败: ${error.message}`)
  } finally {
    singleAnalyzing.value = false
  }
}

// 处理文件选择
const handleFileChange = (file) => {
  excelFile.value = file.raw
}

// 批量分析评论
const analyzeBatchComments = async () => {
  if (!excelFile.value) {
    ElMessage.warning('请先选择Excel文件')
    return
  }

  batchAnalyzing.value = true
  batchResults.value = []
  
  try {
    const reader = new FileReader()
    reader.onload = async (e) => {
      const data = new Uint8Array(e.target.result)
      const workbook = XLSX.read(data, { type: 'array' })
      const sheetName = workbook.SheetNames[0]
      const worksheet = workbook.Sheets[sheetName]
      const jsonData = XLSX.utils.sheet_to_json(worksheet)

      if (!jsonData.length || !jsonData[0].hasOwnProperty('评论内容')) {
        ElMessage.error('Excel文件格式不正确，请确保包含"评论内容"列')
        batchAnalyzing.value = false
        return
      }

      const access_token = await getAccessToken()
      if (!access_token) {
        batchAnalyzing.value = false
        return
      }

      for (const row of jsonData) {
        const comment = row['评论内容']
        if (comment) {
          const result = await analyzeSentiment(comment, access_token)
          if (result) {
            batchResults.value.push({
              comment,
              ...result
            })
          }
          // 添加延迟以避免API限制
          await new Promise(resolve => setTimeout(resolve, 100))
        }
      }

      ElMessage.success('批量分析完成')
    }
    reader.readAsArrayBuffer(excelFile.value)
  } catch (error) {
    console.error('批量分析失败:', error)
    ElMessage.error('批量分析失败，请检查文件格式')
  } finally {
    batchAnalyzing.value = false
  }
}

// 导出为Excel
const exportToExcel = () => {
  if (batchResults.value.length === 0) {
    ElMessage.warning('没有可导出的数据')
    return
  }

  const worksheet = XLSX.utils.json_to_sheet(
    batchResults.value.map(item => ({
      '评论内容': item.comment,
      '情感倾向': getSentimentText(item.sentiment),
      '置信度': `${(item.confidence * 100).toFixed(2)}%`
    }))
  )

  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, '情感分析结果')
  
  // 生成Excel文件并下载
  XLSX.writeFile(workbook, '情感分析结果.xlsx')
}

// 获取情感类型
const getSentimentType = (sentiment) => {
  const types = {
    0: 'danger',   // 负向
    1: 'warning',  // 中性
    2: 'success'   // 正向
  }
  return types[sentiment] || 'info'
}

// 获取情感文本
const getSentimentText = (sentiment) => {
  const texts = {
    0: '负向',
    1: '中性',
    2: '正向'
  }
  return texts[sentiment] || '未知'
}
</script>

<style scoped>
.sentiment-analysis-usage {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: calc(100vh - 84px);
  overflow-y: auto;
  background-color: #f5f7fa;
}

.page-title {
  margin: 0 0 20px 0;
  color: #303133;
  font-size: 24px;
}

.input-card, .batch-card {
  background-color: #fff;
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.button-container {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.result-container {
  margin-top: 20px;
}

.upload-container {
  padding: 20px 0;
}

.file-info {
  margin-top: 10px;
  color: #606266;
}

.batch-results {
  margin-top: 20px;
}

.table-operations {
  margin-bottom: 16px;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-descriptions) {
  margin-top: 16px;
}

:deep(.el-descriptions__cell) {
  padding: 12px 20px;
}

:deep(.el-upload-list) {
  margin-top: 10px;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style>