<template>
  <div class="sub-record-container">
    <div class="proto-label">
      <span class="label">设备类型：</span>
      {{data['protocol']}}
      </div>
    <div class="date-label">
      <span class="label">扫描时间：</span>
      {{ formatedTime }}</div>

    <div class="date-label">
      <span class="label">状态:</span>
      {{ data['status'] }}</div>
    <div class="record-result" v-for="(value, key) in getResults" :key="key">
      <span class="label">{{ key }}：</span>
      {{ value }}
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  computed: {
    formatedTime() {
      return moment(this.data["timestamp"]).format("YYYY, MMMM Do, H:mm:ss");
    },
    getResults() {
      let results = {}
      for (let key in this.data["result"]) {
        let value = this.formatResult(this.data['result'][key])
        if (value === "") continue
        results[key] = value
      }
      return results
    }
  },
  methods: {
    formatResult(item) {
      if (!item) return ""
      if (typeof item === "boolean" || typeof item === "object") return ""
      if (item.length > 70) return item.slice(0, 70)
      return item
    }
  }
};
</script>

<style lang="scss" scoped>
.sub-record-container {
  color: $font_color;
  margin-left: 36px;
  &>div {
    margin-top: 18px;
  }
  .label {
    display: inline-block;
    width: 150px;
    color: #aaa;
  }
  .proto-label {
    font-weight: 400;
  }
  .record-result {
    color: $font_color;
    
  }
}
</style>
