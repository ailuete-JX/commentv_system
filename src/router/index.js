import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import ProductAnalysis from '../views/analysis/ProductAnalysis.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },  {
    path: '/keywords',
    name: 'KeywordsAnalysis',
    component: () => import('../views/analysis/SentimentAnalysis.vue'),
    meta: { requiresAuth: true }
  },  {
    path: '/emotion',
    name: 'EmotionAnalysis',
    component: () => import('../views/analysis/KeywordsAnalysis.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/topics',
    name: 'TopicsAnalysis',
    component: () => import('../views/analysis/TopicsAnalysis.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/analysis/product',
    name: 'ProductAnalysis',
    component: ProductAnalysis,
    meta: { requiresAuth: true }
  },
  {
    path: '/geographic',
    name: 'GeographicAnalysis',
    component: () => import('../views/analysis/GeographicAnalysis.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/analysis/comments',
    name: 'CommentSearch',
    component: () => import('../views/analysis/CommentSearch.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/algorithm',
    name: 'Algorithm',
    component: () => import('../views/algorithm/Algorithm.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'sentiment-model',
        name: 'SentimentModel',
        component: () => import('../views/algorithm/SentimentModel.vue'),
        meta: {
          requiresAuth: true,
          title: '情感分析模型评估'
        }
      },
      {
        path: 'sentiment-analysis',
        name: 'SentimentAnalysis',
        component: () => import('../views/algorithm/SentimentAnalysis.vue'),
        meta: {
          requiresAuth: true,
          title: '情感分析使用'
        }
      }
    ]
  },
  {
    path: '/algorithm/clustering',
    name: 'TopicsClustering',
    component: () => import('../views/algorithm/TopicsClustering.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/suggestions',
    name: 'Suggestions',
    component: () => import('../views/Suggestions.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn')
  
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router