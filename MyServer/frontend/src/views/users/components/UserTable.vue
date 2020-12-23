<template>
  <div class="users-table">
    <el-table :data="users" >
      <el-table-column prop="id" label="节点id" width="300" :show-overflow-tooltip="true"></el-table-column>
      <el-table-column prop="name" label="节点名称" width="100"></el-table-column>
      <el-table-column prop="ip" label="创建时间" width="150"></el-table-column>
      <el-table-column prop="description" label="详情" :show-overflow-tooltip="true" ></el-table-column>
      <el-table-column label="操作" width="140">
        <template slot-scope="scope">
          <el-button @click="handleDelete(scope.row)">查看</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  props: {
    users: {
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

