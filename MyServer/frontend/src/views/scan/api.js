import request from '@/utils/request'

export const scanTarget = (ip) => {
  return request.post('/scan_vuls/scan', {
    ip
  })
}

export const getTargetInfo = (jobId) => {
  return request.get(`/scan_vuls/result/${jobId}`)
}

export const getTargetVuls = (protocols) => {
  return request.post(`/scan_vuls/vuls`, {
    protocols
  })
}
