<template>
  <div class="job-table">
    <el-table :data="data" :height="tableHeight">
      <el-table-column prop="title" label="任务名" min-width="300"></el-table-column>
      <el-table-column label="完成度">
        <template slot-scope="scope">{{ getPercent(scope.row) }}</template>
      </el-table-column>
      <el-table-column prop="type" label="任务类型">
        <template slot-scope="scope">{{ getLabel(scope.row) }}</template>
      </el-table-column>
      <el-table-column prop="time" label="开始时间" min-width="200">
        <template slot-scope="scope">{{ formatTime(scope.row) }}</template>
      </el-table-column>
      <el-table-column prop="username" label="创建人"></el-table-column>
      <el-table-column label="操作" min-width="200">
        <template slot-scope="scope">
          <el-button @click="enterJob(scope.row)">进入任务</el-button>
          <el-button @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { formatDate } from "@/utils/tools";
import { deleteJob } from "../api";
import { JobStatus } from "@/views/fuzz/constants";

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
        document.documentElement.clientHeight -
        navHeight -
        taskItemHeight -
        margin
      );
    }
  },
  mounted() {
    this.$store
      .dispatch("reloadJobs")
      .catch(err => this.$message.error("服务器错误"));
  },
  methods: {
    getLabel(job) {
      return {
        1: "模糊测试",
        2: "漏洞扫描"
      }[job.type];
    },
    formatTime(job) {
      return formatDate(new Date(job.time * 1000));
    },
    getPercent(job) {
      if (this.status == 4) return 100; // 设备扫描完成即是percent：100%
      if (job.case.length == 0) return 0;
      if (!('completed' in job)) return 0;
      return ((100 * job.completed) / job.case.length).toFixed(1); // 相对于用例数
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

      .el-table__empty-block {
        background-color: $component_bg;
      }
    }
  }
}
</style>

