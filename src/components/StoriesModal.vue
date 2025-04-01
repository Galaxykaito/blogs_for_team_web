<template>
  <div class="story-modal" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">×</button>
      <h2>{{ story.title }}</h2>
      <p class="meta">{{ story.wordCount }}字 · {{ story.date }}</p>
      <div class="markdown-content" v-html="story.content"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StoryModal',
  props: {
    story: {
      type: Object,
      required: true,
      default: () => ({
        title: '',
        date: '',
        wordCount: 0,
        content: ''
      })
    }
  },
  mounted() {
    // 禁止背景滚动
    document.body.style.overflow = 'hidden';
  },
  // 在模态框组件中
updated() {
  this.$nextTick(() => {
    Prism.highlightAll()
  })
},
  beforeDestroy() {
    // 恢复背景滚动
    document.body.style.overflow = '';
  }
}
</script>

<style scoped>
.story-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.modal-content {
  position: relative;
  background: white;
  border-radius: 8px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 30px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #e74c3c;
}

h2 {
  color: #333;
  margin-bottom: 10px;
  font-size: 24px;
}

.meta {
  color: #888;
  font-size: 14px;
  margin-bottom: 20px;
  display: flex;
  gap: 15px;
}

.markdown-content {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.8;
  color: #333;
  font-size: 16px;
}

.markdown-content >>> h1 {
  font-size: 1.8em;
  margin: 1em 0;
  color: #222;
}

.markdown-content >>> h2 {
  font-size: 1.5em;
  margin: 1em 0;
  color: #222;
}

.markdown-content >>> h3 {
  font-size: 1.25em;
  margin: 1em 0;
  color: #222;
}

.markdown-content >>> p {
  margin: 1em 0;
  text-align: justify;
}

.markdown-content >>> a {
  color: #e74c3c;
  text-decoration: none;
}

.markdown-content >>> a:hover {
  text-decoration: underline;
}

.markdown-content >>> blockquote {
  border-left: 3px solid #e74c3c;
  padding-left: 15px;
  margin: 1em 0;
  color: #666;
  font-style: italic;
}

.markdown-content >>> hr {
  border: none;
  border-top: 1px solid #eee;
  margin: 2em 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .modal-content {
    padding: 20px;
    max-height: 85vh;
  }

  h2 {
    font-size: 20px;
  }

  .markdown-content {
    font-size: 15px;
    line-height: 1.7;
  }
}
</style>