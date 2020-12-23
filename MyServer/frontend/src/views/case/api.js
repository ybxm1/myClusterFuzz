import request from '@/utils/request'

export const getCases = (page, pageSize = 10) => {
  return request.get('/cases', { params: { page, pageSize } })
}

export const deleteCase = (id) => {
  return request.delete('/cases', { data: id })
}
