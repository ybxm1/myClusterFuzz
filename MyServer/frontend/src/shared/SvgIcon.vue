<template>
  <svg :class="svgClass" aria-hidden="true">
    <use :xlink:href="iconName"></use>
  </svg>
</template>

<script>
// svg use 解释 http://taye.me/blog/svg/a-guide-to-svg-use-elements/

// SvgIcon组件用于展示svg
export default {
  name: 'svg-icon',
  props: {
    icon: {
      type:String, 
      required: true,
    },
    className: {
      type:String
    }
  },
  computed: {
    iconName() {
      return `#icon-${this.icon}`
    },
    svgClass() {
      if (this.className) {
        return `svg-icon ${this.className}`
      }
      return 'svg-icon'
    }
  }
}
</script>

<style lang="scss">
.svg-icon {
  vertical-align: middle;
}
</style>
