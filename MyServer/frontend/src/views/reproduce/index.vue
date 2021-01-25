<template>
  <div class="reproduce">
    <div class="control-bar">
      <task-item name="漏洞修复验证"/>
      <!-- <task-item name="工控设备检测"/> -->
    </div>
    <div class="showArea">
      <el-tabs type="border-card" v-model="activeName">
        <el-tab-pane label="正在运行" name="running">
          <reproduce-runing :data="runingRep"/>
          <div class="cases-pagination">
              <el-pagination
                :current-page="currentPage1"
                :page-size="pagesize"
                @current-change="handlePageChange1"
                layout="prev, pager, next"
                :total="total1"
              ></el-pagination>
          </div>
        </el-tab-pane>

        <el-tab-pane label="已完成" name="complete">
          <reproduce-completed :data="completedRep"/>
          <div class="cases-pagination">
              <el-pagination
                :current-page="currentPage2"
                :page-size="pagesize"
                @current-change="handlePageChange2"
                layout="prev, pager, next"
                :total="total2"
              ></el-pagination>
          </div>
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
import ReproduceRuning from './components/ReproduceRuning'
import ReproduceCompleted from './components/ReproduceCompleted'
import { getJobs, getRep_runing, getRep_complete } from './api'
export default {
  data() {
    return {
      activeName: "running",
      runingRep: [],
      completedRep: [],
      pagesize: 8,
      currentPage1: 1,
      total1: 0,
      currentPage2: 1,
      total2: 0,
    };
  },
  components: {
    TaskItem,
    JobTable,
    CreateDialog,

    ReproduceRuning,
    ReproduceCompleted
  },
  mounted(){
  //created(){
    this.handlePageChange1(1);
    this.handlePageChange2(1);
  },
  methods: {
    handlePageChange1(page) {
      getRep_runing(page).then(resp => {
        this.runingRep = resp.data.data;
        this.total1 = resp.data.count;
      });
    },
    handlePageChange2(page) {
      getRep_complete(page).then(resp => {
        this.completedRep = resp.data.data;
        this.total2 = resp.data.count;
      });
    },
  }
};
</script>

<style lang="scss" >
.reproduce {
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
.cases-pagination {
    margin-top: 5px;
    text-align: center;
    .btn-prev {
      background-color: $component_bg;
      color: $font_color;
    } // Todo 无法解决当页数为１的时候，左边的箭头背景呈现白色？？？
    .el-pager {
      li {
        background-color: $component_bg;
        &.btn-quicknext {
          color: $font_color;
        }
      }
      color: $font_color;
    }
    .btn-next {
      background-color: $component_bg;
      color: $font_color;
    }
  }
</style>
