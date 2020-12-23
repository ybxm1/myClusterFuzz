import { getJobs_runing, getJobs_complete } from '@/views/jobs/api'

const jobs = {
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
    reloadJobs_runing (context) {
      return getJobs_runing().then(response => {
        if (response.code >= 500) {
          throw new Error('服务器连接失败')
        }
        // context.commit('ADD_JOBS', response.data)
        return response.data
      })
    },
    reloadJobs_complete (context) {
        return getJobs_complete().then(response => {
          if (response.code >= 500) {
            throw new Error('服务器连接失败')
          }
        //   context.commit('ADD_JOBS', response.data)
          return response.data
        })
      }
  },
  getters: {
    completedJobs1: state => {
        reloadJobs_runing()
        return state.jobs
    },
    uncompletedJobs: state => {
        return state.jobs
    },
    // errorJobs: state => {
    //   if (!state.jobs) return []
    //   return state.jobs.filter(job => {
    //     return job.status === 5
    //   })
    // }
  }
}
export default jobs
