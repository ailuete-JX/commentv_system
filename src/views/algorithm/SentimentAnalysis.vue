<template>
  <div class="sentiment-analysis-usage">
    <!-- 分析模式选择器 -->
    <div class="mode-selector">
      <el-radio-group v-model="analysisMode" size="large">
        <el-radio-button label="single">单条评论分析</el-radio-button>
        <el-radio-button label="batch">批量评论分析</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 单条评论分析 -->
    <el-card v-if="analysisMode === 'single'" class="input-card">
      <el-input
        v-model="singleComment"
        type="textarea"
        :rows="4"
        placeholder="请输入需要分析的评论文本"
      />
      <div class="button-container">
        <el-button type="primary" @click="analyzeSingleComment" :loading="singleAnalyzing">
          分析
        </el-button>
      </div>

      <!-- 单条评论分析结果 -->
      <div v-if="singleResult" class="result-container">
        <el-row>
          <el-col :span="24">
            <el-descriptions title="情感倾向分析结果" :column="1" border>
              <el-descriptions-item label="情感类别">
                <el-tag :type="getSentimentType(singleResult.sentiment)">
                  {{ getSentimentText(singleResult.sentiment) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="置信度">
                <el-progress 
                  :percentage="Math.round(singleResult.confidence * 100)"
                  :color="getConfidenceColor(singleResult.confidence)"
                />
              </el-descriptions-item>
            </el-descriptions>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 批量评论分析 -->
    <el-card v-if="analysisMode === 'batch'" class="batch-card">
      <div class="batch-header">
        <div class="upload-section">
          <el-upload
            class="upload-demo"
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :show-file-list="true"
            accept=".xlsx,.xls"
          >
            <el-button type="primary">选择文件</el-button>
          </el-upload>
        </div>
        
        <div class="file-info-section">
          <div class="file-info">支持 .xlsx, .xls 格式文件，文件大小不超过 10MB</div>
          <div class="file-list" v-if="excelFile">
            当前文件：{{ excelFile.name }}
          </div>
        </div>
        
        <div class="action-section">
          <el-button 
            type="success" 
            :loading="batchAnalyzing" 
            @click="analyzeBatchComments"
            v-if="excelFile"
          >
            开始分析
          </el-button>
        </div>
      </div>

      <!-- 结果展示区域 -->
      <div class="batch-content">
        <div class="results-header" v-if="batchResults.length">
          <div class="results-title">分析结果</div>
          <el-button type="success" @click="exportToExcel">导出结果</el-button>
        </div>
        
        <div class="results-container" v-if="batchResults.length">
          <el-table :data="batchResults" style="width: 100%" border>
            <el-table-column prop="comment" label="评论内容" min-width="200" show-overflow-tooltip />
            <el-table-column prop="sentiment" label="情感倾向" width="100">
              <template #default="scope">
                <el-tag :type="getSentimentType(scope.row.sentiment)">
                  {{ getSentimentText(scope.row.sentiment) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="confidence" label="置信度" width="120">
              <template #default="scope">
                <el-progress 
                  :percentage="Math.round(scope.row.confidence * 100)"
                  :color="getConfidenceColor(scope.row.confidence)"
                />
              </template>
            </el-table-column>
          </el-table>
        </div>
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

// 添加分析模式选择
const analysisMode = ref('single')

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
    const response = await fetchWithRetry(`${API_BASE_URL}/api/sentiment`, {
      method: 'POST',
      body: JSON.stringify({ text, access_token }),
      timeout: 20000
    })
    
    if (!response.items || response.items.length === 0) {
      throw new Error('分析结果为空')
    }
    
    const result = response.items[0]
    console.log('情感分析结果:', result)  // 添加日志输出
    
    // 确保返回正确的数据结构
    return {
      sentiment: result.sentiment,
      confidence: result.confidence || result.sentiment_prob || 0,  // 使用实际的置信度值
      keywords: result.keywords || []
    }
    
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
const handleFileChange = (uploadFile) => {
  if (uploadFile) {
    // 验证文件大小（10MB限制）
    const maxSize = 10 * 1024 * 1024 // 10MB
    if (uploadFile.raw.size > maxSize) {
      ElMessage.error('文件大小不能超过10MB')
      return false
    }
    
    // 验证文件类型
    const validTypes = [
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/vnd.ms-excel'
    ]
    if (!validTypes.includes(uploadFile.raw.type)) {
      ElMessage.error('只支持.xlsx和.xls格式的Excel文件')
      return false
    }
    
    excelFile.value = uploadFile.raw
    ElMessage.success('文件已选择，点击"开始分析"按钮进行分析')
    return true
  }
  return false
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
      try {
        const data = new Uint8Array(e.target.result)
        const workbook = XLSX.read(data, { type: 'array' })
        const sheetName = workbook.SheetNames[0]
        const worksheet = workbook.Sheets[sheetName]
        const jsonData = XLSX.utils.sheet_to_json(worksheet)

        if (!jsonData.length || !jsonData[0].hasOwnProperty('评论内容')) {
          throw new Error('Excel文件格式不正确，请确保包含"评论内容"列')
        }

        const access_token = await getAccessToken()
        if (!access_token) {
          throw new Error('无法获取访问令牌')
        }

        const total = jsonData.length
        let completed = 0

        for (const row of jsonData) {
          const comment = row['评论内容']
          if (comment) {
            try {
              const result = await analyzeSentiment(comment, access_token)
              if (result) {
                batchResults.value.push({
                  comment,
                  ...result
                })
              }
              completed++
              // 更新进度提示
              if (completed % 5 === 0) {
                ElMessage.info(`已处理 ${completed}/${total} 条评论`)
              }
            } catch (error) {
              console.error(`分析评论失败: ${comment}`, error)
              continue
            }
            // 添加延迟以避免API限制
            await new Promise(resolve => setTimeout(resolve, 100))
          }
        }
        ElMessage.success(`批量分析完成，共处理 ${completed} 条评论`)
      } catch (error) {
        ElMessage.error(error.message)
        console.error('处理Excel数据失败:', error)
      }
    }
    
    reader.onerror = (error) => {
      ElMessage.error('读取文件失败')
      console.error('读取文件失败:', error)
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
  try {
    if (batchResults.value.length === 0) {
      ElMessage.warning('没有可导出的数据')
      return
    }

    // 构建导出数据
    const exportData = batchResults.value.map(item => ({
      '评论内容': item.comment,
      '情感倾向': getSentimentText(item.sentiment),
      '置信度': `${Math.round(item.confidence * 100)}%`
    }))

    // 创建工作表
    const worksheet = XLSX.utils.json_to_sheet(exportData)

    // 设置列宽
    const colWidths = {
      A: { wch: 50 },  // 评论内容列宽
      B: { wch: 10 },  // 情感倾向列宽
      C: { wch: 10 }   // 置信度列宽
    }
    worksheet['!cols'] = [
      { wch: 50 }, // A
      { wch: 10 }, // B
      { wch: 10 }  // C
    ]

    // 创建工作簿
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, '情感分析结果')

    // 生成文件名（包含时间戳）
    const timestamp = new Date().toLocaleString().replace(/[/:]/g, '-')
    const fileName = `情感分析结果_${timestamp}.xlsx`

    // 导出文件
    XLSX.writeFile(workbook, fileName)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败，请重试')
  }
}

// 获取情感类型
const getSentimentType = (sentiment) => {
  const types = {
    0: 'danger',   // 差评
    1: 'warning',  // 中评
    2: 'success'   // 好评
  }
  return types[sentiment] || 'info'
}

// 获取情感文本
const getSentimentText = (sentiment) => {
  const texts = {
    0: '差评',
    1: '中评',
    2: '好评'
  }
  return texts[sentiment] || '未知'
}

// 获取置信度颜色
const getConfidenceColor = (confidence) => {
  const value = parseFloat(confidence)
  // 调整颜色阈值，使其更合理
  if (value > 0.9) return '#67C23A'  // 绿色，非常高的置信度
  if (value > 0.7) return '#E6A23C'  // 黄色，较高的置信度
  if (value > 0.5) return '#F0C78A'  // 浅橙色，中等置信度
  return '#F56C6C'  // 红色，低置信度
}
</script>

<style scoped>
.sentiment-analysis-usage {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.mode-selector {
  margin-bottom: 20px;
  text-align: center;
}

.input-card, .batch-card {
  margin-bottom: 2rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.card-header {
  margin-bottom: 1.5rem;
}

.card-header h3 {
  font-size: 1.2rem;
  color: #444;
  margin: 0;
}

.button-container {
  margin: 1rem 0;
  display: flex;
  justify-content: flex-end;
}

.result-container {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.upload-container {
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.file-info {
  color: #606266;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.batch-results {
  margin-top: 1.5rem;
}

.table-operations {
  margin-bottom: 1rem;
  display: flex;
  justify-content: flex-end;
}

.analyze-button {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

:deep(.el-tag) {
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
}

:deep(.el-descriptions) {
  padding: 1rem;
}

:deep(.el-progress) {
  margin: 0.5rem 0;
}

:deep(.el-upload-list) {
  margin-top: 1rem;
}

/* 添加新的过渡动画样式 */
.el-card {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.batch-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid #ebeef5;
}

.upload-section {
  flex: 0 0 auto;
  margin-right: 20px;
}

.file-info-section {
  flex: 1;
  padding: 0 20px;
}

.file-info {
  color: #606266;
  font-size: 0.9rem;
}

.file-list {
  margin-top: 0.5rem;
  color: #409EFF;
  font-size: 0.9rem;
}

.action-section {
  flex: 0 0 auto;
  margin-left: 20px;
}

.batch-content {
  margin-top: 1rem;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0.5rem 0;
}

.results-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #303133;
}

.results-container {
  border-radius: 4px;
  background: #fff;
  overflow-x: auto;
  max-height: 60vh;
  overflow-y: auto;
}

:deep(.el-table) {
  min-width: 600px;
}

@media (max-width: 1200px) {
  .results-container {
    overflow-x: auto;
    max-width: 100vw;
  }
  :deep(.el-table) {
    max-height: unset;
    min-width: 600px;
  }
}

@media (max-width: 768px) {
  .sentiment-analysis-usage {
    padding: 10px;
  }
  :deep(.el-descriptions-item) {
    padding: 0.5rem;
  }
  .results-container {
    overflow-x: auto;
    max-width: 100vw;
  }
  :deep(.el-table) {
    max-height: unset;
    min-width: 600px;
  }
}
</style>