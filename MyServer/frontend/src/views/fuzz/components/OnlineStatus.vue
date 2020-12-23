<template>
  <div class="online-status">
    <div class="title">测试用例执行情况及状态</div>
    <div class="row">
      <span class="label">当前用例：</span>
      <span>{{ currentCase }}</span>
    </div>
    <div class="row">
      <span>剩余时间：</span>
      <span>{{ eta }}</span>
    </div>
    <div class="row progess">
      <span class="progress-label">当前进度：</span>
      <el-progress :stroke-width="8" :percentage="percent" :show-text="false"></el-progress>
    </div>
    <div class="row">
      <span>当前报文：</span>
      <span class="packet">{{ packet }}</span>
    </div>
    <div class="row">
      <span>报文长度：</span>
      <span>{{ packetLength }} 字节</span>
    </div>
    <div class="row">
      <span>随机种子：</span>
      <span>{{ seed }}</span>
    </div>
    <div class="row">
      <span>变异次数：</span>
      <span>{{ mutation }}</span>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    currentCase() {
      let job = this.$store.state.fuzz.job;
      if (job && job.hasOwnProperty("current")) {
        return job.current;
      }
      return "还未开始测试";
    },
    eta() {
      let sessionInfo = this.$store.state.fuzz.sessionInfo;
      if (!sessionInfo) return "??";
      let currentIndex = sessionInfo.current_index;
      if (!currentIndex) return "??";
      let startTime = sessionInfo.start_time;
      let startIndex = sessionInfo.start_index;
      let endIndex = sessionInfo.end_index;
      let currentTime = new Date().getTime(); // 因为获取的是毫秒级别的所以要除以1000
      currentTime /= 1000;
      let remainTime =
        ((currentTime - startTime) / (currentIndex - startIndex)) *
        (endIndex - currentIndex);
      let hour = parseInt(remainTime / 3600);
      let minute = parseInt(remainTime / 60 - hour * 60);
      let second = parseInt(remainTime % 60);
      return `${hour}小时 ${minute}分钟 ${second}秒`;
    },
    percent() {
      let sessionInfo = this.$store.state.fuzz.sessionInfo;
      if (!sessionInfo) return 0;
      return parseFloat(
        ((sessionInfo.current_index * 100) / sessionInfo.end_index).toFixed(2)
      );
    },
    packet() {
      let sessionInfo = this.$store.state.fuzz.sessionInfo;
      if (!sessionInfo) return "";
      let volatile = sessionInfo.volatile;
      let value = volatile.test_info.node.field.value;
      return value.rendered.base64;
    },
    packetLength() {
      let sessionInfo = this.$store.state.fuzz.sessionInfo;
      if (!sessionInfo) return "";
      let volatile = sessionInfo.volatile;
      let value = volatile.test_info.node.value;
      return value.rendered.length_in_bytes;
    },
    seed() {
      let sessionInfo = this.$store.state.fuzz.sessionInfo;
      if (!sessionInfo) return 0;
      let volatile = sessionInfo.volatile;
      let field = volatile.test_info.node.field;
      return field.seed;
    },
    mutation() {
      let sessionInfo = this.$store.state.fuzz.sessionInfo;
      if (!sessionInfo) return "";
      let mutation = sessionInfo.volatile.template_info.mutation;
      return `${mutation.current_index} / ${mutation.total_number}`;
    }
  }
};
</script>

<style lang="scss" >
.online-status {
  width: 100%;
  margin: 16px;
  background-color: $component_bg;
  border: 1px solid black;
  border-radius: $radius;
  padding: 8px 16px;
  .title {
    color: #999;
    text-align: center;
  }
  .row {
    span {
      &:first-child {
        color: #999;
      }
    }
    .packet {
      word-break: break-all;
    }
    margin: 20px 0;
  }
  .progess {
    display: flex;
    .progress-label {
      width: 100px;
    }
    .el-progress {
      width: 100%;
      .el-progress-bar {
        margin-top: 7px;
        .el-progress-bar__inner {
          background-color: $active_color;
        }
      }
    }
  }
}
</style>

