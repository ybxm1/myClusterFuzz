<template>
  <div class="task-item">
    <div class="task-label">{{ name }}</div>
    <el-button @click="createTask">
      <svg-icon icon="plus" class="create-icon"/>创建
    </el-button>
  </div>
</template>

<script>
export default {
  props: {
    name: {
      type: String,
      required: true
    }
  },
  methods: {
    createTask() {
      this.$store.commit('CHANGE_CREA_DIALOG', true)
    }
  }
};
</script>

<style lang="scss" scoped>
.task-item {
  border-radius: 12px;
  text-align: center;
  background-color: $component_bg;
  color: $font_color;
  height: 136px;
  width: 246px;
  margin: 20px;
  .el-button {
    color: $font_color;
    width: 187px;
    height: 43px;
    font-size: 20px;
    background-color: $active_color;
    border-radius: 12px;
    outline:none; 
    border: 0;
    box-shadow: 0 2px 0 $active_color, 0 3px 20px rgba(0,0,0,0.3);
    :active {
      box-shadow: 0 1px 0 $active_color, 0 3px 8px rgba(0,0,0,0.2);
      position: relative;
      top: 3px;
    }
  }
  .task-label {
    padding-top: 23px;
    padding-bottom: 15px;
    font-size: 20px;
  }
  .create-icon {
    fill: $font_color;
    height: 23px;
    width: 23px;
    margin-right: 8px;
  }
}
</style>
