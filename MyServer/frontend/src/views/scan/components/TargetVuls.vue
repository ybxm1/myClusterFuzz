<template>
  <div class="target-vuls">
    <div class="info-header">已知漏洞</div>
    <div class="info-empty-label" v-if="vuls.length === 0"> 暂无设备漏洞 </div>
    <div v-else class="info-vuls">
      <target-vuls-list :data="vuls" :height="600"/>
    </div>
  </div>
</template>

<script>
import TargetVulsList from './TargetVulsList'

export default {
  props: {
    vuls: {
      type: Array,
      default: []
    }
  },
  computed: {
    hasInfo() {
      if (!this.vuls) return false
      if (Object.keys(this.vuls).length == 0) return false
      return true
    },
    formatedInfo() {
      return JSON.parse(this.info)
    }
  },
  components: {
    TargetVulsList
  }
}
</script>

<style lang="scss">
.target-vuls {
  position: relative;
  box-shadow: 0px 0px 6px rgba(0,0,0,0.8);
  background-color: #292929;
  margin-top: 20px;
  margin-left: 10px;
  border-radius: $radius;
  width: 50%;
  .info-header {
    background-color: black;
    border-top-left-radius: $radius;
    border-top-right-radius: $radius;
    color: $font_color;
    height: 32px;
    text-align: center;
    line-height: 32px;
  }
  .info-empty-label {
    color: #aaa;
    position: absolute;
    top: 50%;
    left: 45%;
  }
  .info-vuls {
    padding: 16px;
  }
}
</style>

