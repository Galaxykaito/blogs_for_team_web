<template>
  <div class="article-modal" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">×</button>
      <h2>{{ article.title }}</h2>
      <p class="meta">发布于 {{ article.date }}</p>
      <div class="markdown-content" v-html="article.content"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ArticleModal',
  props: {
    article: {
      type: Object,
      required: true,
      validator: (value) => {
        return 'title' in value && 'content_html' in value
      }
    }
  },
  mounted() {
    // 改为添加class而不是直接修改style
    document.body.classList.add('modal-open');
  },
  // 在模态框组件中
updated() {
  this.$nextTick(() => {
    Prism.highlightAll()
  })
},
  beforeUnmount() { // 使用 beforeUnmount 替代 beforeDestroy
    document.body.classList.remove('modal-open');
  }
}
</script>

<style scoped>
.article-modal {
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
}

.markdown-content {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.8;
  color: #333;
}

.markdown-content >>> h1 {
  font-size: 2em;
  margin: 1em 0;
  color: #222;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
}

.markdown-content >>> h2 {
  font-size: 1.5em;
  margin: 1em 0;
  color: #222;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
}

.markdown-content >>> h3 {
  font-size: 1.25em;
  margin: 1em 0;
  color: #222;
}

.markdown-content >>> p {
  margin: 1em 0;
  font-size: 16px;
}

.markdown-content >>> a {
  color: #e74c3c;
  text-decoration: none;
}

.markdown-content >>> a:hover {
  text-decoration: underline;
}

.markdown-content >>> pre {
  background: #f8f8f8;
  border-radius: 6px;
  padding: 16px;
  overflow: auto;
  margin: 1em 0;
  position: relative;
}

.markdown-content >>> pre::before {
  content: attr(data-language);
  position: absolute;
  top: 0;
  right: 0;
  background: #e74c3c;
  color: white;
  padding: 2px 8px;
  font-size: 12px;
  border-radius: 0 0 0 4px;
}

.markdown-content >>> code {
  font-family: 'Fira Code', monospace;
  font-size: 14px;
  background: rgba(175, 184, 193, 0.2);
  padding: 0.2em 0.4em;
  border-radius: 3px;
}

.markdown-content >>> pre code {
  background: transparent;
  padding: 0;
}

.markdown-content >>> blockquote {
  border-left: 4px solid #e74c3c;
  padding-left: 16px;
  margin: 1em 0;
  color: #666;
}

.markdown-content >>> img {
  max-width: 100%;
  border-radius: 4px;
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

  .markdown-content >>> p {
    font-size: 15px;
  }
}
</style>