<template>
  <div class="create-dialog">
    <el-dialog

      :visible.sync="canOpen"
      :modal="true"
      :close-on-click-modal="false"
      width="40%"
    >
      <el-form ref="form" :model="form" label-width="80px">

        <el-form-item>
              <div style="display:inline-block;width:25%;">
                <font>任务名称</font>
              </div>
              <div style="display:inline-block;width:70%;">
                <el-input name="jobname" v-model="form.jobname" type="text"/>
              </div>
            </el-form-item>

            <el-form-item>
              <div style="display:inline-block;width:25%;">
                <font>模糊器</font>
              </div>
              <div style="display:inline-block;width:70%;">
              <el-select name="fuzz" v-model="form.fuzz" placeholder="请选择模糊器">
                <el-option label="AFL" value="AFL"></el-option>
                <el-option label="Honggfuzz" value="Honggfuzz"></el-option>
                <el-option label="Libfuzz" value="Libfuzz"></el-option>
              </el-select>
              </div>
            </el-form-item>

            <el-form-item>
              <div style="display:inline-block;width:25%;">
                <font>漏洞名称</font>
              </div>
              <div style="display:inline-block;width:70%;">
              <el-input name="crashname" v-model="form.crashname" type="text" />
              </div>
            </el-form-item>

            <el-form-item>
              <div style="display:inline-block;width:25%;">
                <font>可执行文件名</font>
              </div>
              <div style="display:inline-block;width:70%;">
              <el-input name="exec" v-model="form.exec" type="text" />
              </div>
            </el-form-item>

            <el-form-item>
              <div style="display:inline-block;width:25%;">
                <font>上传待测组件</font>
              </div>
              <div style="display:inline-block;width:70%;">
                <input type="file" id="file" ref="file" @change="getFile()">
                <!-- 不能使用el-input标签，会出错的 -->
              </div>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" style="width:80%;margin-left:10%;" @click.native.prevent="createjob">
                提交 
              </el-button>
            </el-form-item>
      </el-form>

    </el-dialog>
  </div>
</template>

<script>
import { createReproduce } from "../api";

export default {
  data() {
    return {
      form: {
        jobname: null,
        fuzz: null,
        crashname: null,
        exec: null,
        file: null
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
    getFile(event){
      let file = this.$refs.file.files[0];   // 通过设置refs来引用html中变量的值，或者使用this来引用data中的值
      this.form.file = file;
    },
    createjob(){
      let formData = new FormData();
      formData.append("file", this.form.file);
      formData.append("jobname", this.form.jobname);
      formData.append("fuzz", this.form.fuzz);
      formData.append("crashname", this.form.crashname);
      formData.append("exec", this.form.exec);
      console.log(this.form.file)
      console.log(this.form.jobname)
      // formData = this.$refs.createJobForm; 直接引用form表单会造成TypeError: cyclic object value错误
      createReproduce(formData).then(resp => {
          this.$message(resp.data.msg);
          this.$store.commit("CHANGE_CREA_DIALOG", false);
          this.$router.push({ path: "/reproduce" });
        })
        .catch(err => { // Todo 错误信息显示
          this.$message(err.data.msg);
          console.log(err);
        });
    }

  }
};
</script>

<style>
</style>
