import request from '@/utils/request'

export const uplodaJobInfo = (formData) => {
  return request.post('/createjob/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data' 
    }
  })
}
