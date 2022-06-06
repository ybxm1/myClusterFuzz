import Vuex from 'vuex'
import Vue from 'vue'
import workstation from './workstation'
import fuzz from './fuzz'
import user from './user'
import jobs from './jobs'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: { 
    workstation,
    fuzz,
    user,
    jobs
  }
})

export default store
