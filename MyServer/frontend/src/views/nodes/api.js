import request from '@/utils/request'

export const getNodes = (page) => {
  return request.get(`/nodes/${page}`)  // post最后必须加/，否则后端会报308错误;get则不用加
}
