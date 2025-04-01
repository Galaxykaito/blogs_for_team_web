import axios from 'axios'
import DOMPurify from 'dompurify'

const api = axios.create({
  baseURL: import.meta.env.VUE_APP_API_URL || 'http://localhost:8000',
  timeout: 10000
})

export default {
  async getMemberContent(memberId) {
    try {
      const response = await api.get(`/api/member/${memberId}/content/`)
      return {
        articles: response.data.articles.map(article => ({
          ...article,
          excerpt_html: DOMPurify.sanitize(article.excerpt_html || '')
        })),
        stories: response.data.stories.map(story => ({
          ...story,
          excerpt_html: DOMPurify.sanitize(story.excerpt_html || '')
        }))
      }
    } catch (error) {
      console.error('获取成员内容失败:', error)
      throw error
    }
  },

  async getArticle(identifier) {
    try {
      const response = await api.get(`/api/article/${identifier}/`)
      return {
        ...response.data,
        content_html: DOMPurify.sanitize(response.data.content_html || '')
      }
    } catch (error) {
      console.error('获取文章详情失败:', error)
      throw error
    }
  }
}