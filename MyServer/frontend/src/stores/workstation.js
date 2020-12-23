import { getJobs } from '@/views/workstation/api'
const workstation = {
  state: {
    jobs: null, // 任务列表中的任务
    cases: {}, // 展示的用例
    createDialog: false // 新建任务窗口
  },
  mutations: {
    ADD_JOBS (state, newJobs) {
      state.jobs = newJobs
    },
    CHANGE_CREA_DIALOG (state, status) {
      state.createDialog = status
    }
  },
  actions: {
    reloadJobs (context) {
      return getJobs().then(response => {
        if (response.code >= 500) {
          throw new Error('服务器连接失败')
        }
        context.commit('ADD_JOBS', response.data)
        return response.data
      })
    }
  },
  getters: {
    completedJobs: state => {
      if (!state.jobs) return []
      return state.jobs.filter(job => {
        return job.status === 4
      })
    },
    uncompletedJobs: state => {
      if (!state.jobs) return []
      return state.jobs.filter(job => {
        return job.status !== 4 && job.status !== 5
      })
    },
    errorJobs: state => {
      if (!state.jobs) return []
      return state.jobs.filter(job => {
        return job.status === 5
      })
    }
  }
}
export default workstation
