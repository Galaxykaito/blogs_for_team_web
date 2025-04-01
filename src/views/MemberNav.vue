<template>
  <div class="nav-sidebar">
    <div
      v-for="tab in tabs"
      :key="tab.id"
      class="nav-item"
      :class="{ active: activeTab === tab.id }"
      @click="$emit('tab-change', tab.id)"
    >
      <span class="tab-number">{{ tab.number }}</span>
      <span class="tab-title">{{ tab.title }}</span>
      <span class="tab-subtitle">{{ tab.subtitle }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tabs: {
      type: Array,
      required: true
    },
    activeTab: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
/* 导航栏样式保持不变 */
.nav-sidebar {
  width: 250px;
  flex-shrink: 0;
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  margin-bottom: 8px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: #f8f8f8;
}

.nav-item.active {
  background: #e74c3c;
  color: white;
}

.tab-number {
  font-size: 16px;
  font-weight: bold;
  margin-right: 15px;
  opacity: 0.7;
}

.tab-title {
  font-size: 16px;
  font-weight: 500;
  flex-grow: 1;
}

.tab-subtitle {
  font-size: 12px;
  opacity: 0.6;
  text-transform: uppercase;
}
</style>