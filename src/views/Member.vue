<template>
  <div class="member-container">
    <button class="back-btn" @click="$router.go(-1)">← 返回主页</button>

    <MemberHeader :member="member" />
    <div class="member-main-wrapper"> <!-- 新增滚动容器 -->

    <div class="member-main">
      <MemberNav
        :tabs="tabs"
        :active-tab="activeTab"
        @tab-change="activeTab = $event"
      />

      <MemberContent
        :active-tab="activeTab"
        :member="member"
        :articles="articles"
        :stories="stories"
        :photos="photos"
        :playlist="playlist"
        :videos="videos"
        :games="games"
        :loading="loading"
        @open-article="openArticle"
        @open-story="openStory"
        @open-photo="openPhotoViewer"
      />
    </div>

    <!-- 新增的模态框组件 -->
    <ArticleModal
      v-if="activeArticle"
      :article="activeArticle"
      @close="activeArticle = null"
    />

    <StoryModal
      v-if="activeStory"
      :story="activeStory"
      @close="activeStory = null"
    />

    <PhotoViewer
      v-if="photoViewerVisible"
      :photos="photos"
      :current-index="currentPhotoIndex"
      @close="photoViewerVisible = false"
      @prev="prevPhoto"
      @next="nextPhoto"
    />
  </div>
</div>
</template>

<script>
import contentApi from '@/api/content'
import MemberHeader from './MemberHeader.vue'
import MemberNav from './MemberNav.vue'
import MemberContent from './MemberContent.vue'
import ArticleModal from '@/components/ArticlesModal.vue'
import StoryModal from '@/components/StoriesModal.vue'
import PhotoViewer from '@/components/PhotoViewer.vue'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-python'

// 导入资源文件
import member1 from '@/assets/tlsy.png'
import member2 from '@/assets/abln.png'
import member3 from '@/assets/gzh.png'
import member4 from '@/assets/sy.png'
import photo1 from '@/assets/tlsy.png'
import album2 from '@/assets/member1.jpg'
import album1 from '@/assets/巴别塔.png'
import videoThumb1 from '@/assets/member1.jpg'
import videoThumb2 from '@/assets/member2.png'
import song1 from '@/assets/theopening.mp3'
import song2 from '@/assets/Founding Stone.flac'
import song3 from '@/assets/相见欢.flac'
import vedio1 from '@/assets/brokensun.mp4'
import vidio1 from '@/assets/语音合成效果展示.mp4'

