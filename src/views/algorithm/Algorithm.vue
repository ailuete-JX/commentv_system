<template>
  <div class="algorithm-container">
    <el-menu
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
  padding: 0;
  position: relative;
}
</style>