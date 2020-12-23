import request from '@/utils/request'
 
export const getJobs_runing = (page) => {
  return request.get(`/joblist/runing/${page}`)  // post最后必须加/，否则后端会报308错误;get则不用加
}

export const getJobs_complete = (page) => {
  return request.get(`/joblist/complete/${page}`)  // 最后必须加/，否则后端会报308错误　
}

export const getJobLog = (id) => {
  return request.get(`/joblist/getjoblog/${id}`)  // 最后必须加/，否则后端会报308错误　
}

export const getCrashInfo = (id) => {
  return request.get(`/crashes/getcrashinfo/${id}`)  // 最后必须加/，否则后端会报308错误　
}