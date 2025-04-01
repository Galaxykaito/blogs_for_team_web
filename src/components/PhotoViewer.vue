<template>
  <div class="photo-viewer" @click.self="$emit('close')">
    <button class="close-btn" @click="$emit('close')">×</button>
    <img
      :src="photos[currentIndex]"
      class="viewer-image"
      :key="currentIndex"
      @click.stop
    >
    <button class="nav-btn prev" @click.stop="$emit('prev')">❮</button>
    <button class="nav-btn next" @click.stop="$emit('next')">❯</button>
    <div class="photo-counter">
      {{ currentIndex + 1 }} / {{ photos.length }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'PhotoViewer',
  props: {
    photos: {
      type: Array,
      required: true,
      default: () => []
    },
    currentIndex: {
      type: Number,
      required: true,
      default: 0
    }
  },
  mounted() {
    // 禁止背景滚动
    document.body.style.overflow = 'hidden';
    // 添加键盘事件监听
    window.addEventListener('keydown', this.handleKeydown);
  },
  beforeDestroy() {
    // 恢复背景滚动
    document.body.style.overflow = '';
    // 移除键盘事件监听
    window.removeEventListener('keydown', this.handleKeydown);
  },
  methods: {
    handleKeydown(e) {
      switch(e.key) {
        case 'ArrowLeft':
          this.$emit('prev');
          break;
        case 'ArrowRight':
          this.$emit('next');
          break;
        case 'Escape':
          this.$emit('close');
          break;
      }
    }
  }
}
</script>

<style scoped>
.photo-viewer {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  z-index: 10;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(231, 76, 60, 0.8);
  transform: scale(1.1);
}

.viewer-image {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  cursor: zoom-in;
  transition: transform 0.3s;
}

.viewer-image:hover {
  transform: scale(1.02);
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  z-index: 10;
}

.nav-btn:hover {
  background: rgba(231, 76, 60, 0.8);
  transform: translateY(-50%) scale(1.1);
}

.prev {
  left: 20px;
}

.next {
  right: 20px;
}

.photo-counter {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-btn {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }

  .close-btn {
    width: 35px;
    height: 35px;
    font-size: 18px;
  }

  .photo-counter {
    font-size: 13px;
    padding: 4px 12px;
  }
}
</style>