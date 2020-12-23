<template>
  <div class="case-select">
    <div class="case-select-title">待选择的用例</div>
    <div class="case-select-collapse">
      <el-collapse accordion>
        <el-collapse-item
          v-for="(cases, key) in $store.state.fuzz.cases"
          :key="key"
          :title="getTitle(key, cases)"
        >
          <div class="cases-item">
            <div v-if="cases.length!==0">
              <div v-for="(value, index) in cases" :key="value._id">
                <case-item :item="value" :index="index"/>
              </div>
            </div>
            <div v-else class="empty-cases">暂无测试用例</div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
import { PROTO_TITLE } from "@/views/fuzz/constants";
import CaseItem from "./CaseItem";
import { getJob, getCases } from "../api";
export default {
  data() {
    return {
      cases: []
    };
  },
  methods: {
    getTitle(key, item) {
      return `${PROTO_TITLE[key]}协议 (${item.length})`;
    }
  },
  components: {
    CaseItem
  },
  mounted() {
    this.$store.commit("EMPTY_SELECT"); // 清空之前的选择
  },
  beforeDestroy() {
    this.$store.commit("EMPTY_SELECT"); // 清空之前的选择
  }
};
</script>

<style lang="scss">
.case-select {
  color: $font_color;
  width: 50%;
  border-radius: $radius;
  border: 1px solid black;
  background-color: #4f4d4d;
  .case-select-title {
    font-size: 20px;
    text-align: center;
    height: 48px;
    line-height: 48px;
    border-bottom: 1px solid black;
    background-color: #403f3f;
    border-top-left-radius: $radius;
    border-top-right-radius: $radius;
  }
  .case-select-collapse {
    padding: 18px;

    .el-collapse {
      height: 55vh;
      overflow: auto;
      border: 0px;
      &::-webkit-scrollbar {
        width: 6px;
        height: 2px;
      }

      &::-webkit-scrollbar-thumb {
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 8px;
      }
      .el-collapse-item {
        margin: 8px;
        .el-collapse-item__header {
          color: $font_color;
          background-color: $dark_header;
          padding-left: 18px;
          border-bottom: 0px;
          border-radius: $radius;
          &.is-active {
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
          }
        }
        .el-collapse-item__wrap {
          background-color: #403f3f;
          border-bottom: 0px;
          border-bottom-left-radius: $radius;
          border-bottom-right-radius: $radius;
          .el-collapse-item__content {
            color: $font_color;
            padding-bottom: 0px;
            .cases-item {
              .empty-cases {
                text-align: center;
                padding: 10px 0;
              }
            }
          }
        }
      }
    }
  }
}
</style>

