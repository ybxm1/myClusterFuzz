<template>
  <div class="users-container">
    <el-tabs type="border-card" v-model="currentTab">
      <el-tab-pane label="节点信息" name="users">
        <node-table :data="nodes"/>

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
    </el-tabs>
  </div>
</template>

<script>
import { getNodes } from "./api";
import NodeTable from "./components/NodeTable";
export default {
  data() {
    return {
      nodes: [],
      users:[],
      currentTab: "users",
      pagesize: 8,
      currentPage1: 1,
      total1: 0,
    };
  },
  created() {
    this.handlePageChange1(1);
  },
  components: {
    NodeTable
  },
  methods: {
    handlePageChange1(page) {
      getNodes(page).then(resp => {
        this.nodes = resp.data.data;
        this.total1 = resp.data.count;
      });
    },
  }
};
</script>

<style lang="scss">
.users-container {
  padding: 20px;
  .el-tabs {
    border: 0px;
    .el-tabs__header {
      background-color: $common_bg;
      border-bottom: 1px solid $common_bg;
      .el-tabs__nav-wrap {
        .el-tabs__nav-scroll {
          .el-tabs__nav {
            #tab-users {
              color: $active_color;
              background-color: $component_bg;
              border-top-left-radius: $radius;
              border-top-right-radius: $radius;
              border-right-color: $common_bg;
              border-left-color: $common_bg;
            }
          }
        }
      }
    }
    .el-tabs__content {
      padding: 15px;
      background-color: $component_bg;
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

