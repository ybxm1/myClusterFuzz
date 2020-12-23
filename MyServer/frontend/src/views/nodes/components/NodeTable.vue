<template>
  <div class="users-table">
    <el-table :data="data" >
      <el-table-column prop="id" label="节点ID" ></el-table-column>
      <el-table-column prop="name" label="节点名" ></el-table-column>
      <el-table-column prop="ip" label="ip地址" ></el-table-column>
      <el-table-column prop="men" label="内存大小" ></el-table-column>
      <el-table-column prop="corenum" label="核数" ></el-table-column>
      <el-table-column prop="isfree" label="是否空闲" ></el-table-column>
      <el-table-column prop="surplustime" label="剩余完成时间" ></el-table-column>
      <!-- 
      <el-table-column label="运行日志" >
          <template slot-scope="scope">
        　   <el-button @click="handleView(scope.row)">查看</el-button>
          </template>
      </el-table-column> 
      -->
    </el-table>
  </div>
</template>

<script>
export default {
  props: {
    data: {
      type: Array
    }
  },
  methods: {
    handleDelete() {
      
    }
  }
};
</script>

<style lang="scss">
$--table-current-row-background-color: red;
.users-table {
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
</style>

