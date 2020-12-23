import request from '@/utils/request'

export const getUsers = (page, pageSize = 10) => {
  return request.get('/login/users', { params: { page, pageSize } })
}
