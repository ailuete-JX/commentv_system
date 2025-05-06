<template>
  <div class="login-container">
    <div class="login-background">
      <div class="stars">
        <div class="meteor-1"></div>
        <div class="meteor-2"></div>
        <div class="meteor-3"></div>
        <div class="meteor-4"></div>
        <div class="meteor-5"></div>
      </div>
    </div>
    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <div class="system-logo">
            <el-icon size="32" color="#409EFF"><Monitor /></el-icon>
          </div>
          <h2>智能扫地机器人评论分析系统</h2>
          <p class="system-subtitle">Robotic Vacuum Cleaner Review Analysis</p>
        </div>
      </template>
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="0"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            :prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            :prefix-icon="Lock"
            show-password
            size="large"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-button" size="large" @click="handleLogin">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Monitor } from '@element-plus/icons-vue'

const router = useRouter()
const loginFormRef = ref(null)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = () => {
  loginFormRef.value.validate((valid) => {
    if (valid) {
      if (loginForm.username === 'admin' && loginForm.password === '123456') {
        localStorage.setItem('isLoggedIn', 'true')
        ElMessage.success('登录成功')
        router.push('/')
      } else {
        ElMessage.error('用户名或密码错误')
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #ffffff 0%, #e8f4f8 100%);
  z-index: 0;
}

.stars {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.meteor-1,
.meteor-2,
.meteor-3,
.meteor-4,
.meteor-5 {
  position: absolute;
  background: linear-gradient(to right, rgba(64, 158, 255, 0.3), transparent);
  height: 3px;
  width: 150px;
  transform: rotate(-45deg);
  animation: meteor linear infinite;
  border-radius: 1px;
  box-shadow: 0 0 5px rgba(64, 158, 255, 0.5);
}

.meteor-1 {
  top: 10%;
  left: 80%;
  animation-duration: 4s;
  animation-delay: 0s;
  background: linear-gradient(to right, rgba(64, 158, 255, 0.4), transparent);
}

.meteor-2 {
  top: 20%;
  left: 40%;
  animation-duration: 5s;
  animation-delay: 1s;
  background: linear-gradient(to right, rgba(103, 194, 58, 0.4), transparent);
}

.meteor-3 {
  top: 30%;
  left: 60%;
  animation-duration: 3s;
  animation-delay: 2s;
  background: linear-gradient(to right, rgba(144, 147, 153, 0.4), transparent);
}

.meteor-4 {
  top: 40%;
  left: 20%;
  animation-duration: 4.5s;
  animation-delay: 3s;
  background: linear-gradient(to right, rgba(230, 162, 60, 0.4), transparent);
}

.meteor-5 {
  top: 50%;
  left: 70%;
  animation-duration: 3.5s;
  animation-delay: 4s;
  background: linear-gradient(to right, rgba(64, 158, 255, 0.4), transparent);
}

@keyframes meteor {
  0% {
    opacity: 0;
    transform: rotate(-45deg) translateX(0);
  }
  20% {
    opacity: 1;
  }
  80% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: rotate(-45deg) translateX(-1500px);
  }
}

.login-card {
  width: 420px;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;
  transform: translateY(0);
  transition: all 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
}

.login-header {
  text-align: center;
  padding: 10px 0;
}

.system-logo {
  margin-bottom: 16px;
  animation: logoFloat 3s ease-in-out infinite;
}

.system-subtitle {
  margin: 8px 0 0;
  color: #909399;
  font-size: 14px;
  letter-spacing: 1px;
}

.login-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
  font-weight: 600;
  letter-spacing: 1px;
}

.login-form {
  padding: 24px 0;
}

.login-form :deep(.el-input) {
  --el-input-hover-border-color: #409EFF;
  --el-input-focus-border-color: #409EFF;
}

.login-form :deep(.el-input__wrapper) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.login-form :deep(.el-input__inner) {
  height: 42px;
}

.login-button {
  width: 100%;
  height: 42px;
  font-size: 16px;
  letter-spacing: 2px;
  background: linear-gradient(135deg, #8E9EAB 0%, #647687 100%);
  border: none;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(100, 118, 135, 0.3);
}

@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* 添加响应式样式 */
@media (max-width: 480px) {
  .login-card {
    width: 90%;
    margin: 0 20px;
  }
}

/* 添加输入框动画效果 */
.el-form-item {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.5s ease forwards;
}

.el-form-item:nth-child(1) {
  animation-delay: 0.2s;
}

.el-form-item:nth-child(2) {
  animation-delay: 0.3s;
}

.el-form-item:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>