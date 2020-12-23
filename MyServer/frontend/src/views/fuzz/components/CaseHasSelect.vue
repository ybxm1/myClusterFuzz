<template>
  <div class="select-container">
    <div class="case-has-select">
      <div class="case-select-title">已选择用例</div>
      <div class="case-select-items">
        <div v-for="item in $store.state.fuzz.selectCases" :key="item._id" class="select-case">
          {{ getInfo(item) }}
        </div>
      </div>
    </div>
    <div class="start-fuzz">
      <el-button @click="goToFuzz">挖掘界面</el-button>
    </div>
  </div>
</template>

<script>
import { PROTO_TITLE } from "@/views/fuzz/constants";

export default {
  methods: {
    getInfo(item) {  // 标题信息
      return `${PROTO_TITLE[item.protocol]}  >  ${item.title}`;
    },
    goToFuzz() {
      if (this.$store.state.fuzz.selectCases.length == 0) {
        this.$message.error('请选择测试用例')
        return
      }
      let jobId = this.$route.params.id
      this.$store.dispatch('saveSelectCases').then(()=> {
        this.$router.push({ path: `/workstation/job/fuzz/${jobId}`})
      })
    }
  }
};
</script>

<style lang="scss" scoped>
.select-container {
  width: 50%;
  display: flex;
  flex-direction: column;
  .case-has-select {
    flex-grow: 1;
    width: 100%;
    color: $font_color;
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
    .case-select-items {
      padding: 18px;
      .select-case {
        margin: 8px;
        padding: 8px 8px;
        font-size: 13px;
        background-color: #403f3f;
        border-radius: $radius;
        border: 1px solid black;
      }
    }
  }
  .start-fuzz {
    flex-grow: 0;
    text-align: right;
    padding-top: 15px;
  }
}
</style>
