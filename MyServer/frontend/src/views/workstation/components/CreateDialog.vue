<template>
  <div class="create-dialog">
    <el-dialog
      title="创建任务"
      :visible.sync="canOpen"
      :modal="true"
      :close-on-click-modal="false"
      width="40%"
    >
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="任务名称*">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="任务类型*">
          <el-select v-model="form.type" placeholder="请选择类型">
            <el-option label="模糊测试" value="1"></el-option>
            <el-option label="漏洞扫描" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="任务描述">
          <el-input type="textarea" :rows="4" v-model="form.description" placeholder="请输入任务描述"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="createAndGo">创建前往页面</el-button>
          <el-button type="primary" @click="create">创建并返回</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { createJob } from "../api";

export default {
  data() {
    return {
      form: {
        title: "",
        type: null,
        description: ""
      }
    };
  },
  computed: {
    canOpen: {
      get() {
        return this.$store.state.workstation.createDialog;
      },
      set(value) {
        this.$store.commit("CHANGE_CREA_DIALOG", value);
      }
    }
  },
  methods: {
    checkForm() {
      if (this.form.title === "") {
        this.$message("请输入任务名称")
        return false
      }
      if (!this.form.type) {
        this.$message("请选择任务类型")
        return false
      }
      return true
    },
    createAndGo() {
      if (!this.checkForm()) {
        return
      }
      let username = this.$store.state.user.name
      this.form.username = username
      createJob(this.form).then(response => {
        if (response.status == 201) {
          this.$store.dispatch("reloadJobs").then(() => {
            let jobId = response.data.job_id
            this.$message.success('创建任务成功！')
            if (this.form.type === '1') {
              this.$router.push(`/workstation/job/case/${jobId}`)
            } else {
              this.$router.push(`/workstation/scan/${jobId}`)
            }
          })
          
        } else {
          this.$message.error(response.statusText)
        }
        this.$store.commit("CHANGE_CREA_DIALOG", false);
      });
    },
    create() {
      if (!this.checkForm()) {
        return
      }
      createJob(this.form).then(response => {
        if (response.status == 201) {
          this.$store.dispatch("reloadJobs")
          this.$message.success('创建任务成功！')
        } else {
          this.$message.error(response.statusText)
        }
        this.$store.commit("CHANGE_CREA_DIALOG", false);
      });
    }
  }
};
</script>

<style>
</style>
