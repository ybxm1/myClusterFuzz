<template>
  <div class="list-container-wrapper">
    <div class="list-container" :style="{height:getHeight}">
      <div class="list-item" v-for="vul in data" :key="vul['cnvd']" @click="() => handleClick(vul)">
        <span :class="getLevel(vul['level'][0])">{{ vul['level'][0] }}</span>
        <span class="product">{{ vul['title'] }}</span>
        <span class="date">{{ vul['submit_data'] }}</span>
        <transition name="fade">
          <div v-show="activeItem === vul['cve']">
            <table class="specifyTable">
              <colgroup>
                <col id="label">
                <col id="descript">
              </colgroup>
              <tr>
                <td class="key">CVE</td>
                <td class="value">{{ vul['cve'] }}</td>
              </tr>
              <tr>
                <td class="key">CNVD</td>
                <td class="value">{{ vul['cnvd'] }}</td>
              </tr>
              <tr>
                <td class="key">公开日期</td>
                <td class="value">{{ vul['submit_data'] }}</td>
              </tr>
              <tr>
                <td class="key">评分</td>
                <td class="value">{{ vul.score }}</td>
              </tr>
              <tr>
                <td class="key">危险级别</td>
                <td class="value">{{ vul['level'][0] }}</td>
              </tr>
              <tr>
                <td class="key">漏洞信息</td>
                <td class="value">{{ vul['description'] }}</td>
              </tr>
              <tr>
                <td class="key">解决方案</td>
                <td class="value">{{ vul['solve'] }}</td>
              </tr>
              <tr>
                <td class="key">补丁信息</td>
                <td class="value">{{ vul['patch'] }}</td>
              </tr>
              <tr>
                <td class="key">验证信息</td>
                <td class="value">{{ vul['verification'] }}</td>
              </tr>
              <tr>
                <td class="key">参考链接</td>
                <td class="value">{{ vul['link'] }}</td>
              </tr>
            </table>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    height: {
      type: Number,
      default: 300
    },
    data: {
      type: Array,
      default: []
    }
  },
  computed: {
    getHeight() {
      return `${this.height}px`;
    }
  },
  methods: {
    getLevel(level) {
      const levels = {
        高: "level-high",
        中: "level-middle",
        低: "level-low"
      };
      return levels[level] + " level";
    },
    handleClick(item) {
      if (item['CVE ID'] === this.activeItem) {
        this.activeItem = "";
      } else {
        this.activeItem = item['CVE ID'];
      }
    }
  },
  data() {
    return {
      activeItem: ""
    };
  }
};
</script>

<style lang="scss">
.list-container-wrapper {
  height: 100%;
  padding-top: 10px;
  .list-container {
    overflow: auto;
    &::-webkit-scrollbar {
      width: 4px;
      height: 2px;
    }

    &::-webkit-scrollbar-thumb {
      background-color: rgba(255, 255, 255, 0.1);
      border-radius: 8px;
    }
    .list-item {
      margin: 6px;
      border-radius: 8px;
      background-color: #000;
      line-height: 24px;
      color: white;
      padding: 8px;

      .level {
        vertical-align: middle;
        display: inline-block;
        height: 24px;
        width: 48px;
        margin-left: 18px;
      }
      .product {
        vertical-align: middle;
        text-align: left;
        font-size: 16px;
        display: inline-block;
        height: 24px;
        width: 350px;
        overflow: hidden;
      }
      .date {
        height: 24px;
        font-size: 14px;
        float: right;
      }
      .specifyTable {
        background-color: #000;
        word-wrap: break-word;
        word-break: break-all;
        #label {
          width: 10%;
        }
        .key {
          color: rgba(255, 255, 255, 0.7);
          text-align: right;
          font-weight: 600;
        }
        .value {
          padding-left: 10px;
          width: 50%;
          line-height: 130%;
          word-wrap: break-word;
        }
      }
    }
  }
}
.level-high {
  color: red;
}
.level-middle {
  color: orange;
}
.level-low {
  color: yellow;
}
</style>
