import VueRouter from 'vue-router'
import Layout from './Layout'

export const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/login',
    name: '主界面',     // 根目录默认定向到登录界面
    hidden: true
  },
  // {
  //   path: '/testvue',
  //   component: Layout,
  //   redirect: '/create',  // 改成要测试的页面 
  //   name: '测试界面',
  //   hidden: true
  // },

  {
    path: '/login',
    component: () => import('@/views/login'),
    name: '登陆界面',
    hidden: true
  },
  {
    path: '/create',
    name: '创建任务',
    icon: 'console',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/create')
      }
    ]
    //hidden: true  如果设置为true，则在侧栏中不会显示来任务链接，任务侧栏中会通过routers来获取所有没有被隐藏的功能栏
  },
  {
    path: '/joblist',
    name: '任务列表',
    icon: 'case',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/jobs')
      }
    ]
    //hidden: true  如果设置为true，则在侧栏中不会显示来任务链接，任务侧栏中会通过routers来获取所有没有被隐藏的功能栏
  },
  {
    path: '/crashlist',
    name: '漏洞列表',
    icon: 'vuls',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/crashes')
      }
    ]
    //hidden: true  如果设置为true，则在侧栏中不会显示来任务链接，任务侧栏中会通过routers来获取所有没有被隐藏的功能栏
  },
  {
    path: '/nodelist',
    name: '节点资源列表',
    icon: 'users',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/nodes')
      }
    ]
    //hidden: true  如果设置为true，则在侧栏中不会显示来任务链接，任务侧栏中会通过routers来获取所有没有被隐藏的功能栏
  },
  {
    path: '/reproduce',
    name: '漏洞修复验证',
    icon: 'vuls',
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/reproduce')
      }
    ]
    //hidden: true  如果设置为true，则在侧栏中不会显示来任务链接，任务侧栏中会通过routers来获取所有没有被隐藏的功能栏
  },

  
  // {
  //   path: '/workstation',
  //   name: '任务工作台',
  //   icon: 'console',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '',
  //       component: () => import('@/views/workstation')
  //     },
  //     {
  //       path: 'job',
  //       component: () => import('@/views/fuzz/JobContainer'),
  //       children: [
  //         {
  //           path: 'case/:id',
  //           component: () => import('@/views/fuzz/CasePanel')
  //         },
  //         {
  //           path: 'fuzz/:id',
  //           component: () => import('@/views/fuzz/FuzzPanel')
  //         },
  //         {
  //           path: 'result/:id',
  //           component: () => import('@/views/fuzz/ResultPanel')
  //         }
  //       ]
  //     },
  //     {
  //       path: 'scan/:id',
  //       component: () => import('@/views/scan')
  //     }
  //   ]
  // },



  // {
  //   path: '/case',
  //   name: '用例库管理',
  //   icon: 'case',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '',
  //       component: () => import('@/views/case/index')
  //     }
  //   ]
  // },
  // {
  //   path: '/vuls',
  //   name: '漏洞库管理',
  //   icon: 'vuls',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '',
  //       component: () => import('@/views/vuls')
  //     }
  //   ]
  // },
  // {
  //   path: '/users',
  //   name: '用户管理',
  //   icon: 'users',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '',
  //       component: () => import('@/views/users')
  //     }
  //   ]
  // },

  {
    path: '/settings',
    name: '设置',
    icon: 'setting',
    hidden: true,
    component: Layout,
    children: [
      {
        path: '',
        component: () => import('@/views/settings')
      }
    ]
  },
  {
    name: '404',
    path: '/404',
    hidden: true,
    component: () => import('@/views/404.vue')
  },
  {
    path: '*',
    redirect: '/',
    hidden: true
  }
]

export default new VueRouter({
  routes
})
