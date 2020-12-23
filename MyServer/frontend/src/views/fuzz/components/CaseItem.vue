<template>
  <div class="case-item" >
    <el-checkbox v-model="checked" @change="handleCheck"></el-checkbox>
    <span class="label" @click="itemHandleCheck">
      {{ index+1 }}
      .
      {{ item.title }}
    </span>
  </div>
</template>

<script>
export default {
  props: {
    item: {
      type: Object
    },
    index: {
      type: Number
    }
  },
  data() {
    return {
      checked: false
    }
  },
  methods: {
    handleCheck (checked) {
        if (checked) {
          this.$store.commit('SELECT_CASE', this.item)
          this.checked = true
        } else {
          this.$store.commit('REMOVE_CASE', this.item)
          this.checked = false
        }
    },
    itemHandleCheck () {
      if (this.checked) {
        this.$store.commit('REMOVE_CASE', this.item)
        this.checked = false
      } else {
        this.$store.commit('SELECT_CASE', this.item)
        this.checked = true
      }
    }
  },
  mounted () {
    this.$store.state.fuzz.selectCases.forEach(i => {
      if (i._id == this.item._id) {
        this.checked = true
        return
      }
    })
  }
}
</script>

<style lang="scss">
.case-item {
  border-bottom: 1px dotted black;
  .el-checkbox {
    margin-right: 12px;
  }
  cursor: pointer;
  padding: 8px 10px;
  overflow: hidden;
}
</style>

