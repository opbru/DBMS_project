<template>
    <div class="authenticated-layout">
      <router-view></router-view>
    </div>
  </template>

  <script>
  export default {
    name: 'AuthenticatedLayout',
  };
  </script>

  <style scoped>
  .authenticated-layout {
    padding: 20px;
  }
  </style>
