import request from '@/utils/request'

export const getVuls = (page, pageSize = 10) => {
  return request.get('/vuls/', { params: { page, pageSize } })
}

export const uploadFile = (formData) => {
  return request.post('/vuls/import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data' 
    }
  })
}

// export const onlineUpdate = () => {
//   return request.post('/vuls/online')
// }

// export const updateState = () => {
//   return request.get('/vuls/online')
// }
