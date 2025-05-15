<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  HomeFilled,
  Monitor,
  DataAnalysis,
  Notification,
  Fold,
  Expand
} from '@element-plus/icons-vue'

const getMenuIndexFromPath = (path) => {
  const pathMap = {    '/': '1',
    '/keywords': '2-1',
    '/topics': '2-2',
    '/analysis/product': '2-3',
    '/geographic': '2-4',
    '/emotion': '2-5',    '/analysis/comments': '2-6',
    '/algorithm/sentiment-model': '3-1',
    '/algorithm/clustering': '3-2'
  }
  return pathMap[path] || '1'
}

const router = useRouter()
const route = useRoute()
const isCollapse = ref(false)
const activeIndex = computed(() => getMenuIndexFromPath(route.path))

const handleMenuSelect = (index) => {
  switch(index) {
    case '1':
      router.push('/')
      break
    case '2-1':
      router.push('/keywords')
      break
    case '2-2':
      router.push('/topics')
      break
    case '2-3':
      router.push('/analysis/product')
      break
    case '2-4':
      router.push('/geographic')
      break
    case '2-5':
      router.push('/emotion')
      break
    case '2-6':
      router.push('/analysis/comments')
      break
    case '3-1':
      router.push('/algorithm/sentiment-model')
      break
    case '3-2':
      router.push('/algorithm/clustering')
      break
  }
}

const handleLogout = () => {
  localStorage.removeItem('isLoggedIn')
  router.push('/login')
}
</script>

<template>
  <div v-if="$route.path !== '/login'">
    <el-container class="layout-container">
      <el-aside :width="isCollapse ? '64px' : '200px'" class="menu-aside">
        <el-menu
          :default-active="activeIndex"
          class="menu-vertical"
          :collapse="isCollapse"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          @select="handleMenuSelect"
        >
          <el-menu-item index="1">
            <el-icon><HomeFilled /></el-icon>
            <template #title>主页</template>
          </el-menu-item>

          <el-sub-menu index="2">
            <template #title>
              <el-icon><DataAnalysis /></el-icon>
              <span>描述性分析</span>
            </template>
            <el-menu-item index="2-1">高频词分析</el-menu-item>
            <el-menu-item index="2-2">评论时间序列</el-menu-item>
            <el-menu-item index="2-3">产品评论分析</el-menu-item>
            <el-menu-item index="2-4">地理分布分析</el-menu-item>
            <el-menu-item index="2-5">情感词云图分析</el-menu-item>
            <el-menu-item index="2-6">评论查询</el-menu-item>
          </el-sub-menu>          <el-sub-menu index="3">
            <template #title>
              <el-icon><Monitor /></el-icon>
              <span>算法分析</span>
            </template>
            <el-menu-item index="3-1">情感分析模型</el-menu-item>
            <el-menu-item index="3-2">主题聚类分析</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header class="layout-header">
          <div class="header-left">
            <el-icon 
              class="collapse-btn"
              @click="isCollapse = !isCollapse"
            >
              <Fold v-if="!isCollapse"/>
              <Expand v-else/>
            </el-icon>
            <h2>扫地机器人评论分析系统</h2>
          </div>
          <div class="header-right">
            <el-button type="danger" plain size="small" @click="handleLogout">
              退出登录
            </el-button>
          </div>
        </el-header>

        <el-main class="layout-main">
          <div class="main-content">
            <router-view></router-view>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
  <router-view v-else></router-view>
</template>

<style scoped>
.layout-container {
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.menu-aside {
  height: 100%;
  transition: width 0.3s;
  background-color: #545c64;
}

.menu-vertical {
  height: 100%;
  border-right: none;
}

.layout-header {
  height: 60px;
  line-height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
}

.collapse-btn:hover {
  color: #409eff;
}

.layout-main {
  height: calc(100% - 60px);
  background-color: #f0f2f5;
  padding: 16px;
  overflow-y: auto;
}

.main-content {
  background-color: #fff;
  border-radius: 4px;
  padding: 16px;
  height: 100%;
}
</style>
