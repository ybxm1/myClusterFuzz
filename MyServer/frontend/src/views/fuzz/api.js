import request from '@/utils/request'

export const getJob = (id) => {
  return request.get(`/workstation/job/${id}`)
}

export const modifyJob = (id, info) => {
  return request.post(`/workstation/job/${id}`, { data: info })
}

export const createJob = (job) => {
  return request.post('/workstation/', { data: job })
}

export const getCases = () => {
  return request.get('/workstation/cases')
}

export const startFuzz = (params, cases) => {
  return request.post('/workstation/fuzz', { params, cases })
}

export const getNetworkStatus = (id) => {
  return request.get(`/workstation/network_status/${id}`)
}

export const getFuzzStatus = (id) => {
  return request.get(`/workstation/fuzz_status/${id}`)
}

// 获取模糊测试kitty生成的用例信息，只有在发生错误的时候才有这个report
export const getReport = (jobId, caseId) => {
  return request.post('/workstation/report', {
    jobId,
    caseId
  })
}

// 下载这个任务
export const downloadPcap = (jobId, testId) => {
  return request.post('/workstation/download', {
    jobId,
    testId
  })
}
