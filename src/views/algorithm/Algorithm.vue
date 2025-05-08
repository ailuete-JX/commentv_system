<template>
  <div class="algorithm-container">
    <el-menu
      v-if="shouldShowMenu"
      :default-active="activeMenu"
      class="algorithm-menu"
      mode="horizontal"
      router
    >
      <el-menu-item index="/algorithm/sentiment-model">情感分析模型</el-menu-item>
      <el-menu-item index="/algorithm/sentiment-analysis">情感分析使用</el-menu-item>
    </el-menu>
    <div class="algorithm-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)

// 只在情感分析相关页面显示导航菜单
const shouldShowMenu = computed(() => {
  return route.path === '/algorithm/sentiment-model' || 
         route.path === '/algorithm/sentiment-analysis'
})
</script>

<style scoped>
.algorithm-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #fff;
}

.algorithm-menu {
  border-bottom: solid 1px #e6e6e6;
  padding-left: 20px;
}

.algorithm-content {
  flex: 1;
  overflow: hidden;
}
</style>