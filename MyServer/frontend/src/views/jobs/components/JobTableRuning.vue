<template>
<div class="vuls-table-container">
  <div class="job-table">
    <!-- 以表格的形式显示，任务ID、任务名、模糊器、节点数、运行时间（每个节点的fuzz）、任务创建时间、已发现漏洞数、任务完成度、运行日志信息链接 -->
    <el-table :data="data" :height="tableHeight" style="background-color:#393939;">
      <el-table-column prop="id" label="任务ID" ></el-table-column>
      <el-table-column prop="name" label="任务名" ></el-table-column>
      <el-table-column prop="fuzzer" label="模糊器" ></el-table-column>
      <el-table-column prop="botnum" label="节点数" ></el-table-column>
      <el-table-column prop="time" label="运行时间" ></el-table-column>
      <el-table-column prop="createtime" label="任务创建时间" ></el-table-column>
      <el-table-column prop="crashnum" label="已发现漏洞数" ></el-table-column>
      <el-table-column prop="completenum" label="任务完成度" >
        　<template slot-scope="scope">{{ getPercent(scope.row) }}</template>
      </el-table-column>
      <el-table-column label="运行日志" >
          <template slot-scope="scope">
        　   <el-button @click="handleView(scope.row)">查看</el-button>
          </template>
      </el-table-column>
    </el-table>
  </div>

  <el-dialog title="日志信息" :visible.sync="showDialog" width="50%" class="result-collapse"> 
      <!-- <div class="" v-for="item in logdata" :key="item.name">
         <li>{{item.name}}</li>
         <li>{{item.log}}</li>
      </div>
      -->
      <el-collapse>
        <el-collapse-item v-for="item in logdata" :key="item.name" :title="item.name">
          <case-report>{{item.log}}</case-report> <!-- Todo 无法显示换行符　-->
        </el-collapse-item>
      </el-collapse>
     
</el-dialog>
</div>
</template>

<script>
// import { formatDate } from "@/utils/tools";
import { getJobLog } from "../api";
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
  // mounted() {
  //   this.$store
  //     .dispatch("reloadJobs")
  //     .catch(err => this.$message.error("服务器错误"));
  // },
  data(){
    return {
      vul: {},
      showDialog: false,
      logdata: []
    };
  },
  methods: {
    // getLabel(job) {
    //   return {
    //     1: "模糊测试",
    //     2: "漏洞扫描"
    //   }[job.type];
    // }, 
    // formatTime(job) {
    //   return formatDate(new Date(job.time * 1000));
    // },
    replace:function(str){
       return str.replace("/\n|\r\n/g", "<br/>");
    },
    handleView(row) {
      this.vul = row;
      this.showDialog = true;
      this.logdata = [];
      getJobLog(row.id).then(resp => {
        this.logdata = resp.data;
        // this.logdata.replace(/\n|\r\n/g,"<br/>"); 
        // var camelize = cached(function (str) {
        //   return str.replace(camelizeRE, function (_, c) { return c ? c.toUpperCase() : ''; })
        // });
 
        // this.logdata = this.replace(resp.data);
      });
    },
    
    getPercent(job) {
      // if (this.status == 4) return 100; // 设备扫描完成即是percent：100%
      // if (job.case.length == 0) return 0;
      // if (!('completed' in job)) return 0;
      // return ((100 * job.completed) / job.case.length).toFixed(1); // 相对于用例数
      return (job.completenum / job.botnum).toFixed(1)
    },
    enterJob(job) {
      if (job.type == 2) {
        // 2表示漏洞挖掘
        this.$router.push({
          path: `/workstation/scan/${job._id}`
        });
      } else {
        if (job.status == JobStatus.CREATED) {
          this.$router.push({
            path: `/workstation/job/case/${job._id}`
          });
        } else if (
          job.status == JobStatus.SELECTED_CASE ||
          job.status == JobStatus.FUZZING ||
          job.status == JobStatus.TO_FUZZ
        ) {
          this.$router.push({
            path: `/workstation/job/fuzz/${job._id}`
          });
        } else if (job.status == JobStatus.FUZZ_COMPLETE ||
          job.status == JobStatus.ERROR
        ) {
          this.$router.push({
            path: `/workstation/job/result/${job._id}`
          });
        } else {
          this.$router.push({
            path: "/404"
          });
        }
      }
    },
    
    handleDelete(job) {
      deleteJob(job._id).then(resp => {
        if (resp.status == 200) {
          this.$store.dispatch("reloadJobs").then(() => {
            this.$message.info("删除成功");
          });
        } else {
          this.$message.error("删除失败：", resp.msg);
        }
      });
    }
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

