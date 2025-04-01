<template>
  <div class="member-container">
    <button class="back-btn" @click="$router.go(-1)">← 返回主页</button>

    <MemberHeader :member="member" />

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
  </div>
</template>

<script>
import MemberHeader from './MemberHeader.vue'
import MemberNav from './MemberNav.vue'
import MemberContent from './MemberContent.vue'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-python'
import { marked } from 'marked'


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

marked.setOptions({
  highlight: (code, lang) => {
    if (Prism.languages[lang]) {
      return Prism.highlight(code, Prism.languages[lang], lang)
    }
    return code
  }
});

export default {
  name: 'MemberView',
  components: {
    MemberHeader,
    MemberNav,
    MemberContent
  },
  props: ['id'],
  data() {
    return {
      activeTab: 'articles',
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
      }
    }
  },
  async created() {
    await this.loadMemberData();
    await this.loadContent();
  },
  mounted() {
    this.$nextTick(() => {
      Prism.highlightAll();
    });
  },
  updated() {
    this.$nextTick(() => {
      Prism.highlightAll();
    });
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
      // 其他成员的数据加载...
    },
    async loadContent() {
      await Promise.all([
        this.loadArticles(),
        this.loadStories()
      ]);
    },
    async loadArticles() {
      try {
        await new Promise(resolve => setTimeout(resolve, 800));

        if (this.id === '1') {
          const article1Content = await import('@/markdown/articles/qqbot.md?raw');
          const article1Content2 = await import('@/markdown/articles/gsv.md?raw');
          this.articles = [
            {
              id: 'article1',
              title: 'QQbot-cos安全总监德穆兰',
              date: '2025-03-18',
              views: 256,
              excerpt: marked('本文介绍了nonebot2和napcat结合的QQbot用来cos安全总监德穆兰...'),
              content: marked(article1Content.default)
            },
            {
              id: 'article2',
              title: 'GPT-SOVITS云端训练',
              date: '2023-03-22',
              views: 189,
              excerpt: marked('GPT-SOVITS云端训练语音合成模型的方法...'),
              content: marked(article1Content2.default)
            }
          ];
        }
        // 其他成员的文章加载...
      } finally {
        this.loading.articles = false;
      }
    },
    async loadStories() {
      try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        if (this.id === '1') {
          const story1Content = await import('@/markdown/stories/原批.md?raw');
          this.stories = [
            {
              id: 'story1',
              title: '原批',
              date: '2023-06-10',
              wordCount: 3200,
              excerpt: marked('那是一个雨夜，我启动了原神，成为了原批...'),
              content: marked(story1Content.default)
            }
          ];
        }
        // 其他成员的故事加载...
      } finally {
        this.loading.stories = false;
      }
    },
    openArticle(article) {
      this.activeArticle = article;
    },
    openStory(story) {
      this.activeStory = story;
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
  flex-direction: row;
  align-items: flex-start;
  gap: 30px;
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