<template>
  <div class="fuzz-container">
    <div class="fuzz-param">
      <div class="param-item">
        <span class="label">目标IP：</span>
        <el-input type="text" placeholder="192.168.1.1" v-model="params.TARGET_IP"/>
      </div>
      <div class="param-item">
        <span class="label">模糊次数：</span>
        <el-input type="text" placeholder="10" v-model="params.FUZZ_COUNT"/>
      </div>
      <div class="param-item">
        <span class="label">模糊间隔：</span>
        <el-input type="text" placeholder="1秒" v-model="params.DELAY"/>
      </div>
      <div class="control-item">
        <el-button v-if="isCompleted" @click="gotoResult">查看结果</el-button>
        <el-button v-else-if="isFuzzing">模糊测试中</el-button>
        <el-button v-else-if="isError" @click="viewErrMsg">测试出错</el-button>
        <el-button v-else @click="fuzzHandler">开始</el-button>
      </div>
    </div>
    <fuzz-status :delay="delay"/>
    <fuzz-progress/>
  </div>
</template>

<script>
import { startFuzz, getNetworkStatus } from "./api";
import { JobStatus } from "./constants";
import FuzzStatus from "./components/FuzzStatus";
import FuzzProgress from "./components/FuzzProgress";

export default {
  data() {
    return {
      jobId: null,
      params: {
        FUZZ_COUNT: 2,
        DELAY: 1,
        TARGET_IP: "192.168.1.173",
        TIME_OUT: 2
      },
      fuzzTimer: null,
      delay: 0 // 网络延迟，用于绘制网络延迟的点图
    };
  },
  computed: {
    isCompleted() {
      if (
        this.$store.state.fuzz.job &&
        this.$store.state.fuzz.job.status == JobStatus.FUZZ_COMPLETE
      ) {
        return true;
      }
      return false;
    },
    isFuzzing() {
      if (
        this.$store.state.fuzz.job &&
        this.$store.state.fuzz.job.status == JobStatus.FUZZING
      ) {
        return true;
      }
      return false;
    },
    isError() {
      if (
        this.$store.state.fuzz.job &&
        this.$store.state.fuzz.job.status == JobStatus.ERROR
      ) {
        return true;
      }
      return false;
    }
  },
  methods: {
    monitor() {
      let jobId = this.$route.params.id;
      this.$store.dispatch("loadSessionInfo", jobId);
      let job = this.$store.state.fuzz.job;
      if (job.status == JobStatus.FUZZ_COMPLETE) {
        window.clearInterval(this.fuzzTimer);
      }
      getNetworkStatus(jobId).then(response => {
        this.delay = response.data.delay;
      });
    },
    async fuzzHandler() {
      let jobId = this.$route.params.id;
      this.params["JOB_ID"] = jobId;
      try {
        await startFuzz(this.params);
      } catch (e) {
        this.$message.error("模糊测试启动失败");
      }

      this.fuzzTimer = setInterval(this.monitor, 1000);
    },
    gotoResult() {
      let jobId = this.$route.params.id
      this.$router.push({path:`/workstation/job/result/${jobId}`})
    },
    viewErrMsg() {
      let job = this.$store.state.fuzz.job
      this.$alert(job.error_msg, '错误相关信息', {
          confirmButtonText: '关闭',
        });
    }
  },
  beforeDestroy() {
    if (this.fuzzTimer) {
      window.clearInterval(this.fuzzTimer);
      this.fuzzTimer = null;
    }
  },
  async created() {
    let jobId = this.$route.params.id;
    try {
      await this.$store.dispatch("loadJob", jobId);
    } catch (e) {
      this.$message.error("url地址错误");
      this.$router.push("/");
    }
  },
  mounted() {
    let jobId = this.$route.params.id;
    this.$store.dispatch("loadJob", jobId).then(job => {
      if ('params' in job) {
        this.params = job.params;
      }
      if (job.status === JobStatus.FUZZING) {
        this.fuzzTimer = setInterval(this.monitor, 1000);
      }
    });
    this.$store.commit('SET_SESSION', null); // 初始化fuzz session状态
  },
  components: {
    FuzzStatus,
    FuzzProgress
  }
};
</script>

<style lang="scss" scoped>
.fuzz-container {
  color: $font_color;
  background-color: #4f4d4d;
  height: 100%;
  .fuzz-param {
    display: flex;
    background-color: $dark_header;
    height: 80px;
    .param-item {
      height: 40px;
      margin: auto 0;
      flex-grow: 0;
      display: flex;
      .label {
        line-height: 40px;
        vertical-align: middle;
        width: 100px;
        text-align: right;
      }
      &:first-child .label {
        width: 70px;
      }
      .el-input {
        width: 150px;
      }
    }
    .control-item {
      height: 40px;
      margin: auto 0;
      flex-grow: 1;
      text-align: right;
      margin-right: 16px;
      .el-button {
        color: $active_color;
      }
    }
  }
}
</style>
