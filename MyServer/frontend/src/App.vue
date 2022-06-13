<template>
  <transition name="fade">
    <router-view></router-view>
  </transition>
</template>

<script>

export default {
  name: 'app',
}
</script>


<style lang="scss">
body, html {
  margin: 0;
  height: 100%;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s;
}
.fade-enter, .fade-leave-to {  
  opacity: 0;
}
</style>

<!-- 启动命令：　npm run dev -->