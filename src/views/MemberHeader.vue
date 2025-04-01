<template>
  <div class="member-header">
    <img :src="member.avatar" class="header-avatar">
    <div class="header-info">
      <h1>{{ member.name }}</h1>
      <p class="member-bio">{{ member.bio }}</p>
    </div>
    <div class="particles-container"></div>
  </div>
</template>

<script>
export default {
  props: {
    member: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
/* 头部样式保持不变 */
.member-header {
  display: flex;
  align-items: center;
  padding: 30px;
  background: whitesmoke;
  position: relative;
  overflow: hidden;
  border-radius: 10px;
  margin-bottom: 30px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.particles-container {
  position: absolute;
  right: 0;
  top: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.particles-container::before {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  background:
    radial-gradient(circle at 20% 50%,
      rgba(255, 200, 200, 0.8),
      transparent 70%),
    radial-gradient(circle at 70% 30%,
    rgba(239, 48, 134, 0.37),
      transparent 70%),
    radial-gradient(circle at 50% 80%,
      rgba(255, 150, 150, 0.9),
      transparent 70%);
  background-size: 200% 200%;
  animation: particleFlow 8s infinite alternate ease-in-out;
  opacity: 0.3;
  filter:
    blur(15px)
    contrast(120%)
    brightness(120%);
  mix-blend-mode: screen;
}

@keyframes particleFlow {
  0% {
    background-position: 0% 0%;
    opacity: 0.3;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    background-position: 100% 100%;
    opacity: 0.3;
  }
}

.header-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 25px;
  border: 3px solid #e74c3c;
  position: relative;
  z-index: 1;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
}

.header-info h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
  font-weight: 600;
  position: relative;
  z-index: 1;
}

.member-bio {
  margin: 5px 0 0;
  color: #666;
  font-size: 14px;
}
</style>