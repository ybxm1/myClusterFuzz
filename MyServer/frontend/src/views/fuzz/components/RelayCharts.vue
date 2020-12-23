<template>
  <div id="relay-echarts" class="relay-charts"></div>
</template>

<script>
import echarts from "echarts";
import { getNetworkStatus } from "../api";
import { setInterval } from "timers";
export default {
  props: {
    delayTime: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      delayTimes: [0, 0, 0, 0, 0, 0, 0, 0],
      dates: [],
      echart: null
    };
  },
  async mounted() {
    let orig_date = new Date();
    this.delayTimes.forEach(_ => {
      this.dates.push(orig_date.toLocaleTimeString());
      orig_date.setSeconds(orig_date.getSeconds() + 1);
    });

    let el = document.querySelector("#relay-echarts");
    this.echart = echarts.init(el);
    let jobId = this.$route.params.id;
    try {
      await this.$store.dispatch("loadJob", jobId);
    } catch (e) {
      this.$message.error("url地址错误");
      this.$router.push("/");
    }
    this.echart.setOption(this.opt);
  },
  watch: {
    delayTime: {
      handler: function(val) {
        this.delayTimes.shift();
        this.delayTimes.push(val);
        this.dates.shift();
        this.dates.push(new Date().toLocaleTimeString());
        this.echart.setOption(this.opt);
      }
    }
  },
  computed: {
    opt() {
      let option = {
        name: "设备网络状态",

        backgroundColor: "#4f4d4d",
        tooltip: {
          trigger: "axis"
        },
        grid: {
          top: "12%",
          left: "3%",
          right: "4%",
          bottom: "4%",
          containLabel: true
        },
        // animationDurationUpdate: function(idx) {
        //   // 越往后的数据延迟越大
        //   return idx * 10;
        // },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: this.dates,
          axisLabel: {
            textStyle: {
              color: "rgb(238, 238, 238,0.9)"
            }
          },
          axisLine: {
            lineStyle: {
              color: "rgb(238, 238, 238,0.9)"
            }
          }
        },
        yAxis: {
          name: "MS",
          type: "value",
          axisLabel: {
            formatter: "{value}",
            textStyle: {
              color: "rgb(238, 238, 238,0.9)"
            }
          },
          splitLine: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: "rgb(238, 238, 238,0.9)"
            }
          }
        },
        series: [
          {
            data: this.delayTimes,
            type: "scatter",
            color: "#eee",
            smooth: true,
            symbol: "circle",
            symbolSize: 20,
            itemStyle: {
              borderColor: "#000",
              borderWidth: 2
            }
          }
        ]
      };
      return option;
    }
  }
};
</script>

<style lang="scss" scoped>
.relay-charts {
  width: 550px;
  height: 350px;
}
</style>
