import Vue from 'vue'
import SvgIcon from '@/shared/SvgIcon'

Vue.component('svg-icon', SvgIcon)
const svgReq = require.context('./svg', false, /\.svg$/)
svgReq.keys().map(svgReq)
