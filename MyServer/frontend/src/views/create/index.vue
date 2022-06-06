<template>
  <div class="create">
    <div class="control-bar">
      <task-itemordinary name="普通模糊测试"/>
      <task-iteminteger name="集成模糊测试"/>
    </div>

    <div class="control-bar">
      <task-itemmix name="混合模糊测试"/>
      <task-itemtarget name="目标点模糊测试"/>
    </div>

    <create-integerfuzz />
    <create-mixfuzz />
    <create-ordinaryfuzz />
    <create-targetfuzz />
  </div>
</template>

<script>

import TaskItemordinary from './components/TaskItemordinary'
import TaskIteminteger from './components/TaskIteminteger'
import TaskItemmix from './components/TaskItemmix'
import TaskItemtarget from './components/TaskItemtarget'
import CreateIntegerfuzz from './components/CreateIntegerfuzz'
import CreateMixfuzz from './components/CreateMixfuzz'
import CreateOrdinaryfuzz from './components/CreateOrdinaryfuzz'
import CreateTargetfuzz from './components/CreateTargetfuzz'

export default {
  components: {
    TaskItemordinary,
    TaskIteminteger,
    TaskItemmix,
    TaskItemtarget,
    CreateIntegerfuzz,
    CreateMixfuzz,
    CreateOrdinaryfuzz,
    CreateTargetfuzz
  }
};
</script>



<style lang="scss" >
.create {
  .control-bar {
    display: flex;
    flex-direction: row;
    margin-top: 5%;
    margin-left: 20%;
  }
}

</style>
