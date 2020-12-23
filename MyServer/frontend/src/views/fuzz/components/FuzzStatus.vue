<template>
  <div class="status-container">
    <div class="static-status">
      <div class="title">Linkstate 监视器</div>
      <div>
        <span class="label">用例数量:</span>
        <span class="value case-count">{{ caseCount }}</span>
      </div>
      <div>
        <span class="label">开始时间:</span>
        <span class="value case-date">{{ startTime }}</span>
      </div>
      <div class="label label-status">目标端口状态</div>
      <div class="net-status">
        <relay-charts :delayTime="delay"/>
      </div>
    </div>
    <online-status />
  </div>
</template>

<script>
import { formatDate } from "@/utils/tools"
import RelayCharts from './RelayCharts'
import OnlineStatus from './OnlineStatus'

export default {
  props: {
    delay: {
      type: Number,
      default: 0
    }
  },
  computed: {
    caseCount() {
      let job = this.$store.state.fuzz.job
      if (job && job.hasOwnProperty("case")) {
        return job.case.length
      }
      return 0
    },
    startTime() {
      let job = this.$store.state.fuzz.job;
      if (job && job.hasOwnProperty("start_time")) {
        return formatDate(new Date(job.start_time * 1000));
      }
      return "";
    }
  },
  components: {
    RelayCharts,
    OnlineStatus,
  }
};
</script>

<style lang="scss" scoped>
.status-container {
  display: flex;
  height: 100%;
  .static-status {
    width: 700px;
    padding: 16px 8px;
    margin-right: 20px;
    .title {
      text-align: center;
      margin-top: 8px;
    }
    .label {
      display: inline-block;
      width: 80px;
    }
    .label-id {
      width: 110px;
      padding-left: 8px;
    }
    .label-status {
      width: 110px;
      margin-top: 16px;
    }
    .value {
      margin: 8px 0;
      padding: 8px 8px;
      font-size: 13px;
      background-color: #403f3f;
      border-radius: $radius;
      border: 1px solid black;
      display: inline-block;
    }
    .case-count {
      display: inline-block;
    }
    .case-date {
      display: inline-block;
    }
    .net-status {
      width: 100%;
      height: 100%;
    }
  }
}
</style>

