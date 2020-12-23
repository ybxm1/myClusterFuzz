<template>
  <div class="scan-container">
    <el-tabs type="border-card" v-model="currentTab">
      <el-tab-pane label="漏洞扫描" name="vulScan" :loading="true">
        <div class="control-bar">
          <span class="label">目标IP：</span>
          <el-input v-model="ip" placeholder="请输入目标IP"></el-input>
          <div class="control-item">
            <el-button class="scanning-button" @click="scaning">扫描</el-button>
          </div>
          <show-ports :tcp="tcpPorts" :udp="udpPorts"/>
        </div>
        <div class="scan-result-container">
          <target-info :info="scanResult" />
          <target-vuls :vuls="vuls"/>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { scanTarget, getTargetInfo, getTargetVuls } from './api.js'
import { modifyJob } from '@/views/workstation/api'
import { setTimeout } from 'timers'
import TargetInfo from './components/TargetInfo'
import TargetVuls from './components/TargetVuls'
import ShowPorts from './components/ShowPorts'

export default {
  data() {
    return {
      currentTab: "vulScan",
      ip: "",
      scanJobId: null, // 扫描任务的
      scanJobTimer: null,  // 扫描任务的定时器
      scanResult: '',
      loading: false,
      vuls: [],
      tcpPorts: [],
      udpPorts: []
    };
  },
  methods: {
    scaning() {
      if (this.ip === '') {
        this.$message.error('请填写目标ip地址')
        return 
      }
      let loading = this.$loading({
        lock: true,
        spinner: 'el-icon-loading',
        background: 'rgba(0,0,0,0.8)',
        target: document.querySelector('.scanning-button')
      })
      
      this.loading = loading
      scanTarget(this.ip).then(resp => {
        let jobId = resp.data.job
        this.scanJobId = jobId
        this.scanJobTimer = setTimeout(this.pullResult, 1000)
      })
    },
    pullResult() {
      getTargetInfo(this.scanJobId).then(resp => {
        console.log('resp:', resp)
        let protocols = {};
        if ('results' in resp.data) {
          this.scanResult = resp.data.results
          this.tcpPorts = resp.data.tcpPorts
          this.udpPorts = resp.data.udpPorts
          let jsonResult = JSON.parse(this.scanResult)
          let data = jsonResult['data']
          for (let key in data) {
            if (data[key]['status'] !== 'success') continue
            let info = data[key]['result']
            let protocol = data[key]['protocol']
            protocols[protocol] = info
          }
          getTargetVuls(protocols).then(resp => {
            this.vuls = resp.data.vuls
          })
          let fuzzJobId = this.$route.params.id;
          modifyJob(fuzzJobId, {status: 4, percentage: 100})
          this.loading.close()
        } else {
          this.scanJobTimer = setTimeout(this.pullResult, 1000)
        }
      }).catch((err) => {
        this.$message.error(err.msg)
        this.loading.close()
      })
    }
  },
  components: {
    TargetInfo,
    TargetVuls,
    ShowPorts
  }
};
</script>

<style lang="scss">
.scan-container {
  padding: 30px;
  .el-tabs {
    border: 0px;
    .el-tabs__header {
      background-color: $common_bg;
      border-bottom: 1px solid $common_bg;
      .el-tabs__nav-wrap {
        .el-tabs__nav-scroll {
          .el-tabs__nav {
            #tab-vulScan {
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
      padding: 20px;
      background-color: $component_bg;
    }
  }
  .control-bar {
    box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.8);
    background-color: #292929;
    width: 100%;
    height: 60px;
    line-height: 60px;
    border-radius: $radius;
    margin: auto 0px;
    flex-grow: 0;
    display: flex;
    color: $active_color;
    vertical-align: middle;
    .label {
      line-height: 60px;
      vertical-align: middle;
      width: 100px;
      text-align: right;
      margin-right: 20px;
    }
    .control-item {
      .el-loading-spinner {
        margin-top: -7px;
        i {
          color: $active_color;
        }
      }
    }
    .el-input {
      width: 200px;
    }

    .el-button {
      background-color: black;
      border: 3px solid black;
      margin-left: 18px;
      color: $active_color;
    }
  }
  .scan-result-container {
    height: 700px;
    display: flex;
  }
}
</style>
