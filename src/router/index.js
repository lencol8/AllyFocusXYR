import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue')
  },
  {
    path: '/login',
    name: 'LogIn',
    component: () => import('../views/LogIn.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/token',
    name: 'Token',
    component: () => import('../components/Token.vue')
  },
  {
    path: '/stake',
    name: 'Stake',
    component: () => import('../components/Stake.vue')
  },
  // {
  //   path: '/wc',
  //   name: 'WalletConnect',
  //   component: () => import('../components/WalletConnect.vue')
  // },
  {
    path: '/:city',
    name: 'City',
    component: () => import('../views/City.vue')
  },
  {
    path: '/:city/:category',
    name: 'Category',
    component: () => import('../views/Category.vue')
  },
  {
    path: '/:city/:category/:key',
    name: 'Post',
    component: () => import('../views/Post.vue')
  },
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
