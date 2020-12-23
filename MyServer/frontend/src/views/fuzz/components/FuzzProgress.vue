<template>
  <div class="fuzz-progress">
    <div class="label">测试进度</div>
    <el-progress :text-inside="true" :stroke-width="18" :percentage="percentage"></el-progress>
  </div>
</template>

<script>
export default {
  computed: {
    percentage() {
      let job = this.$store.state.fuzz.job
      if (job && !('completed' in job)) return 0;
      if (job && job.case && job.case.length != 0) return (100 * job.completed / job.case.length).toFixed(2)
      return 0
    }
  }
}
</script>

<style lang="scss" >
.fuzz-progress {
  height: 80px;
  background-color: $dark_header;
  display: flex;
  .label {
    width: 100px;
    margin-top: 31px;
    padding-left: 36px;
  }
  .el-progress {
    width: 90%;
    margin-top: 31px;
    
    .el-progress-bar__inner {
      background-color: $active_color;
    }
  }
}
</style>

