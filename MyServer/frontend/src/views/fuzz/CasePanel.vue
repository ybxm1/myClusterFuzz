<template>
  <div class="case-container">
    <case-select/>
    <svg-icon icon="arrow" class="icon-arrow"/>
    <case-has-select/>
  </div>
</template>

<script>
import CaseHasSelect from './components/CaseHasSelect'
import CaseSelect from './components/CaseSelect'
export default {
  components: {
    CaseHasSelect,
    CaseSelect
  },
  async created () {
    await this.$store
      .dispatch("loadCases")
      .catch(() => {
        this.$message.error("加载测试用例错误")
        this.$router.push("/")
      });

  }
};
</script>

<style>
</style>
