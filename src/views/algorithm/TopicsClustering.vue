<template>
  <div class="topics-clustering">
    <div class="filter-container">
      <el-select
        v-model="selectedBrand"
        placeholder="选择品牌"
        class="filter-item"
        size="small"
      >
        <el-option label="总体" value="总体" />
        <el-option label="科沃斯" value="科沃斯" />
        <el-option label="小米" value="小米" />
        <el-option label="石头" value="石头" />
        <el-option label="追觅" value="追觅" />
        <el-option label="云鲸" value="云鲸" />
      </el-select>

      <el-select
        v-model="selectedSentiment"
        placeholder="选择情感倾向"
        class="filter-item"
        size="small"
      >
        <el-option label="正向评论" value="正向" />
        <el-option label="负向评论" value="负向" />
      </el-select>
    </div>

    <div class="visualization-container" v-loading="loading">
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <iframe
        v-show="!error"
        :src="currentUrl"
        class="lda-iframe"
        ref="ldaIframe"
        @load="handleIframeLoad"
        @error="handleIframeError"
        sandbox="allow-same-origin allow-scripts allow-popups allow-modals"
        scrolling="no"
      ></iframe>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage } from 'element-plus'

const selectedBrand = ref('总体')
const selectedSentiment = ref('正向')
const loading = ref(true)
const error = ref('')

// 计算当前应该显示的URL
const currentUrl = computed(() => {
  if (!selectedBrand.value || !selectedSentiment.value) return ''
  // 使用相对路径
  return `/LDA可视化页面/${selectedBrand.value}_${selectedSentiment.value}_主题模型可视化.html`
})

// 添加必要的脚本
const loadExternalScripts = () => {
  const d3Script = document.createElement('script')
  d3Script.src = 'https://d3js.org/d3.v5.js'
  d3Script.async = true
  
  const ldavisScript = document.createElement('script')
  ldavisScript.src = 'https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.4.0/pyLDAvis/js/ldavis.v3.0.0.js'
  ldavisScript.async = true
  
  document.head.appendChild(d3Script)
  document.head.appendChild(ldavisScript)
}

// 添加 CSS 引入
const loadExternalStyles = (iframeDocument) => {
  const link = document.createElement('link')
  link.rel = 'stylesheet'
  link.type = 'text/css'
  link.href = 'https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.4.0/pyLDAvis/js/ldavis.v1.0.0.css'
  if (iframeDocument) {
    iframeDocument.head.appendChild(link)
  }
}

// 监听选择变化
watch([selectedBrand, selectedSentiment], () => {
  loading.value = true
  error.value = ''
})

// iframe加载完成的处理
const handleIframeLoad = (event) => {
  loading.value = false
  try {
    const iframe = event.target
    if (iframe.contentWindow.document.body.innerHTML === '') {
      throw new Error('页面内容为空')
    }

    const iframeDoc = iframe.contentWindow.document
    loadExternalStyles(iframeDoc)
    const style = iframeDoc.createElement('style')
    
    // 获取容器尺寸
    const container = document.querySelector('.visualization-container')
    const containerWidth = container.clientWidth
    const containerHeight = container.clientHeight
    
    // 小屏幕下设置自适应缩放
    const screenWidth = window.innerWidth
    const scale = screenWidth < 2000 ? Math.min(containerWidth / 1024, containerHeight / 768) * 0.9 : 1 // 增加缩放比例

    // 设置页面缩放和布局
    style.textContent = `
      html, body {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100% !important;
        overflow: hidden !important;
      }
      body {
        position: absolute;
        left: 50%;
        top: 0;
        transform: translateX(-50%) scale(${scale});
        transform-origin: top center;
        width: ${Math.ceil(100/scale)}% !important;
        height: ${Math.ceil(100/scale)}vh !important;
        display: flex !important;
        justify-content: center !important;
        align-items: flex-start !important;
      }
      #ldavis {
        margin: 0 auto !important;
        padding: 0 !important;
        width: 100% !important;
        height: auto !important;
        display: block !important;
        transform-origin: top center !important;
      }
      .bubble-tool, svg {
        width: 100% !important;
        height: auto !important;
        max-width: none !important;
        transform-origin: top center !important;
      }
    `
    iframeDoc.head.appendChild(style)
    
    // 调整 iframe 尺寸
    iframe.style.width = '100%'
    iframe.style.height = '100%'
    iframe.style.maxWidth = 'none'
    iframe.style.maxHeight = 'none'
    iframe.style.position = 'absolute'
    iframe.style.top = '0'
    iframe.style.left = '0'
    iframe.style.right = '0'
    iframe.style.bottom = '0'
  } catch (e) {
    handleIframeError(e)
  }
}

// iframe加载错误处理
const handleIframeError = (e) => {
  loading.value = false
  error.value = '加载可视化内容失败，请检查文件路径或刷新页面重试'
  console.error('iframe加载错误:', e)
  ElMessage.error('加载可视化内容失败')
}

// 组件挂载时初始化
onMounted(async () => {
  loadExternalScripts()
  
  try {
    const response = await fetch(currentUrl.value)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
  } catch (e) {
    handleIframeError(e)
  }
})
</script>

<style scoped>
.topics-clustering {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: calc(100vh - 60px); /* 进一步减小顶部空间 */
  overflow: hidden;
  background-color: #fff;
  padding: 0; /* 移除内边距 */
}

.filter-container {
  display: flex;
  gap: 6px;
  padding: 2px 4px; /* 进一步减小过滤器内边距 */
  margin-bottom: 2px; /* 减小下边距 */
  background-color: #fff;
  z-index: 1;
}

.filter-item {
  width: 110px; /* 继续减小选择器宽度 */
}

.visualization-container {
  position: relative;
  flex: 1;
  width: 100%;
  height: calc(100% - 32px); /* 减小过滤器占用空间 */
  overflow: hidden;
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0; /* 移除所有边距 */
}

.lda-iframe {
  border: none;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.error-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #f56c6c;
  text-align: center;
}

:deep(.el-loading-mask) {
  background-color: rgba(255, 255, 255, 0.8);
}
</style>