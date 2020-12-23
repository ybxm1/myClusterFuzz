import request from '@/utils/request'

export const changeStatus = (type, id, status) => {
  return request.post('/settings/power', { type, id, status })
}

export const getStatus = () => {
  return request.get('/settings/power')
}
