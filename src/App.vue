<template>
  <router-view/>
</template>

<script>
export default {
  name: 'App'
}
</script>
<style>
/* 添加到全局样式或App.vue中 */
body.modal-open {
  overflow: hidden;
  position: fixed;
  width: 100%;
}
</style>