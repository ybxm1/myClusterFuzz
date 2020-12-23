<template>
  <div class="layout">
    <layout-nav />
    <div class="main-layout">
      <layout-side-bar />
      <div class="app-main">
        <transition name="fade" mode="out-in">
          <router-view></router-view>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import LayoutNav from './components/Nav'
import LayoutSideBar from './components/SideBar'

export default {
  components: {
    LayoutNav,
    LayoutSideBar
  }
};
</script>

<style lang="scss" scoped>
.layout {
  height: 100%;
  background-color: #4F4E4E;
  .main-layout {
    display: flex;
    overflow: hidden;
    height: calc(100% - 100px);
    .app-main {
      height: 100%;
      width: calc(100% - 240px);
      overflow: auto;
    }
  }
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .25s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

</style>
