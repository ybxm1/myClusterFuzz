<template>
  <div class="ports-container">
    <div class="ports-item" v-if="hasTcpPorts">
      <span>TCP端口：</span>
      <span>{{ getTcpPort }}</span>
    </div>
    <div class="ports-item" v-if="hasUdpPorts">
      <span>UDP端口：</span>
      <span>{{ getUdpPort }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tcp: {
      type: Array,
      default: []
    },
    udp: {
      type: Array,
      default: []
    }
  },
  computed: {
    hasTcpPorts() {
      if (this.tcp.length == 0) return false;
      return true;
    },
    getTcpPort() {
      return this.tcp.join(', ')
    },
    hasUdpPorts() {
      if (this.udp.length == 0) return false;
      return true;
    },
    getUdpPort() {
      return this.udp.join(', ')
    }
  }
};
</script>

<style lang="scss">
.ports-container {
  margin-left: 36px;
  display: flex;

  .ports-item {
    margin-right: 18px;
  }
}
</style>

