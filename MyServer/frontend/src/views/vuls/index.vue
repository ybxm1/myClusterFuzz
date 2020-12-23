<template>
  <div class="vuls-container">
    <el-tabs type="border-card" v-model="currentTab">

      <div class="control-bar">
        <span>当前漏洞数量：</span>
        <span>{{ total }}</span>
        <span class="bar">
          <label for="file">选择漏洞文件上传</label>
          <input type="file" id="file" ref="file" @change="handleFileUpload()">
        </span>
        <span class="bar">
          <label @click="startOnlineUpdate">
            在线更新
            <svg-icon v-if="isUpdating" icon="loading" class="icon-loading"/>
          </label>
        </span> 
      </div>
     
      <el-tab-pane label="漏洞信息" name="vuls">
        <vuls-table :vuls="vuls"/>
        
        <div class="cases-pagination">
          <el-pagination
            :current-page="currentPage"
            @current-change="handlePageChange"
            layout="prev, pager, next"
            :total="total"
          ></el-pagination>
        </div>

      </el-tab-pane>
    
    </el-tabs>
  </div>
</template>

<script>
import { getVuls, uploadFile } from "./api";
import VulsTable from "./components/VulsTable";
import { clearInterval } from 'timers';

export default {
  data() {
    return {
      vuls: [],
      currentTab: "vuls",
      currentPage: 1,
      total: 0,
      updateTimer: null,
      isUpdating: false // 是否正在在线更新
    };
  },
  created() {
    getVuls(1).then(resp => {
      this.vuls = resp.data.vuls;
      this.total = resp.data.count;
    });
  },
  mounted() {
    this.updateTimer = setInterval(this.getUpdateState, 1000);
  },
  beforeDestroy() {
    if (this.updateTimer) {
      // clearInterval(this.updateTimer)
      this.updateTimer = null
    }
  },
  methods: {
    handlePageChange(page) {
      getVuls(page).then(resp => {
        this.vuls = resp.data.vuls;
        this.total = resp.data.count;
      });
    },
    handleFileUpload() {
      let formData = new FormData();  // 新建了一个form变量
      let file = this.$refs.file.files[0]; 
      formData.append("file", file);
      uploadFile(formData)
        .then(resp => {
          this.$message(resp.data.msg);
        })
        .catch(err => {
          console.log(err);
        });
    },
    startOnlineUpdate() {
      //onlineUpdate();
    },
    getUpdateState() {
      // updateState().then(resp => {
      //   let data = resp.data;
      //   if (data.status === "updating") {
      //     this.isUpdating = true;
      //   } else {
      //     this.isUpdating = false;
      //   }
      // });
    }
  },
  components: {
    VulsTable
  }
};
</script>

<style lang="scss">
.vuls-container {
  padding: 20px;
  .el-tabs {
    border: 0px;
    .el-tabs__header {
      background-color: $common_bg;
      border-bottom: 1px solid $common_bg;
      .el-tabs__nav-wrap {
        .el-tabs__nav-scroll {
          .el-tabs__nav {
            .el-tabs__item {
              font-size: inherit;
            }
            #tab-vuls {
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
    &:first-child {
      color: $active_color;
    }
    .bar {
      label {
        margin-left: 36px;
        color: $font_color;
        background-color: $dark_header;
        border-radius: $radius;
        display: inline-block;
        width: 180px;
        height: 36px;
        line-height: 36px;
        text-align: center;
        vertical-align: middle;
        &:active {
          color: #aaa;
          background-color: black;
        }
        .icon-loading {
          margin-left: 5px;
          margin-right: -5px;
          height: 25px;
          width: 25px;
          fill: $font_color;
          animation: rotation 2s linear infinite;
        }
        @keyframes rotation {
          from {
            transform: rotate(0);
          }
          to {
            transform: rotate(360deg);
          }
        }
      }
      input {
        width: 0.1px;
        height: 0.1px;
        opacity: 0;
        z-index: -1;
      }
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

