<template>
  <div class="job-panel">
    <div class="job-title">
      <span @click="gotoHome">模糊测试</span>
      > 
      <span> {{ getTitle }} </span>
    </div>

    <div class="showArea">
      <el-steps :active="activeStep" finish-status="success">
        <el-step title="选择用例"></el-step>
        <el-step title="模糊测试"></el-step>
        <el-step title="测试结果"></el-step>
      </el-steps>
      <transition name="fade" mode="out-in">
        <router-view></router-view>
      </transition>
    </div>
  </div>
</template>

<script>
import CasePanel from "./CasePanel";
import FuzzPanel from "./FuzzPanel";
import { JobStatus } from './constants'
export default {
  methods: {
    gotoHome() {
      this.$router.push("/workstation");
    }
  },
  computed: {
    activePanel: {
      get() {
        return this.$store.state.fuzz.activeName;
      },
      set(value) {
        return this.$store.commit("CHANGE_FUZZ_PANEL", value);
      }
    },
    getTitle() {
      if (this.$store.state.fuzz.job) {
        return this.$store.state.fuzz.job.title;
      }
      return "";
    },
    activeStep() {
      if (!this.$store.state.fuzz.job) return 0
      let status = this.$store.state.fuzz.job.status;
      let statusToActive = {
        [JobStatus.CREATED]: 0,
        [JobStatus.SELECTED_CASE]: 1,
        [JobStatus.TO_FUZZ]: 1,
        [JobStatus.FUZZING]: 2,
        [JobStatus.FUZZ_COMPLETE]: 3
      }
      return statusToActive[status]
    }
  },
  async created() {
    let jobId = this.$route.params.id;
    await this.$store.dispatch("loadJob", jobId);
  },
  components: {
    CasePanel,
    FuzzPanel
  }
};
</script>

<style lang="scss">
.job-panel {
  padding: 20px 30px;
  .job-title {
    font-size: 20px;
    color: $font_color;
    padding-bottom: 20px;

    span {
      cursor: pointer;
    }
  }
  .showArea {
    background-color: $component_bg;
    padding: 18px;
    border-radius: $radius;
    .el-step {
      margin: 18px 0;
      .el-step__head.is-process {
        color: $active_color;
        border-color: $active_color;
        border-width: 2px;
      }
      .el-step__title.is-process {
        color: $active_color;
      }
    }
    }
  .icon-arrow {
    width: 70px;
    height: 70px;
    padding-top: 12%;
  }
  .case-container {
    display: flex;
  }
}
</style>

