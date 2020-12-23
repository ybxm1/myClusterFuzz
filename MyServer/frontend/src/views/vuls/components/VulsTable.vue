<template>
  <div class="vuls-table-container">
    <div class="job-table">
      <el-table :data="vuls">
        <el-table-column prop="title" label="漏洞名称"></el-table-column>
        <el-table-column prop="收录时间" label="公布时间" width="220"></el-table-column>
        <el-table-column label="危险级别" width="200">
          <template slot-scope="scope" width="200">{{ scope.row['危害级别'][0] }}</template>
        </el-table-column>
        <el-table-column prop="score" label="评分" width="200"></el-table-column>
        <el-table-column prop="漏洞类型" label="类型" width="200">
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button @click="handleView(scope.row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog title="详细信息" :visible.sync="showDialog" width="50%">
      <div class="vul-container">
        <h3 class="vulTitle">{{ vul.title }}</h3>
        <table class="specifyTable">
          <colgroup>
            <col id="label">
            <col id="descript">
          </colgroup>
          <tr>
            <td class="key">CVE</td>
            <td class="value">{{ vul['CVE ID'] }}</td>
          </tr>
          <tr>
            <td class="key">CNVD</td>
            <td class="value">{{ vul['CNVD-ID'] }}</td>
          </tr>
          <tr>
            <td class="key">公开日期</td>
            <td class="value">{{ vul['收录时间'] }}</td>
          </tr>
          <tr>
            <td class="key">评分</td>
            <td class="value">{{ vul.score }}</td>
          </tr>
          <tr>
            <td class="key">危险级别</td>
            <td class="value">{{ getLevel }}</td>
          </tr>
          <tr>
            <td class="key">漏洞详情</td>
            <td class="value">{{ vul['漏洞描述'] }}</td>
          </tr>
          <tr>
            <td class="key">解决方案</td>
            <td class="value">{{ vul['漏洞解决方案'] }}</td>
          </tr>
          <tr>
            <td class="key">补丁信息</td>
            <td class="value">{{ vul['厂商补丁'] }}</td>
          </tr>
          <tr>
            <td class="key">验证信息</td>
            <td class="value">{{ vul['验证信息'] }}</td>
          </tr>
          <tr>
            <td class="key">参考链接</td>
            <td class="value">{{ vul['参考链接'] }}</td>
          </tr>
        </table>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  props: {
    vuls: {
      type: Array
    }
  },
  data() {
    return {
      vul: {},
      showDialog: false
    };
  },
  methods: {
    handleView(row) {
      this.vul = row;
      this.showDialog = true;
    }
  },
  computed: {
    getLevel() {
      if (typeof vul === 'undefined') return '低'
      if (vul['危害级别']) {
        return vul.level[0]
      }
      return '高'
    }
  }
};
</script>

<style lang="scss">
$--table-current-row-background-color: red;
.vuls-table-container {
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
  .el-dialog {
    background-color: #777575;
    .el-dialog__header {
      background-color: #393939;
      .el-dialog__title {
        color: $font_color;
      }
    }
    .el-dialog__body {
      color: $font_color;

      .vul-container {
        .vulTitle {
          text-align: center;
        }
        .specifyTable {
          width: 100%;
          margin-top: 10px;
          td {
            border-bottom: #000;
            padding: 23px 7px 2px 7px;
          }
        }
        #label {
          width: 15%;
        }
        .key {
          text-align: right;
          font-weight: 600;
        }
        .value {
          line-height: 130%;
        }
      }
    }
  }
}
</style>

