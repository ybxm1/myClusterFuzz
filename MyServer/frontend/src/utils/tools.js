export function formatDate (date) {
  var day = date.getDate()
  var monthIndex = date.getMonth()
  var year = date.getFullYear()
  var hour = date.getHours()
  var minute = date.getMinutes()
  return `${year}年 ${monthIndex + 1}月 ${day}日 ${hour}:${minute}`
}

export function b64DecodeUnicode (str) {
  // Going backwards: from bytestream, to percent-encoding, to original string.
  return decodeURIComponent(atob(str).split('').map(function (c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
  }).join(''))
}
