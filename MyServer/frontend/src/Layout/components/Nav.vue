<template>
  <nav>
    <div class="left">
      <svg-icon icon="logo" class="icon icon-logo"/>
      <h1>杭州电子科技大学</h1>
    </div>

    <div class="middle"></div>
    <div class="right">
      <span class="username">{{ $store.state.user.name }}</span>
      <el-dropdown @command="doCommand">
          <svg-icon icon="settings" className="icon icon-right"/>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="settings">设置</el-dropdown-item>
          <el-dropdown-item command="logout">退出登陆</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </nav>
</template>

<script>
import "@/icons/svg/logo.svg";

export default {
  methods: {
    doCommand(command) {
      if (command === 'logout') {
        this.$store.dispatch('LogOut').then(() => {
          this.$router.push({ path: '/login' })
        })
        return
      } else if (command === 'settings') {
        this.$router.push({ path: '/settings'})
      }
    }
  }
};
</script>

<style lang="scss" scoped>
nav {
  display: flex;
  flex-flow: columns;
  background-image: linear-gradient(to bottom, #1c1c1c, #131313 95%, #131313);
  height: 100px;
  .icon {
    width: 100px;
    cursor: pointer;
    fill: #eee;
  }
  .left {
    display: flex;
    flex-flow: columns;
    width: 300px;
    min-width: 300px;
    max-width: 300px;
    flex-grow: 0;
    .icon-logo {
      height: 60px;
      margin-top: 20px;
    }
    h1 {
      cursor: pointer;
      width: 200px;
      margin: 0;
      line-height: 100px;
      color: #eee;
      font-family: "Arial", "Microsoft YaHei", "黑体", "宋体", sans-serif;
    }
  }
  .middle {
    flex-grow: 1;
    width: auto;
  }
  .right {
    display: flex;
    justify-content: flex-end;
    width: 300px;
    min-width: 300px;
    max-width: 300px;
    flex-grow: 0;
    .username {
      color: $font_color;
      vertical-align: middle;
      line-height: 100px;
    }
    .icon-right {
      height: 40px;
      margin-top: 30px;
    }
  }
}
.el-dropdown-menu {
  background-color: #393939;
  border: 1px solid black;
  .el-dropdown-menu__item {
    color: $font_color;
    &:hover {
      background-color: $common_bg;
      color: black;
    }
  }
}
</style>
                                                       