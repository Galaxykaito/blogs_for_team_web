<template>
  <div class="home-container" @mousemove="trackMousePosition">
    <!-- 声音控制按钮 -->
    <button
      v-if="showUnmuteButton"
      @click="unmuteVideo"
      class="unmute-btn"
    >
      🔊 点击开启声音
    </button>

    <!-- 全屏视频背景 -->
    <video
      ref="videoPlayer"
      autoplay
      loop
      :muted="isMuted"
      class="background-video"
    >
      <source :src="videoSrc" type="video/mp4">
    </video>

    <!-- 内容层 -->
    <div class="content-layer">
      <h1 class="welcome-title">
        欢迎来到253
      </h1>

      <!-- 成员卡片网格 -->
      <div class="members-grid">
        <div
          v-for="member in members"
          :key="member.id"
          class="member-card"
          @click="goToMember(member.id)"
          :style="cardStyle(member.id)"
          :data-id="member.id"
        >
          <div class="card-glow"></div>
          <div class="card-highlight"></div>
          <img
            :src="member.avatar"
            class="member-avatar"
            :alt="member.name"
          >
          <div class="member-name">{{ member.name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router' // 添加这行

// 静态资源导入
import videoSrc from '@/assets/brokensun.mp4'
import member1 from '@/assets/tlsy.png'
import member2 from '@/assets/abln.png'
import member3 from '@/assets/gzh.png'
import member4 from '@/assets/sy.png'

export default {
  setup() {
    const router = useRouter() // 在setup中获取router
    const videoPlayer = ref(null)
    const showUnmuteButton = ref(true)
    const isMuted = ref(true)
    const mouseX = ref(0)
    const mouseY = ref(0)

    const members = ref([
      { id: 1, name: '黄德祥/Tachyon', avatar: member1 },
      { id: 2, name: '许一成/飞鼠', avatar: member2 },
      { id: 3, name: '李坤昀/艾琳吹', avatar: member3 },
      { id: 4, name: '张政辉/霸白', avatar: member4 }
    ])

    const trackMousePosition = (e) => {
      mouseX.value = e.clientX
      mouseY.value = e.clientY
    }

    const cardStyle = (id) => {
      const card = document.querySelector(`.member-card[data-id="${id}"]`)
      if (!card) return {}

      const rect = card.getBoundingClientRect()
      const x = mouseX.value - rect.left
      const y = mouseY.value - rect.top

      return {
        '--mouse-x': `${x}px`,
        '--mouse-y': `${y}px`
      }
    }

    const goToMember = (id) => {
      router.push(`/member/${id}`) // 使用获取到的router
    }

    const unmuteVideo = () => {
      videoPlayer.value.muted = false
      isMuted.value = false
      showUnmuteButton.value = false
    }

    return {
      videoSrc,
      members,
      videoPlayer,
      showUnmuteButton,
      isMuted,
      mouseX,
      mouseY,
      trackMousePosition,
      cardStyle,
      goToMember,
      unmuteVideo
    }
  },
  mounted() {
    this.videoPlayer.play().catch(e => {
      console.log("自动播放需要用户交互:", e)
      this.showUnmuteButton = true
    })

    // 初始化卡片鼠标位置追踪
    setInterval(() => {
      this.members.forEach(member => {
        this.cardStyle(member.id)
      })
    }, 100)
  }
}
</script>

<style scoped>
.home-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
  opacity: 0.9;
}

.content-layer {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
}

.unmute-btn {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
  padding: 10px 20px;
  background: rgba(255,255,255,0.9);
  color: #e74c3c;
  border: 1px solid #e74c3c;
  border-radius: 25px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  font-weight: bold;
}

.unmute-btn:hover {
  background: #e74c3c;
  color: white;
  transform: scale(1.05);
}

.welcome-title {
  color: white;
  font-size: 3.5rem;
  text-align: center;
  margin-bottom: 60px;
  text-shadow: 0 4px 8px rgba(231, 76, 60, 0.5);
  font-weight: 500;
  letter-spacing: 2px;
  position: relative;
}

.welcome-title::after {
  content: '';
  display: block;
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #ffffff, transparent);
  margin: 20px auto 0;
  opacity: 0.9;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.member-card {
  position: relative;
  background: rgba(18, 18, 18, 0.85); /* 保持高级黑 */
  border-radius: 16px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  z-index: 1;
  backdrop-filter: blur(8px);
}

.member-card:hover {
  transform: translateY(-10px) scale(1.03);
  box-shadow: 0 12px 40px rgba(231, 76, 60, 0.3);
  border-color: rgba(231, 76, 60, 0.5);
}

/* 红白色系流光效果 */
.card-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    rgba(231, 76, 60, 0.4),
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: 0.7s;
  z-index: -1;
}

.member-card:hover .card-glow {
  left: 100%;
}

/* 红白色系鼠标跟随高光 */
.card-highlight {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    400px circle at var(--mouse-x) var(--mouse-y),
    rgba(255, 255, 255, 0.15),
    transparent 50%
  );
  border-radius: inherit;
  opacity: 0;
  transition: opacity 0.4s;
  z-index: -1;
}

.member-card:hover .card-highlight {
  opacity: 1;
}

/* 头像样式 - 红白边框 */
.member-avatar {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(255, 255, 255, 0.5);
  margin-bottom: 20px;
  transition: all 0.5s ease;
  filter: brightness(0.95);
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
}

.member-card:hover .member-avatar {
  transform: scale(1.08);
  filter: brightness(1.1);
  border-color: #e74c3c;
  box-shadow: 0 8px 25px rgba(231, 76, 60, 0.4);
}

/* 成员名字样式 - 红白色系 */
.member-name {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.3rem;
  font-weight: 500;
  margin: 0;
  transition: all 0.3s ease;
  position: relative;
  display: inline-block;
}

.member-name::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 0;
  height: 2px;
  background: #e74c3c;
  transition: width 0.3s ease;
}

.member-card:hover .member-name {
  color: white;
  text-shadow: 0 0 10px rgba(231, 76, 60, 0.5);
}

.member-card:hover .member-name::after {
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .members-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
  }

  .welcome-title {
    font-size: 2.8rem;
    margin-bottom: 50px;
  }

  .member-avatar {
    width: 120px;
    height: 120px;
  }
}

@media (max-width: 640px) {
  .members-grid {
    grid-template-columns: 1fr;
    max-width: 400px;
  }

  .welcome-title {
    font-size: 2.2rem;
    margin-bottom: 40px;
  }

  .content-layer {
    padding: 40px 20px;
  }

  .member-avatar {
    width: 100px;
    height: 100px;
  }

  .member-name {
    font-size: 1.1rem;
  }
}

/* 卡片入场动画 - 红白色系 */
@keyframes cardEntrance {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.member-card {
  animation: cardEntrance 0.6s ease-out both;
}

.member-card:nth-child(1) { animation-delay: 0.1s; }
.member-card:nth-child(2) { animation-delay: 0.2s; }
.member-card:nth-child(3) { animation-delay: 0.3s; }
.member-card:nth-child(4) { animation-delay: 0.4s; }
</style>