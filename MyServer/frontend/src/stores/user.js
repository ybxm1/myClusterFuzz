import { getToken, setToken, removeToken } from '@/utils/auth'
import { login, getInfo } from '@/views/login/api' 
const user = {
  state: {
    // token: getToken(),
    name: '',
    info: {}
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_INFO: (state, info) => {
      state.info = info
    }
  },

  actions: {
    // 登录 
    Login ({ commit }, userForm) {
      const username = userForm.username.trim()
      const password = userForm.password.trim()

      return login(username, password).then(response => {
        const data = response.data
        console.log(response)
        // setToken(data.token)
        commit('SET_INFO', data.info)
        commit('SET_NAME', data.username)
        commit('SET_TOKEN', data.token)
      })
    },

    // 获取用户信息
    // GetInfo ({ commit, state }) {
    //   return new Promise((resolve, reject) => {
    //     getInfo(state.token).then(response => {
    //       const data = response.data
    //       commit('SET_INFO', data.info)
    //       commit('SET_NAME', data.username)
    //       resolve(response)
    //     }).catch(error => {
    //       reject(error)
    //     })
    //   })
    // },

    // 登出
    LogOut ({ commit, state }) {
      return new Promise((resolve, reject) => {
        commit('SET_TOKEN', '')
        // removeToken()
        resolve()
      })
    }
  }
}

export default user
