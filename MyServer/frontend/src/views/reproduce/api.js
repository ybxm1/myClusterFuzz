import request from '@/utils/request'

export const createReproduce = (formData) => {
  return request.post('/reproduce/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data' 
    }
  })
}

export const getRep_runing = (page) => {
  return request.get(`/reproduce/runing/${page}`)  // post最后必须加/，否则后端会报308错误;get则不用加
}

export const getRep_complete = (page) => {
  return request.get(`/reproduce/complete/${page}`)  // 最后必须加/，否则后端会报308错误　
}





export const getJobs = () => {
  return request.get('/workstation/')
}

export const getJob = (id) => {
  return request.get(`/workstation/job/${id}`)
}

export const deleteJob = (id) => {
  return request.delete(`/workstation/job/${id}`)
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
