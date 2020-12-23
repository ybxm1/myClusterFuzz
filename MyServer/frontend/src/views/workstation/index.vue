<template>
  <div class="workstation">
    <div class="control-bar">
      <task-item name="工控设备检测"/>
      <!-- <task-item name="工控设备检测"/> -->
    </div>
    <div class="showArea">
      <el-tabs type="border-card" v-model="activeName">
        <el-tab-pane label="正在运行" name="running">
          <job-table :data="$store.getters.uncompletedJobs"/>
        </el-tab-pane>
        <el-tab-pane label="已完成" name="complete">
          <job-table :data="$store.getters.completedJobs"/>
        </el-tab-pane>
        <el-tab-pane label="发生错误" name="error">
          <job-table :data="$store.getters.errorJobs"/>
        </el-tab-pane>
      </el-tabs>
    </div>
    <create-dialog />
  </div>
</template>

<script>
import JobTable from './components/JobTable'
import TaskItem from './components/TaskItem'
import CreateDialog from './components/CreateDialog'
import { getJobs } from './api'
export default {
  data() {
    return {
      activeName: "running"
    };
  },
  components: {
    TaskItem,
    JobTable,
    CreateDialog
  },
  methods: {

  }
};
</script>

<style lang="scss">
.workstation {
  .control-bar {
    display: flex;
  }

  .showArea {
    margin: 0 20px 0 20px;

    .el-tabs--border-card {
      border: 0px;
      background-color: $component_bg;
      & > .el-tabs__header {
        background-color: #4f4e4e;
        border-bottom: 1px solid black;
        .el-tabs__item {
          &.is-active {
            color: $active_color;
            background-color: $component_bg;
            border-right-color: black;
            border-left-color: black;
          }
          :hover {
            color: $font_color;
          }
          font-size: 18px;
          border-radius: 8px 8px 0 0;
          color: $font_color;
          background-color: #848383;
          margin-right: 2px;
        }
      }
    }
  }
}
</style>
