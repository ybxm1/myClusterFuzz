<template>
  <div class="job-table">
    <el-table :data="cases" >
      <el-table-column
        type="index"
        width="50">
      </el-table-column>
      <el-table-column prop="title" label="测试用例名称" width="380" :show-overflow-tooltip="true"></el-table-column>
      <el-table-column 
        prop="protocol" 
        label="测试协议"  
        width="120"
        :filters="filters"
        :filter-method="filterHandle"
      >
        <template slot-scope="scope">
          {{ convert(scope.row) }}
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="150"></el-table-column>
      <el-table-column prop="creator" label="创建人" width="100"></el-table-column>
      <el-table-column prop="des" label="详情" :show-overflow-tooltip="true" ></el-table-column>
      <el-table-column label="操作" width="100">
        <template slot-scope="scope">
          <el-button @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { Filters, PROTO_MAP } from './contants'
import { deleteCase } from '../api'
export default {
  props: {
    cases: {
      type: Array
    }
  },
  methods: {
    handleDelete(row) {
      deleteCase(row['_id']).then(_ => {
        this.$message('删除成功')
        this.$emit('delete-case', row['_id'])
      }).catch(err => {
        console.log(err)
      })
    },
    filterHandle(value, row, column) {
      const property = column['property'];
      return row[property] === value;
    },
    convert(row) {
      return PROTO_MAP[row['protocol']];
    }
  },
  data: function(){
    return {
      filters: Filters
    }
  }
};
</script>

<style lang="scss">
$--table-current-row-background-color: red;
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
      .highlight {
        color: $active_color;
        .el-table__column-filter-trigger {
          .el-icon-arrow-down {
            color: $active_color;
            font-size: 16px;
          }
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

