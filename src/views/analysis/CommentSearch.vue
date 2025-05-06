<template>
  <div class="comment-search">
    <el-card class="search-card">
      <!-- 搜索条件区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="search-form" size="small">
          <el-form-item label="平台" label-width="50px">
            <el-select v-model="searchForm.platform" placeholder="选择平台" clearable style="width: 120px">
              <el-option label="京东" value="JD" />
              <el-option label="淘宝" value="TB" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="品牌" label-width="50px">
            <el-select 
              v-model="searchForm.brand" 
              placeholder="选择品牌" 
              clearable 
              style="width: 120px"
              @change="handleBrandChange"
            >
              <el-option v-for="brand in brandOptions" :key="brand" :label="brand" :value="brand" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="型号" label-width="50px">
            <el-select 
              v-model="searchForm.model" 
              placeholder="选择产品型号" 
              clearable 
              style="width: 180px"
              :disabled="!searchForm.brand"
            >
              <el-option 
                v-for="model in filteredModelOptions" 
                :key="model" 
                :label="model" 
                :value="model" 
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="日期" label-width="50px">
            <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
              style="width: 240px"
              :shortcuts="dateShortcuts"
              :locale="zhCn"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleSearch" size="small">查询</el-button>
            <el-button @click="resetForm" size="small">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 数据表格区域 -->
      <el-table
        :data="tableData"
        style="width: 100%"
        border
        stripe
        v-loading="loading"
        height="calc(100vh - 220px)"
        size="small"
      >
        <el-table-column prop="用户ID" label="用户ID" width="140" />
        <el-table-column prop="评论时间" label="评论时间" width="140" />
        <el-table-column prop="评论内容" label="评论内容" min-width="400" show-overflow-tooltip>
          <template #default="scope">
            <div style="white-space: pre-line;">{{ scope.row.评论内容 }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="评分" label="评分" width="80" align="center">
          <template #default="scope">
            <span>{{ scope.row.评分 || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="情感倾向" label="情感" width="80" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.情感倾向 === 1 ? 'success' : 'danger'" size="small">
              {{ scope.row.情感倾向 === 1 ? '积极' : '消极' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页器 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[20, 50, 100, 200]"
          :popper-class="'custom-pagination'"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          small
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import * as XLSX from 'xlsx'
import { ElMessage } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    }
  },
  {
    text: '最近三个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    }
  }
]

// 搜索表单数据
const searchForm = reactive({
  platform: '',
  brand: '',
  model: '',
  dateRange: []
})

// 表格数据
const tableData = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 品牌和型号选项
const brandOptions = ref([])
const modelOptions = ref({}) // 改为对象，key为品牌，value为该品牌的型号数组

// 根据选择的品牌过滤型号选项
const filteredModelOptions = computed(() => {
  if (!searchForm.brand) return []
  return modelOptions.value[searchForm.brand] || []
})

// 品牌变更处理
const handleBrandChange = () => {
  searchForm.model = '' // 清空型号选择
}

// 原始数据
const rawData = ref([])

// 读取Excel文件数据
const loadExcelData = async () => {
  try {
    loading.value = true
    const response = await fetch('/public/中期后_情感分析后完整数据集.xlsx')
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    
    const arrayBuffer = await response.arrayBuffer()
    const workbook = XLSX.read(arrayBuffer)
    const worksheet = workbook.Sheets[workbook.SheetNames[0]]
    rawData.value = XLSX.utils.sheet_to_json(worksheet)
    
    // 提取品牌和对应的型号选项
    const brands = new Set()
    const brandModelMap = {}
    
    rawData.value.forEach(row => {
      if (row['品牌']) {
        brands.add(row['品牌'])
        if (!brandModelMap[row['品牌']]) {
          brandModelMap[row['品牌']] = new Set()
        }
        if (row['产品型号']) {
          brandModelMap[row['品牌']].add(row['产品型号'])
        }
      }
    })
    
    brandOptions.value = Array.from(brands)
    // 转换Set为数组
    Object.keys(brandModelMap).forEach(brand => {
      modelOptions.value[brand] = Array.from(brandModelMap[brand])
    })
    
    // 初始加载数据
    handleSearch()
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('数据加载失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  loading.value = true
  
  // 筛选数据
  let filteredData = [...rawData.value]
  
  if (searchForm.platform) {
    filteredData = filteredData.filter(row => 
      searchForm.platform === 'JD' ? row['平台'] === 'JD' : row['平台'] === 'TB'
    )
  }
  
  if (searchForm.brand) {
    filteredData = filteredData.filter(row => row['品牌'] === searchForm.brand)
  }
  
  if (searchForm.model) {
    filteredData = filteredData.filter(row => row['产品型号'] === searchForm.model)
  }
  
  if (searchForm.dateRange && searchForm.dateRange.length === 2) {
    const startDate = new Date(searchForm.dateRange[0])
    const endDate = new Date(searchForm.dateRange[1])
    filteredData = filteredData.filter(row => {
      const commentDate = new Date(row['评论时间'])
      return commentDate >= startDate && commentDate <= endDate
    })
  }
  
  total.value = filteredData.length
  
  // 分页处理
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  tableData.value = filteredData.slice(start, end)
  
  loading.value = false
}

// 重置表单
const resetForm = () => {
  searchForm.platform = ''
  searchForm.brand = ''
  searchForm.model = ''
  searchForm.dateRange = []
  currentPage.value = 1
  handleSearch()
}

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val
  handleSearch()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  handleSearch()
}

// 组件挂载时加载数据
onMounted(() => {
  loadExcelData()
})
</script>

<style>
/* 修改分页组件的文本 */
.el-pagination {
  --el-pagination-small-padding: 0 6px;
}

.el-pagination .el-pagination__total {
  display: flex;
  align-items: center;
}

.el-pagination .el-pagination__total::before {
  content: '';
}

.el-pagination .el-pagination__total::after {
  content: ' 条';
}

.el-pagination .el-pagination__sizes .el-select__caret::before {
  content: '';
}

.el-pagination .btn-prev .el-icon {
  display: none;
}

.el-pagination .btn-next .el-icon {
  display: none;
}

.el-pagination .btn-prev::before {
  content: '上一页';
  font-size: 13px;
}

.el-pagination .btn-next::before {
  content: '下一页';
  font-size: 13px;
}

.el-pagination .el-pager li:not(.more)::before {
  content: '';
  font-size: 13px;
}

.el-pagination .el-pager li:not(.more)::after {
  content: '';
  font-size: 13px;
}

.el-pagination .el-pagination__jump::before {
  content: '';
  font-size: 13px;
}

.el-pagination .el-pagination__jump .el-pagination__editor {
  margin: 0 4px;
}

.el-pagination .el-pagination__jump::after {
  content: '页';
  font-size: 13px;
}
</style>

<style scoped>
.comment-search {
  padding: 8px;
  height: 100%;
  box-sizing: border-box;
}

.search-card {
  height: 100%;
}

.search-area {
  margin-bottom: 8px;
  background-color: #f8f9fa;
  padding: 8px;
  border-radius: 4px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.pagination-container {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end;
  padding: 4px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

:deep(.el-card__body) {
  height: calc(100% - 20px);
  padding: 10px !important;
  display: flex;
  flex-direction: column;
}

:deep(.el-table) {
  flex: 1;
}

:deep(.el-table .cell) {
  line-height: 1.5;
}

:deep(.el-form-item) {
  margin-bottom: 0;
  margin-right: 8px;
}

:deep(.el-form-item__label) {
  padding-right: 4px;
}

:deep(.el-tag) {
  width: 42px;
}
</style>