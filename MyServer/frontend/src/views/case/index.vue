<template>
  <div class="cases-container">
    <el-tabs type="border-card" v-model="currentTab">
      <el-tab-pane label="测试用例" name="cases">
        <div class="control-bar">
          <span>当前测试用例数量：</span>
          <span>{{ total }}</span>
        </div>
        <case-table @delete-case="deleteHandle" :cases="cases"/>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { getCases } from "./api"; 
import CaseTable from "./components/CaseTable";
export default {
  data() {
    return {
      cases: [],
      currentTab: "cases",
      currentPage: 1,
      total: 0
    };
  },
  created() {
    getCases(1).then(resp => {
      this.cases = resp.data.cases;
      this.total = resp.data.count;
    });
  },
  methods: {
    handlePageChange(page) {
      getCases(page).then(resp => {
        this.cases = resp.data.cases;
        this.total = resp.data.count;
      });
    },
    deleteHandle(id,v) {
      this.cases = this.cases.filter(i => i['_id'] != id)
      this.total -= 1;
    }
  },
  components: {
    CaseTable
  }
};
</script>

<style lang="scss">
.cases-container {
  padding: 20px;
  .el-tabs {
    border: 0px;
    .el-tabs__header {
      background-color: $common_bg;
      border-bottom: 1px solid $common_bg;
      .el-tabs__nav-wrap {
        .el-tabs__nav-scroll {
          .el-tabs__nav {
            #tab-cases {
              font-size: 16px;
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
  .control-bar {
    margin-bottom: 16px;
    margin-left: 4px;
    &:first-child {
      color: $active_color;
    }
  }
  .cases-pagination {
    text-align: center;
    .btn-prev {
      background-color: $component_bg;
      color: $font_color;
    }
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
}
</style>

