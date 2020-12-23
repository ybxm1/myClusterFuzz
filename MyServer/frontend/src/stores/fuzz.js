import { getJob, getCases, getFuzzStatus, modifyJob } from '@/views/fuzz/api'
const fuzz = {
  state: {
    job: null, // 当前的任务
    sessionInfo: null, // 当前会话状态
    selectCases: [], // 用例选择里被选择的用例
    activeName: 'selectCase', // jobPanel中当前的面板名
    cases: []
  },
  mutations: {
    SET_JOB (state, newJob) {
      state.job = newJob
    },
    SET_SESSION (state, sessionInfo) {
      state.sessionInfo = sessionInfo
    },
    EMPTY_SELECT (state) {
      state.selectCases = []
    },
    ADD_CASES (state, newCases) {
      state.cases = newCases
    },
    SELECT_CASE (state, item) {
      if (state.selectCases.some(ele => ele._id === item._id)) {
        return
      }
      state.selectCases.push(item)
    },
    REMOVE_CASE (state, item) { // 删除测试用例
      state.selectCases = state.selectCases.filter(i => i._id !== item._id)
    }
  },
  actions: {
    loadJob (context, jobId) {
      return getJob(jobId).then(response => {
        if (response.code >= 500) {
          throw new Error('服务器错误')
        }
        context.commit('SET_JOB', response.data)
        return response.data
      })
    },
    loadSessionInfo (context, jobId) {
      return getFuzzStatus(jobId).then(response => {
        context.commit('SET_JOB', response.data.job)
        context.commit('SET_SESSION', response.data.sessionInfo)
      })
    },
    loadCases (context) {
      return getCases().then(response => {
        if (response.code >= 500) {
          throw new Error('服务器错误')
        }
        context.commit('ADD_CASES', response.data)
      })
    },
    saveSelectCases (context) {
      return modifyJob(context.state.job._id,
        {
          'case': context.state.selectCases,
          'status': 1
        }).then(resp => {
        context.commit('SET_JOB', resp.data)
      })
    }
  }
}
export default fuzz
