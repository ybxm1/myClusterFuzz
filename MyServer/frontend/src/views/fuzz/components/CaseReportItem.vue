<template>
  <div class="case-report-item">
    <div class="case-report-item-bar">
      <span>序号：{{ report.test_number }}</span>
      <span>协议：{{ getName }}</span>
      <span>进度：{{ getState }}</span>
      <span>状态：{{ getStatus }}</span>
      <span @click="showMore">
        <svg-icon icon="more" class="icon-more"/>
      </span>
      <span @click="download">
        <svg-icon icon="download" class="icon-download"/>
      </span>
    </div>

    <el-dialog title="详细信息" :visible.sync="showMoreDialog" width="70%">
      <div class="report-overview">
        <div class="overview-title">
          整体情况
        </div>
        <div>
          <span class="label">状态：</span>
          <span>{{ getStatus }}</span>
        </div>
        <div>
          <span class="label">原因：</span>
          <span>{{ getReason }}</span>
        </div>
        <div>
          <span class="label">模糊路径：</span>
          <span>{{ getFuzzPath }}</span>
        </div>
      </div>
      <div class="subreport" v-for="subReport in report.sub_reports" :key="subReport">
        <div class="subreport-title">{{base64ToString(report[subReport].name)}}</div>
        <div>
          <span class="label">status:</span>
          <span>{{base64ToString(report[subReport].status)}}</span>
        </div>
        <div v-for="(value, key) in filterSubReport(report[subReport])" :key="key">
          <span class="label">{{ key }}</span>
          <span>{{ value }}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { b64DecodeUnicode } from "@/utils/tools";
import { downloadPcap } from '../api';

export default {
  props: {
    report: {
      type: Object,
      required: true
    },
    id: {
      type: Number
    }
  },
  data() {
    return {
      showMoreDialog: false
    };
  },
  computed: {
    getName() {
      return window.atob(this.report.name);
    },
    getState() {
      return window.atob(this.report.state);
    },
    getStatus() {
      return window.atob(this.report.status);
    },
    getFuzzPath() {
      return b64DecodeUnicode(this.report.fuzz_path);
    },
    getReason() {
      return window.atob(this.report.reason);
    },
    getTraceback() {
      return window.atob(this.report.traceback);
    }
  },
  methods: {
    showMore() {
      this.showMoreDialog = true;
    },
    base64ToString(str) {
      return window.atob(str);
    },
    filterSubReport(subReport) {
      let newReport = {};
      for (let key in subReport) {
        if (typeof subReport[key] == "string") {
          newReport[key] = window.atob(subReport[key]);
        }
      }
      return newReport;
    },
    download() {
      // 下载指定的pcap
      let jobId = this.$route.params.id;
      let testId = this.id;
      window.open(`/workstation/download/${jobId}/${testId}`)
    }
  }
};
</script>

<style lang="scss">
.case-report-item {
  border: 1px solid $dark_header;
  border-top: 0;
  padding: 8px 16px;

  .label {
    display: inline-block;
    width: 25%;
    padding: 0 15px;
    border-right: 1px dashed black;
  }
  .case-report-item-bar {
    display: inline-block;
    span {
      padding-right: 16px;
    }
    .icon-more {
      width: 20px;
      height: 20px;
      cursor: pointer;
    }
    .icon-download {
      color: white;
      width: 20px;
      height: 20px;
      cursor: pointer;
    }
  }
  .el-dialog {
    background-color: #777575;
    .el-dialog__header {
      background-color: #393939;
      .el-dialog__title {
        color: $font_color;
      }
    }
    .el-dialog__body {
      color: $font_color;
      .report-overview {
        .overview-title {
          padding: 10px 15px;
          font-size: 14px;
          text-align: center;
          background-color: $dark_header;
        }
      }
      .subreport {
        margin-top: 16px;
        .subreport-title {
          padding: 10px 15px;
          font-size: 14px;
          text-align: center;
          background-color: $dark_header;
        }
      }
      div {
        border-left: 1px solid $dark_header;
        border-right: 1px solid $dark_header;
        border-bottom: 1px solid $dark_header;
      }
    }
  }
}
</style>
