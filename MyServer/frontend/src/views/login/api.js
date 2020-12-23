import request from '@/utils/request'

export const login = (username, password) => {
  return request.post('/user/login', {
    username,
    password
  })
}

// export const register = (username, password, info) => {
//   return request.post('/login/register', {
//     username,
//     password,
//     info
//   })
// }

export const getInfo = (token) => {
  return "admin"
  // return request.post('/login/info', {
  //   token
  // })
}
