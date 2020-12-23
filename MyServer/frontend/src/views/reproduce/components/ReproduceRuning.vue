<template>
  <div class="job-table">
    <el-table :data="data" :height="tableHeight" style="background-color:#393939;">
      <el-table-column prop="id" label="ID" ></el-table-column>
      <el-table-column prop="name" label="任务名" ></el-table-column>
      <el-table-column prop="crashname" label="漏洞名" ></el-table-column>
      <el-table-column prop="createtime" label="任务创建时间" ></el-table-column>
    </el-table>
  </div>
</template>

<script>
// import { formatDate } from "@/utils/tools";
// import { deleteJob } from "../api";
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
        document.documentElement.clientHeight -
        navHeight -
        taskItemHeight -
        margin - 80
      );
    }
  },
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

