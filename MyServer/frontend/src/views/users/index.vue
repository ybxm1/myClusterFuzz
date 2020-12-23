<template>
  <div class="users-container">
    <el-tabs type="border-card" v-model="currentTab">
      <el-tab-pane label="用户管理" name="users">
        <user-table :users="users"/>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { getUsers } from "./api";
import UserTable from "./components/UserTable";
export default {
  data() {
    return {
      users: [],
      currentTab: "users"
    };
  },
  created() {
    getUsers(1).then(resp => {
      console.log(resp)
      this.users = resp.data.users;
    });
  },
  components: {
    UserTable
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
</style>

