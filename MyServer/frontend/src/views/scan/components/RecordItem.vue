<template>
  <div class="record-container" v-if="shouldDisplay">
    <div class="ip-label">{{ record.ip }}</div>
    <div v-for="key in Object.keys(record.data)" :key="key">
      <sub-record-item :data="record.data[key]" />
    </div>
  </div>
</template>

<script>
import SubRecordItem from "./SubRecordItem";
import moment from "moment";

export default {
  props: {
    record: {
      type: Object,
      required: true
    }
  },
  created() {
    moment.locale("zh-cn");
  },
  methods: {
    formatDate(date) {
      return moment(date).format("YYYY, MMMM Do, H:mm:ss");
    }
  },
  computed: {
    shouldDisplay() {
      let successData = {};
      for (var val in this.record.data) {
        if (this.record.data[val].status === "success" || val == "BACnet") {
          successData[val] = this.record.data[val];
        }
      }
      if (Object.keys(successData).length === 0) return false;
      this.record.data = successData;
      return true;
    }
  },
  components: {
    SubRecordItem
  }
};
</script>

<style lang="scss" scoped>
.record-container {
  margin-bottom: 18px;
  padding-bottom: 18px;
  height: 100%;
  overflow: auto;
  &::-webkit-scrollbar {
    width: 4px;
    height: 2px;
  }

  &::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
  }
  .ip-label {
    margin-left: 36px;
    margin-top: 18px;
    font-size: 18px;
    color: $active_color;
    line-height: 20px;
  }
}
</style>

