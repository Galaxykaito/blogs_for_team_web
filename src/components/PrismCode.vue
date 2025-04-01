<template>
  <pre class="line-numbers"><code :class="`language-${language}`"><slot /></code></pre>
</template>

<script>
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'

export default {
  props: {
    language: {
      type: String,
      default: 'javascript'
    }
  },
  mounted() {
    Prism.highlightAllUnder(this.$el)
  },
  updated() {
    Prism.highlightAllUnder(this.$el)
  }
}
</script>

<style scoped>
pre[class*="language-"] {
  border-radius: 8px;
  margin: 1em 0;
}
</style>