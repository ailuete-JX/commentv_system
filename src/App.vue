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
  const pathMap = {    
    '/': '1',
    '/keywords': '2-1',
    '/topics': '2-2',
    '/analysis/product': '2-3',
    '/geographic': '2-4',
    '/emotion': '2-5',    
    '/analysis/comments': '2-6',
    '/algorithm/sentiment-model': '3-1',
    '/algorithm/clustering': '3-2',
    '/optimization': '4'
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
    case '4':
      router.push('/optimization')
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
          background-color="#F7F7F7"
          text-color="#333"
          active-text-color="#1976d2"
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
            <el-menu-item index="2-2">时间序列分析</el-menu-item>
            <el-menu-item index="2-3">产品评分分析</el-menu-item>
            <el-menu-item index="2-4">地理分布分析</el-menu-item>
            <el-menu-item index="2-5">情感词云图分析</el-menu-item>
            <el-menu-item index="2-6">评论查询</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="3">
            <template #title>
              <el-icon><Monitor /></el-icon>
              <span>算法分析</span>
            </template>
            <el-menu-item index="3-1">情感分析模型</el-menu-item>
            <el-menu-item index="3-2">主题聚类分析</el-menu-item>
          </el-sub-menu>
          <el-menu-item index="4">
            <el-icon><Notification /></el-icon>
            <template #title>优化建议</template>
          </el-menu-item>
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
          <router-view></router-view>
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
  background-color: #F7F7F7;
  border-right: 1.5px solid #e5e7eb; /* 更柔和的分割线 */
  box-shadow: none; /* 去除阴影 */
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  border-top-right-radius: 16px; /* 圆角过渡 */
  border-bottom-right-radius: 16px;
  z-index: 2;
}

.menu-vertical {
  height: 100%;
  border-right: none;
  background-color: #F7F7F7;
  color: #333;
  font-weight: 500;
  font-size: 15px;
  overflow: hidden; /* 禁止滚动条 */
}

.menu-vertical::-webkit-scrollbar {
  width: 0 !important;
  display: none !important;
}

.menu-vertical {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE 10+ */
}  .menu-vertical .el-menu-item,
.menu-vertical .el-sub-menu__title {
  background-color: #F7F7F7 !important;
  color: #333 !important;
  border-radius: 6px;
  margin: 2px 6px;
  transition: background 0.2s;
}

/* 统一所有一级菜单项的内边距 */
.menu-vertical > .el-menu-item,
.menu-vertical > .el-sub-menu > .el-sub-menu__title {
  padding-left: 16px !important;
}

/* 子菜单项的内边距 */
.menu-vertical .el-menu--inline .el-menu-item {
  padding-left: 40px !important;
}

.menu-vertical .el-menu-item.is-active {
  background-color: #e3edfa !important;
  color: #1976d2 !important;
  font-weight: bold;
}

.menu-vertical .el-menu-item:hover,
.menu-vertical .el-sub-menu__title:hover {
  background-color: #f0f4fa !important;
  color: #1976d2 !important;
}

.menu-vertical .el-menu-item .el-icon,
.menu-vertical .el-sub-menu__title .el-icon {
  margin-right: 10px !important; /* 统一图标和文字间距 */
  color: #1976d2;
}

.layout-header {
  height: 60px;
  line-height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #f0f0f0;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.02);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-left h2 {
  font-size: 20px;
  color: #222;
  font-weight: 600;
  letter-spacing: 1px;
}

.header-right {
  display: flex;
  align-items: center;
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
  color: #1976d2;
  transition: color 0.2s;
}

.collapse-btn:hover {
  color: #409eff;
}

.layout-main {
  height: calc(100% - 60px);
  background-color: #fcfdff;
  padding: 32px 32px 24px 32px;
  overflow-y: auto;
  border-radius: 0 12px 0 0; /* 右上圆角，左侧无圆角 */
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.03);
  margin-left: 0;
}
</style>
