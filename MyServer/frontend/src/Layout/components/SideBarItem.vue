<template>
  <div :class="{active: isActive, 'sidebar-item': true}">
    <router-link :to="item.path" class="sidebar-href">
      <svg-icon :icon="item.icon" class="sidebar-icon"/>
      <div>{{ item.name }}</div>
    </router-link>
  </div>
</template>

<script>
export default {
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  computed: {
    isActive() {
      return this.$route.path.indexOf(this.item.path) == 0
    }
  }
};
</script>

<style lang="scss" scoped>

.sidebar-item {
  :hover {
    background-color: $component_bg;
  }
  
  .sidebar-href {
    text-decoration: none;
    vertical-align: middle;
    line-height: 35px;
    font-size: 20px;
    color: $font_color;
    display: flex;
    padding: 20px 25px;

    .sidebar-icon {
      fill: $font_color;
      height: 35px;
      width: 35px;
      margin-right: 25px;
    }
  }
}
.active {
  .sidebar-href {
    color: $active_color;
    .sidebar-icon {
      fill: $active_color;
    }
  }
}
</style>

