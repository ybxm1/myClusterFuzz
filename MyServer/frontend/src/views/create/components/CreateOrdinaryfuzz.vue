<template>
  <div class="create-dialog">
    <el-dialog
      :visible.sync="canOpen"
      :modal="true"
      :close-on-click-modal="false"
      width="40%"
    >
      <el-form ref="form" :model="form" label-width="80px"> <!-- border-radius="12px" 只对div元素才有用 -->
            <el-form-item>
              <div style="display:inline-block;width:55%;margin-left:170px;">
                <font size="6" color="#009deb">普通模糊测试</font>
              </div>
            </el-form-item>
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
                  <el-option label="AFLFAST" value="AFLFAST"></el-option>
                  <el-option label="FairFuzz" value="FairFuzz"></el-option>
                  <el-option label="Radamsa" value="Radamsa"></el-option>
                  <el-option label="Honggfuzz" value="Honggfuzz"></el-option>
                  <el-option label="Libfuzz" value="Libfuzz"></el-option>
                </el-select>
              </div>
            </el-form-item>
            <el-form-item>
              <div style="display:inline-block;width:25%;">
                <font>测试节点数量</font>
              </div>
              <div style="display:inline-block;width:70%;">
              <el-input name="botnum" v-model="form.botnum" type="text" />
              </div>
            </el-form-item>
            <el-form-item>
              <div style="display:inline-block;width:25%;">
                <font>测试时间</font>
              </div>
              <div style="display:inline-block;width:70%;">
              <el-input name="runtime" v-model="form.runtime" type="text" />
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
import { uplodaJobInfo } from "../api"; 

export default {
  data() {
    return {
      form: {
        jobname: null,
        fuzz: null,
        botnum: null,
        runtime: null,
        exec: null,
        file: null
      } 
    };
  },

  computed: {  // 会实时计算吗？就是当在state中将CHANGE_CREA_DIALOG的变量值修改后，这里会实时接收吗？这里是否是一个处于等待状态的线程？
    canOpen: {
      get() {
        return this.$store.state.workstation.createOrdinaryfuzz;
      },
      set(value) {
        this.$store.commit("CHANGE_CREA_DIALOG_ORDINARY", value);
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
      formData.append("botnum", this.form.botnum);
      formData.append("runtime", this.form.runtime);
      formData.append("exec", this.form.exec);
      formData.append("type", 1);
      // console.log(this.form.file)
      // console.log(this.form.jobname)
      // formData = this.$refs.createJobForm; 直接引用form表单会造成TypeError: cyclic object value错误
      uplodaJobInfo(formData)
        .then(resp => {
          this.$message(resp.data.msg);  // 弹窗显示“任务创建从成功”
          this.$store.commit("CHANGE_CREA_DIALOG_ORDINARY", false);
          this.$router.push({ path: "/joblist" });
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
