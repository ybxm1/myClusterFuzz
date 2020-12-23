import request from '@/utils/request'
 
export const getCrashes_fixed = (page) => {
  return request.get(`/crashes/fixed/${page}`)  // post最后必须加/，否则后端会报308错误;get则不用加
}

export const getCrashes_unfixed = (page) => {
  return request.get(`/crashes/unfixed/${page}`)  
}

export const getCrashInfo = (name) => {
  return request.get(`/crashes/getsinglecrashinfo/${name}`)  
}