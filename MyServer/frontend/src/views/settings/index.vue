<template>
  <div class="settings-container">
    <el-tabs type="border-card" v-model="currentTab">
      <el-tab-pane label="设置" name="settings">
        <div class="power">
          <div class="title">中继电源控制</div>
          <div class="control">
            <div class="item" v-for="item in plugs" :key="item.name">
              <span>控制器：{{item.name}}</span>
              <el-switch @change="changeHandle(item)" v-model="item.status" active-color="#06c0e1" inactive-color="#6f6e6e"></el-switch>
              <el-button @click="restart(item)">重启</el-button>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { changeStatus, getStatus } from './api'

export default {
  data() {
    return {
      currentTab: "settings",
      plugs: [
        { name:'s1', status: false },
        { name:'s2', status: false },
        { name:'s3', status: false },
        { name:'s4', status: false },
      ]
    };
  },
  methods: {
    changeHandle(item) {
      changeStatus(1, item.name[1], item.status).then(resp => {
        this.$message.info('切换成功')
      })
    },
    restart(item) {
      changeStatus(2, item.name[1], true).then(resp => {
        this.$message.info('重启成功')
      })
    }
  },
  mounted() {
    getStatus().then(resp => {
      this.plugs = resp.data
    })
  }
};
</script>

<style lang="scss">
.settings-container {
  padding: 20px;
  .el-tabs {
    border: 0px;
    .el-tabs__header {
      background-color: $common_bg;
      border-bottom: 1px solid $common_bg;
      .el-tabs__nav-wrap {
        .el-tabs__nav-scroll {
          .el-tabs__nav {
            #tab-settings {
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
  .power {
    color: $font_color;
    .title {
      margin-left: 24px;
      font-size: 20px;
      margin-bottom: 15px;
    }
    .control {
      display: flex;
      .item {
        border: 1px solid #363636;
        border-radius: $radius; 
        padding: 8px;
        margin: 0 16px;

        .el-button {
          padding: 6px 10px;
        }
      }
    }
  }
}
</style>

