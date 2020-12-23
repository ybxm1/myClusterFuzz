import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI, { Message } from 'element-ui'
import App from './App.vue'
import router from './router'
import './styles/index.scss'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/zh-CN'
import store from '@/stores'
import '@/icons'
import NProgress from 'nprogress'
import '@/styles/nprogress.css'
import { getToken } from '@/utils/auth'

Vue.use(VueRouter)
Vue.use(ElementUI, { locale })
Vue.config.productionTip = false

// eslint-disable-next-line no-new  
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})

NProgress.configure({
  easing: 'ease',
  speed: 500,
  showSpinner: false,
  trickleSpeed: 200,
  minimum: 0.3
})

router.afterEach(() => {
  NProgress.done()
})


// 如果放上beforEach，那么会在路由之前先判断路径，如果其中不给出路由的路径，那么程序就不知道该去哪里了
// router.beforeEach((to, from, next) => {
  // let token = getToken()
  // console.log('token:', token, 'end')
  // console.log('main.js: router.beforeEach')

  // if (token !== 'undefined' && token !== '' && typeof (token) !== 'undefined') {
  //   if (to.path === '/login') {
  //     next({ path: '/' })
  //   } else {
  //     NProgress.start()
  //     store.dispatch('GetInfo').then(res => {
  //       next()
  //     }).catch(() => {
  //       store.dispatch('LogOut').then(() => {
  //         Message.error('验证失败，请重新登陆')
  //         next({ path: '/login' })
  //       })
  //     })
  //   }
  // } else {
  //   if (to.path === '/login') {
  //     next()
  //   } else {
  //     next('/login')
  //   }
  // }


// })
