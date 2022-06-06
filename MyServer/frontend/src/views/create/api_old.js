import request from '@/utils/request'

export const uplodaJobInfo = (formData) => {
  return request.post('/createjob/', formData, {  // 通过import导入request库来实现将前端页面的数据传递给后端。
    headers: {
      'Content-Type': 'multipart/form-data' 
    }
  })
}
