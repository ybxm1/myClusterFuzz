import { mount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import App from '../App.vue'

test('App test', () => {
  const localVue = createLocalVue()

  localVue.use(VueRouter)
  const router = new VueRouter()
  const wrapper = mount(App, { localVue, router })
  console.log(wrapper)
})
