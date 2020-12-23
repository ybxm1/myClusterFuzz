import request from '@/utils/request'

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
