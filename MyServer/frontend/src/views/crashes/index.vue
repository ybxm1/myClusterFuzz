<template>
  <div class="workstation">
    <div class="showArea" >
      <el-tabs type="border-card" v-model="activeName">
        <el-tab-pane label="已修复" name="fixed" > <!-- @click.native="handlePageChange1(1)" -->
          <CrashTableFixed :data="fixedcrash"/> <!-- :data == v-bind:data -->
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
        
        <el-tab-pane label="未修复" name="unfixed">
          <CrashTableUnFixed :data="unfixedcrash"/>
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
  </div>
</template>

<script>
import CrashTableFixed from './components/CrashTableFixed'  
import CrashTableUnFixed from './components/CrashTableUnFixed' 
import { getCrashes_fixed, getCrashes_unfixed } from './api'
export default {
  data() {
    return {
      activeName: "fixed",
      fixedcrash: [],
      unfixedcrash: [],
      pagesize: 8,
      currentPage1: 1,
      total1: 0, 
      currentPage2: 1,
      total2: 0,
    };
  },
  components: {
    CrashTableFixed,
    CrashTableUnFixed
  },
  mounted(){
    this.handlePageChange1(1);
    this.handlePageChange2(1);
  },
  methods: {
    handlePageChange1(page) {
      getCrashes_fixed(page).then(resp => {
        this.fixedcrash = resp.data.data;
        this.total1 = resp.data.count;
      });
    },
    handlePageChange2(page) {
      getCrashes_unfixed(page).then(resp => {
        this.unfixedcrash = resp.data.data;
        this.total2 = resp.data.count;
      });
    },

  }
};
</script>



<style lang="scss">
.workstation {
  height: 95%;
  .control-bar {
    // display: flex;
  }

  .showArea {
    margin: 20px 20px 0 20px; // 上右下左
    height: 95%;
    .el-tabs--border-card {
      border: 0px;
      background-color: $component_bg;
      height: 100%;
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