export default {
  name: 'MemberView',
  components: {
    MemberHeader,
    MemberNav,
    MemberContent,
    ArticleModal,
    StoryModal,
    PhotoViewer
  },
  props: ['id'],
  data() {
    return {
      activeTab: 'articles',
      activeArticle: null,
      activeStory: null,
      photoViewerVisible: false,
      currentPhotoIndex: 0,
      tabs: [
        { id: 'articles', number: '01', title: '文章', subtitle: 'Articles' },
        { id: 'stories', number: '02', title: '故事', subtitle: 'Stories' },
        { id: 'photos', number: '03', title: '照片', subtitle: 'Photos' },
        { id: 'playlist', number: '04', title: '歌单', subtitle: 'Playlist' },
        { id: 'videos', number: '05', title: '视频', subtitle: 'Videos' },
        { id: 'games', number: '06', title: '玩的游戏', subtitle: 'Games' }
      ],
      member: {
        id: 1,
        name: '黄德祥/Tachyon',
        avatar: member1,
        bio: '开发者 | 音乐爱好者 | 故事写手'
      },
      articles: [],
      stories: [],
      photos: [],
      playlist: [],
      videos: [],
      games: [],
      loading: {
        articles: true,
        stories: true
      },
      currentArticlePage: 1,
      articlesPerPage: 3,
      currentStoryPage: 1,
      storiesPerPage: 3,
      currentPhotoPage: 1,
      photosPerPage: 6,
      currentVideoPage: 1,
      videosPerPage: 2
    }
  },
  computed: {
    totalArticlePages() {
      return Math.ceil(this.articles.length / this.articlesPerPage)
    },
    paginatedArticles() {
      const start = (this.currentArticlePage - 1) * this.articlesPerPage
      return this.articles.slice(start, start + this.articlesPerPage)
    },
    totalStoryPages() {
      return Math.ceil(this.stories.length / this.storiesPerPage)
    },
    paginatedStories() {
      const start = (this.currentStoryPage - 1) * this.storiesPerPage
      return this.stories.slice(start, start + this.storiesPerPage)
    },
    totalPhotoPages() {
      return Math.ceil(this.photos.length / this.photosPerPage)
    },
    paginatedPhotos() {
      const start = (this.currentPhotoPage - 1) * this.photosPerPage
      return this.photos.slice(start, start + this.photosPerPage)
    },
    totalVideoPages() {
      return Math.ceil(this.videos.length / this.videosPerPage)
    },
    paginatedVideos() {
      const start = (this.currentVideoPage - 1) * this.videosPerPage
      return this.videos.slice(start, start + this.videosPerPage)
    }
  },
  async created() {
    await this.loadMemberData()
    await this.loadContent()
  },
  mounted() {
    this.$nextTick(() => {
      Prism.highlightAll()
    })
  },
  updated() {
    this.$nextTick(() => {
      Prism.highlightAll()
    })
  },
  methods: {
    async loadMemberData() {
      // 根据ID加载不同成员数据
      if (this.id === '1') {
        this.member = {
          id: 1,
          name: '黄德祥/Tachyon',
          avatar: member1,
          bio: '开发者 | 音乐爱好者 | 故事写手|🔺▢粥批 | 原批铁批'
        };
        this.photos = [photo1, album1, album2, member2, member3, member4];
        this.playlist = [
          {
            id: 1,
            title: 'The Opening',
            artist: '塞壬唱片_MSR',
            duration: '3:45',
            cover: album1,
            src: song1
          },
          {
            id: 2,
            title: 'Founding Stone',
            artist: '塞壬唱片_MSR',
            duration: '4:12',
            cover: album1,
            src: song2
          },
          {
            id: 3,
            title: '相见欢',
            artist: '塞壬唱片_MSR',
            duration: '4:12',
            cover: member3,
            src: song3
          }
        ];
        this.videos = [
          {
            id: 1,
            title: '爆裂黎明',
            description: '多喝六个核桃~',
            thumbnail: videoThumb1,
            src: vedio1
          },
          {
            id: 2,
            title: '语音合成效果展示',
            description: '正宗哈夫克口音~',
            thumbnail: videoThumb2,
            src: vidio1
          }
        ];
        this.games = [
          { id: '417827950 欧#3339', title: '明日方舟', description: '入职日2019-9-15 阿斯卡纶，特蕾西娅厨' },
          { id: '哈夫克阴六兵', title: '三角洲行动', description: '战场烽火双修，我说我厨老太你信吗？' }
        ];
      }
      else if (this.id === '2') {
        this.member = {
          id: 2,
          name: '飞鼠',
          avatar: member2,
          bio: 'chikawa'
        };
        // 设置成员2特有的内容
        this.photos = [member2, member2, member2]; // 使用成员2的照片
        this.playlist = [
          {
            id: 1,
            title: '成员2的歌1',
            artist: '成员2',
            duration: '3:20',
            cover: member2,
            src: '#'
          }
        ];
        this.videos = [
          {
            id: 1,
            title: '成员2的视频',
            description: '成员2的视频描述',
            thumbnail: member2,
            src: '#'
          }
        ];
      }
      else if (this.id === '3') {
    this.member = {
      id: 3,
      name: '成员3名称',
      avatar: member3,
      bio: '成员3的简介'
    };
    // 设置成员3特有的内容
    this.photos = [member3, member3, member3, member3];
    this.playlist = [
      {
        id: 1,
        title: '成员3的歌1',
        artist: '成员3',
        duration: '4:10',
        cover: member3,
        src: '#'
      }
    ];
    this.videos = [
      {
        id: 1,
        title: '成员3的视频',
        description: '成员3的视频描述',
        thumbnail: member3,
        src: '#'
      }
    ];
  } else if (this.id === '4') {
    this.member = {
      id: 4,
      name: '成员4名称',
      avatar: member4,
      bio: '成员4的简介'
    };
    // 设置成员4特有的内容
    this.photos = [member4, member4, member4, member4, member4];
    this.playlist = [
      {
        id: 1,
        title: '成员4的歌1',
        artist: '成员4',
        duration: '3:50',
        cover: member4,
        src: '#'
      }
    ];
    this.videos = [
      {
        id: 1,
        title: '成员4的视频',
        description: '成员4的视频描述',
        thumbnail: member4,
        src: '#'
      }
    ];
  }
      // 其他成员的数据加载...
    },
     async loadContent() {
      this.loading.articles = true;
      try {
        const data = await contentApi.getMemberContent(this.id)
        this.articles = data.articles.map(item => ({
          id: item.identifier,
          title: item.title,
          date: item.date,
          views: item.views,
          excerpt: item.excerpt,
          content: '' // 延迟加载
        }))

        this.stories = data.stories.map(item => ({
          id: item.identifier,
          title: item.title,
          date: item.date,
          wordCount: item.word_count,
          excerpt: item.excerpt,
          content: '' // 延迟加载
        }))

        this.loading.articles = false
        this.loading.stories = false
      } catch (error) {
        console.error('加载内容失败:', error)
        this.loading.articles = false
        this.loading.stories = false
      }
    },
    async loadArticles() {
  try {
    const data = await contentApi.getMemberContent(this.id)
    this.articles = data.articles.map(item => ({
      id: item.identifier,
      title: item.title,
      date: item.date,
      views: item.views,
      excerpt: item.excerpt_html,  // 使用后端返回的已渲染摘要
      content: ''  // 延迟加载完整内容
    }))
  } catch (error) {
    console.error('加载文章失败:', error)
    this.articles = []
  } finally {
    this.loading.articles = false
  }
},

    prevPhoto() {
      this.currentPhotoIndex = (this.currentPhotoIndex - 1 + this.photos.length) % this.photos.length
    },
    nextPhoto() {
      this.currentPhotoIndex = (this.currentPhotoIndex + 1) % this.photos.length
    },
    async openArticle(article) {
      if (!article.content) {
        try {
          const data = await contentApi.getArticle(article.id)
          article.content = data.content_html
          article.date = data.date
          article.views = data.views
        } catch (error) {
          console.error('加载文章内容失败:', error)
          article.content = '<p>加载内容失败，请稍后重试</p>'
        }
      }
      this.activeArticle = { ...article } // 创建新对象避免响应式问题
    },
    async openStory(story) {
      if (!story.content) {
        try {
          const data = await contentApi.getArticle(story.id)
          story.content = data.content_html
        } catch (error) {
          console.error('加载故事内容失败:', error)
          story.content = '<p>加载内容失败，请稍后重试</p>'
        }
      }
      this.activeStory = { ...story } // 创建新对象避免响应式问题
    },
    openPhotoViewer(index) {
      this.currentPhotoIndex = index;
      this.photoViewerVisible = true;
    }
  }
}
</script>

<style scoped>
/* 基础样式保持不变 */
.member-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background-image: url('@/assets/巴别塔.png');
  background-size: 100% 100%;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-blend-mode: overlay;
  background-color: rgba(249, 242, 243, 0.8);
}

.back-btn {
  position: fixed;
  top: 20px;
  left: 20px;
  background: rgba(231, 76, 60, 0.9);
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 20px;
  cursor: pointer;
  z-index: 100;
  transition: all 0.3s ease;
}

.back-btn:hover {
  transform: translateX(5px);
}


.member-main {
  display: flex;
  gap: 30px;
  min-height: 100%;
}


/* 响应式设计 */
@media (max-width: 768px) {
  .member-main {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .back-btn {
    padding: 6px 12px;
    font-size: 14px;
  }
}
</style>