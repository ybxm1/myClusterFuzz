<template>
  <div class="result-container">
    <div class="result-title">测试结果</div>
    <div class="result-collapse">
      <el-collapse>
        <el-collapse-item v-for="kase in allCases" :key="kase._id" :title="kase.title">
          <case-report :caseId="kase._id"/>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
import CaseReport from "./components/CaseReport";
export default {
  computed: {
    allCases() {
      if (!this.$store.state.fuzz.job) {
        return [];
      }
      return this.$store.state.fuzz.job.case;
    }
  },
  components: {
    CaseReport
  }
};
</script>

<style lang="scss" >
.result-container {
  color: $font_color;
  margin: 0 auto;
  width: 75%;
  border-radius: $radius;
  border: 1px solid black;
  background-color: #4f4d4d;
  .result-title {
    text-align: center;
    font-size: 20px;
    padding: 12px 0;
  }
  .result-collapse {
    padding: 18px;
    padding-top: 0px;
    .el-collapse {
      border-top: 0px;
      border-bottom: 0px;
      .el-collapse-item {
        margin: 8px;
        .el-collapse-item__header {
          color: $font_color;
          background-color: $dark_header;
          padding-left: 18px;
          border-bottom: 0px;
          border-radius: $radius;
          &.is-active {
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
          }
        }
        .el-collapse-item__wrap {
          background-color: #403f3f;
          border-bottom: 0px;
          border-bottom-left-radius: $radius;
          border-bottom-right-radius: $radius;
          .el-collapse-item__content {
            color: $font_color;
            padding-bottom: 0px;
            .cases-item {
              .empty-cases {
                text-align: center;
                padding: 10px 0;
              }
            }
          }
        }
      }
    }
  }
}
</style>

