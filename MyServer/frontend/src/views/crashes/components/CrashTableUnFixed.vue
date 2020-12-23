<template>
<div class="vuls-table-container">
  <div class="job-table">
    <!-- 以表格的形式显示，任务ID、任务名、模糊器、节点数、运行时间（每个节点的fuzz）、任务创建时间、已发现漏洞数、任务完成度、运行日志信息链接 -->
    <el-table :data="data" :height="tableHeight" style="background-color:#393939;">
      <el-table-column prop="id" label="漏洞ID" ></el-table-column>
      <el-table-column prop="name" label="漏洞名" ></el-table-column>
      <el-table-column prop="jobid" label="任务ID" ></el-table-column>
      <el-table-column prop="findtime" label="发现时间" ></el-table-column>
      <el-table-column prop="isfix" label="是否已经修复" >
          <template slot-scope="scope"><font style="color:red;">{{ getIsfixed(scope.row) }}</font></template>
      </el-table-column>
      <el-table-column label="漏洞详细信息" >
          <template slot-scope="scope">
        　   <el-button @click="handleView(scope.row)">查看</el-button>
          </template>
      </el-table-column>
    </el-table>
  </div>

  <el-dialog title="漏洞信息" :visible.sync="showCrash" width="50%" class="result-collapse">
        <el-collapse>
        <el-collapse-item v-for="item in crashdata" :key="item.name" :title="item.name">
          <case-report>{{item.crash}}</case-report> <!-- Todo 无法显示换行符　-->
        </el-collapse-item>
      </el-collapse>
    </el-dialog>
</div>
</template>

<script>
// import { formatDate } from "@/utils/tools";
import { getCrashInfo } from "../api";
// import { JobStatus } from "@/views/fuzz/constants";

export default {
  props: {
    data: {
      type: Array,
      default: []
    }
  },
  computed: {
    tableHeight() {
      const navHeight = 200;
      const taskItemHeight = 137;
      const margin = 40;
      return (
        document.documentElement.clientHeight + 60 -
        navHeight -
        taskItemHeight -
        margin
      );
    }
  },
  data(){
    return {
      vul: {},
      showCrash: false,
      crashdata: [],
    };
  },
  methods: {
    handleView(row) {
      this.vul = row;
      this.showCrash = true;
      this.crashdata = [];
      getCrashInfo(row.name).then(resp => {
        this.crashdata = resp.data;
      });
    },
    getIsfixed(row) {
      if (row.isfix == 0) return "未修复"; // 设备扫描完成即是percent：100%
      if (row.isfix == 1) return "已修复"; 
      // if (!('completed' in job)) return 0;
      // return ((100 * job.completed) / job.case.length).toFixed(1); // 相对于用例数
    },
  }
};
</script>



<style lang="scss">
$--table-current-row-background-color: red;
.vuls-table-container {
  .job-table {
    .el-table {
      &::before {
        background-color: $component_bg;
      }
      th {
        background-color: rgb(36, 35, 35);
        &.is-leaf {
          border-bottom: 0px;
          border-left: 2px solid #424242;
          &:first-child {
            border-left: 0px;
          }
        }
      }
      tr {
        background-color: #575757;
        color: $font_color;
      }
      tr:hover > td {
        background-color: $component_bg;
      }
      td {
        border-bottom: 1px solid #777575;
      }
      .el-table__body-wrapper {
        background-color: $component_bg;
        height:100%;
        .el-table__empty-block {
          background-color: $component_bg;
          height:100%;
        }
      }
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
      height: 90%;
      .vul-container {
        .vulTitle {
          text-align: center;
        }
        .specifyTable {
          width: 100%;
          margin-top: 10px;
          td {
            border-bottom: #000;
            padding: 23px 7px 2px 7px;
          }
        }
        #label {
          width: 15%;
        }
        .key {
          text-align: right;
          font-weight: 600;
        }
        .value {
          line-height: 130%;
        }
      }
    }
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

