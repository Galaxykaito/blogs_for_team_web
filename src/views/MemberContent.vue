<template>
  <div class="content-area">
    <!-- 文章栏目 -->
    <div v-show="activeTab === 'articles'" class="tab-content">
      <h2>代码作品与文章</h2>
      <div class="pagination-controls">
        <button @click="prevArticlePage" :disabled="currentArticlePage === 1">上一页</button>
        <span>第 {{ currentArticlePage }} 页 / 共 {{ totalArticlePages }} 页</span>
        <button @click="nextArticlePage" :disabled="currentArticlePage === totalArticlePages">下一页</button>
      </div>
      <div v-if="loading.articles" class="loading-spinner"></div>
      <div v-else class="article-list">
        <div v-for="article in paginatedArticles" :key="article.id" class="article-card">
          <h3>{{ article.title }}</h3>
          <p class="meta">发布于 {{ article.date }} · {{ article.views }}次浏览</p>
          <div class="markdown-preview" v-html="article.content_html"></div>
          <button class="read-more" @click="$emit('open-article', article)">阅读全文</button>
        </div>
      </div>
    </div>

    <!-- 故事栏目 -->
    <div v-show="activeTab === 'stories'" class="tab-content">
      <h2>原创故事集</h2>
      <div class="pagination-controls">
        <button @click="prevStoryPage" :disabled="currentStoryPage === 1">上一页</button>
        <span>第 {{ currentStoryPage }} 页 / 共 {{ totalStoryPages }} 页</span>
        <button @click="nextStoryPage" :disabled="currentStoryPage === totalStoryPages">下一页</button>
      </div>
      <div v-if="loading.stories" class="loading-spinner"></div>
      <div v-else class="story-list">
        <div v-for="story in paginatedStories" :key="story.id" class="story-card">
          <h3>{{ story.title }}</h3>
          <div class="markdown-preview" v-html="story.content_html"></div>
          <div class="story-meta">
            <span>{{ story.wordCount }}字</span>
            <span>{{ story.date }}</span>
          </div>
          <button class="read-more" @click="$emit('open-story', story)">阅读全文</button>
        </div>
      </div>
    </div>

    <!-- 照片栏目 -->
    <div v-show="activeTab === 'photos'" class="tab-content">
      <h2>照片集</h2>
      <div class="pagination-controls">
        <button @click="prevPhotoPage" :disabled="currentPhotoPage === 1">上一页</button>
        <span>第 {{ currentPhotoPage }} 页 / 共 {{ totalPhotoPages }} 页</span>
        <button @click="nextPhotoPage" :disabled="currentPhotoPage === totalPhotoPages">下一页</button>
      </div>
      <div class="photo-grid">
        <div v-for="(photo, index) in paginatedPhotos" :key="index" class="photo-item">
          <img :src="photo" alt="照片" @click="$emit('open-photo', index)">
        </div>
      </div>
    </div>

    <!-- 歌单栏目 -->
    <div v-show="activeTab === 'playlist'" class="tab-content">
      <h2>我的歌单</h2>
      <audio v-if="currentSong" ref="audioPlayer" :src="currentSong.src"></audio>

      <div class="music-list">
        <div v-for="song in playlist" :key="song.id" class="music-item">
          <img :src="song.cover" class="album-cover">
          <div class="song-info">
            <h3>{{ song.title }}</h3>
            <p>{{ song.artist }} · {{ song.duration }}</p>
          </div>
          <button class="play-btn" @click="playSong(song)">
            {{ currentSong && currentSong.id === song.id && isPlaying ? '暂停' : '播放' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 视频栏目 -->
    <div v-show="activeTab === 'videos'" class="tab-content">
      <h2>视频</h2>
      <div class="pagination-controls">
        <button @click="prevVideoPage" :disabled="currentVideoPage === 1">上一页</button>
        <span>第 {{ currentVideoPage }} 页 / 共 {{ totalVideoPages }} 页</span>
        <button @click="nextVideoPage" :disabled="currentVideoPage === totalVideoPages">下一页</button>
      </div>
      <div class="video-list">
        <div v-for="video in paginatedVideos" :key="video.id" class="video-item">
          <video
            ref="videoPlayer"
            :poster="video.thumbnail"
            class="video-thumbnail"
          >
            <source :src="video.src" type="video/mp4">
            您的浏览器不支持 HTML5 视频。
          </video>
          <div class="video-info">
            <h3>{{ video.title }}</h3>
            <p>{{ video.description }}</p>
            <button class="play-btn" @click="playVideo(video)">
              {{ currentVideo && currentVideo.id === video.id && isVideoPlaying ? '暂停' : '播放' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 游戏栏目 -->
    <div v-show="activeTab === 'games'" class="tab-content">
      <h2>我的游戏</h2>
      <div class="game-list">
        <div v-for="game in games" :key="game.id" class="game-item">
          <h3>{{ game.title }}</h3>
          <p>游戏内ID: {{ game.id }}</p>
          <p>描述: {{ game.description }}</p>
        </div>
      </div>
    </div>

    <!-- 模态框 -->
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
</template>

<script>
import ArticleModal from '@/components/ArticlesModal.vue'
import StoryModal from '@/components/StoriesModal.vue'
import PhotoViewer from '@/components/PhotoViewer.vue'

export default {
  components: {
    ArticleModal,
    StoryModal,
    PhotoViewer
  },
  props: {
    activeTab: String,
    member: Object,
    articles: Array,
    stories: Array,
    photos: Array,
    playlist: Array,
    videos: Array,
    games: Array,
    loading: Object
  },
  data() {
    return {
      currentArticlePage: 1,
      articlesPerPage: 3,
      currentStoryPage: 1,
      storiesPerPage: 3,
      currentPhotoPage: 1,
      photosPerPage: 6,
      currentVideoPage: 1,
      videosPerPage: 1,
      activeArticle: null,
      activeStory: null,
      photoViewerVisible: false,
      currentPhotoIndex: 0,
      currentSong: null,
      isPlaying: false,
      currentVideo: null,
      isVideoPlaying: false
    }
  },
  computed: {
    // 文章分页
    totalArticlePages() {
      return Math.ceil(this.articles.length / this.articlesPerPage)
    },
    paginatedArticles() {
      const start = (this.currentArticlePage - 1) * this.articlesPerPage
      return this.articles.slice(start, start + this.articlesPerPage)
    },
    // 故事分页
    totalStoryPages() {
      return Math.ceil(this.stories.length / this.storiesPerPage)
    },
    paginatedStories() {
      const start = (this.currentStoryPage - 1) * this.storiesPerPage
      return this.stories.slice(start, start + this.storiesPerPage)
    },
    // 照片分页
    totalPhotoPages() {
      return Math.ceil(this.photos.length / this.photosPerPage)
    },
    paginatedPhotos() {
      const start = (this.currentPhotoPage - 1) * this.photosPerPage
      return this.photos.slice(start, start + this.photosPerPage)
    },
    // 视频分页
    totalVideoPages() {
      return Math.ceil(this.videos.length / this.videosPerPage)
    },
    paginatedVideos() {
      const start = (this.currentVideoPage - 1) * this.videosPerPage
      return this.videos.slice(start, start + this.videosPerPage)
    }
  },
  methods: {
    // 文章分页方法
    prevArticlePage() {
      if (this.currentArticlePage > 1) this.currentArticlePage--
    },
    nextArticlePage() {
      if (this.currentArticlePage < this.totalArticlePages) this.currentArticlePage++
    },
    // 故事分页方法
    prevStoryPage() {
      if (this.currentStoryPage > 1) this.currentStoryPage--
    },
    nextStoryPage() {
      if (this.currentStoryPage < this.totalStoryPages) this.currentStoryPage++
    },
    // 照片分页方法
    prevPhotoPage() {
      if (this.currentPhotoPage > 1) this.currentPhotoPage--
    },
    nextPhotoPage() {
      if (this.currentPhotoPage < this.totalPhotoPages) this.currentPhotoPage++
    },
    // 视频分页方法
    prevVideoPage() {
      if (this.currentVideoPage > 1) this.currentVideoPage--
    },
    nextVideoPage() {
      if (this.currentVideoPage < this.totalVideoPages) this.currentVideoPage++
    },
    // 照片查看器方法
    prevPhoto() {
      this.currentPhotoIndex = (this.currentPhotoIndex - 1 + this.photos.length) % this.photos.length
    },
    nextPhoto() {
      this.currentPhotoIndex = (this.currentPhotoIndex + 1) % this.photos.length
    },
    // 音乐播放方法
    playSong(song) {
      if (this.currentSong && this.currentSong.id === song.id) {
        // 同一首歌，切换播放/暂停
        if (this.isPlaying) {
          this.$refs.audioPlayer.pause()
        } else {
          this.$refs.audioPlayer.play()
        }
        this.isPlaying = !this.isPlaying
      } else {
        // 新歌曲，开始播放
        this.currentSong = song
        this.isPlaying = true
        this.$refs.audioPlayer.loop = true;
        this.$nextTick(() => {
          this.$refs.audioPlayer.play()
        })
      }
    },
    // 视频播放方法
    playVideo(video) {
      const globalIndex = this.videos.findIndex(v => v.id === video.id);
      const currentPageIndex = globalIndex % this.videosPerPage;
      const videoElement = this.$refs.videoPlayer && this.$refs.videoPlayer[currentPageIndex];

      if (!videoElement) return;

      if (this.currentVideo && this.currentVideo.id === video.id) {
        // 同一个视频，切换播放/暂停
        if (this.isVideoPlaying) {
          videoElement.pause();
        } else {
          videoElement.play();
        }
        this.isVideoPlaying = !this.isVideoPlaying;
      } else {
        // 新视频，开始播放
        if (this.currentVideo) {
          // 暂停之前播放的视频
          const prevGlobalIndex = this.videos.findIndex(v => v.id === this.currentVideo.id);
          const prevPageIndex = prevGlobalIndex % this.videosPerPage;
          if (this.$refs.videoPlayer[prevPageIndex]) {
            this.$refs.videoPlayer[prevPageIndex].pause();
          }
        }

        this.currentVideo = video;
        this.isVideoPlaying = true;
        this.$nextTick(() => {
          videoElement.play();
        });
      }
    }
  }
}
</script>

<style scoped>
.content-area {
  flex: 1;
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 8px 12px rgba(0,0,0,0.1);
}

/* 所有标签内容共用样式 */
.tab-content h2 {
  margin-bottom: 20px;
  font-size: 22px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

/* 分页控制 */
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin: 20px 0;
}

.pagination-controls button {
  padding: 6px 12px;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-controls button:hover:not(:disabled) {
  background: #e0e0e0;
}

.pagination-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 加载动画 */
.loading-spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #e74c3c;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 40px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 文章卡片 */
.article-card, .story-card {
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.article-card h3, .story-card h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: #222;
}

.meta, .story-meta {
  font-size: 13px;
  color: #888;
  margin-bottom: 12px;
}

.story-meta {
  display: flex;
  justify-content: space-between;
}

.markdown-preview {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
  color: #555;
  margin: 15px 0;
  font-size: 15px;
}

.read-more {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.read-more:hover {
  background: #c0392b;
}

/* 照片网格 */
.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.photo-item {
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.photo-item:hover {
  transform: scale(1.03);
}

.photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 音乐列表 */
.music-list {
  margin-top: 20px;
}

.music-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 6px;
  transition: background 0.3s ease;
}

.music-item:hover {
  background: #f8f8f8;
}

.album-cover {
  width: 50px;
  height: 50px;
  border-radius: 4px;
  margin-right: 15px;
}

.song-info {
  flex: 1;
}

.song-info h3 {
  font-size: 16px;
  margin-bottom: 3px;
}

.song-info p {
  font-size: 13px;
  color: #888;
}

.play-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
}

/* 视频列表 */
.video-list {
  margin-top: 20px;
}

.video-item {
  margin-bottom: 20px;
}

.video-thumbnail {
  width: 100%;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 8px;
  aspect-ratio: 16/9;
  object-fit: cover;
}

.video-info h3 {
  font-size: 16px;
  margin-bottom: 5px;
}

.video-info p {
  font-size: 14px;
  color: #666;
}

/* 游戏列表 */
.game-list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.game-item {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 12px;
  background: #f9f9f9;
  width: 70%;
  text-align: left;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-area {
    padding: 20px;
  }

  .photo-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .game-item {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .content-area {
    padding: 15px;
  }

  .tab-content h2 {
    font-size: 20px;
  }
}
</style>