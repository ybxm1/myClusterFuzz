<template>
  <div class="sidebar">
    <template v-for="routeItem in allRoutes">
      <side-bar-item :item="routeItem" :key="routeItem.name"/>
    </template>
  </div>
</template>

<script>
import { routes } from '@/router'
import SideBarItem from './SideBarItem'
export default {
  data() {
    return {
      routes
    }
  },
  methods: {
  },
  components: {
    SideBarItem
  },
  computed: {
    allRoutes() {
      return this.routes.filter(item => !item.hidden)
    },
    isActive() {
      this.$route
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebar {
  width: 240px;
  background-image: linear-gradient(to right, #393939, #2d2c2c 95%, #2d2c2c);
  display: flex;
  flex-direction: column;
  box-shadow: 0 0 6px 0 rgba(0,0,0,0.53);
  min-width: 240px;
}
</style>
