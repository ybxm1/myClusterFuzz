<template>
  <div class="target-info">
    <div class="info-header">设备信息</div>
    <div class="info-empty-label" v-if="info == ''"> 目前暂无设备信息 </div>
    <div class="info-labels" v-else >
      <record-item :record="formatedInfo"/>
    </div>
  </div>
</template>

<script>
import RecordItem from './RecordItem'

export default {
  props: {
    info: {
      type: String,
      default: ''
    }
  },
  computed: {
    formatedInfo() {
      return JSON.parse(this.info)
    }
  },
  components: {
    RecordItem
  }
}
</script>

<style lang="scss">
.target-info {
  position: relative;
  background-color: #292929;
  margin-top: 20px;
  margin-right: 10px;
  border-radius: $radius;
  width: 50%;
  box-shadow: 0px 0px 6px rgba(0,0,0,0.8);
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
    left: 42%;
  }
  .info-labels {
    padding: 18px 8px;
    overflow: auto;
    height: 600px;
    overflow-y: hidden;
  }
}
</style>

