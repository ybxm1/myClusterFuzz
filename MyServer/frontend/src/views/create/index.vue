<template>
  <div class="job-container">
    <div class="body-container">
      <!--  
        <div class="title"> 
          <h3>创建任务</h3>
          <hr style="height:5px;border:none;border-top:5px solid #009deb;width:80%;margin-left:10%;margin-top:10px;"/>
        </div>
      -->
        <el-form class="createjob-form" :model="form" ref="createJobForm">
            <div class="title"> 
                <h3>创建任务</h3>
            </div>
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
                <!-- 不能使用el-input标签，会出错的 -->
              </div>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" style="width:80%;margin-left:10%;" @click.native.prevent="createjob">
                提交 
              </el-button>
            </el-form-item>
        </el-form>
    </div>
  </div>
</template>

<script>
import { uplodaJobInfo } from "./api"; 
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
      console.log(this.form.file)
      console.log(this.form.jobname)
      // formData = this.$refs.createJobForm; 直接引用form表单会造成TypeError: cyclic object value错误
      uplodaJobInfo(formData)
        .then(resp => {
          this.$message(resp.data.msg);  // 弹窗显示“任务创建从成功”
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



<style rel="stylesheet/scss" lang="scss" scoped>
$bg: #000;
$dark_gray: #889aa4;
$light_gray: #009deb;

.job-container {
  position: fixed;
  height: 100%;
  width: 100%;
  background: $common_bg;
  // background: white
}
.body-container{
  height: 75%;
  width:75%;
  text-align: center;
  margin-top: 50px;
  .title {
      font-size: 26px;
      font-weight: 400;
      color: $light_gray;
      margin-top: -25px;
      font-weight: bold;
  }
  .createjob-form {
      //position: absolute;
      //left: 0;
      //right: 0;
      width: 520px;
      padding: 25px 35px 5px 5px; //上右下左
      border-radius: 5px;
      margin-top: 10px;
      margin-left: 30%;
      //background: red;
      background:white;
      .el-input {
        display: inline-block;
        height: 100%;
        width: 100%;
      }
      .el-select {
        display: inline-block;
        height: 100%;
        width: 100%;
      }
      .el-form-item {
        border: 0px solid rgba(178, 178, 178, 0.4);
        // background: rgba(0, 0, 0, 0.1);
        background: white;
        border-radius: 5px;
        color: #454545;
      }
  }
  
}
</style>



