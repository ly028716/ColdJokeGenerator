// 笑话卡片组件
const util = require('../../utils/util.js');
const ApiClient = require('../../utils/api.js');

Component({
  properties: {
    // 笑话数据
    joke: {
      type: Object,
      value: {}
    },
    // 是否显示操作按钮
    showActions: {
      type: Boolean,
      value: true
    },
    // 是否显示分享按钮
    showShare: {
      type: Boolean,
      value: true
    },
    // 是否显示收藏按钮
    showFavorite: {
      type: Boolean,
      value: true
    },
    // 是否显示复制按钮
    showCopy: {
      type: Boolean,
      value: true
    },
    // 卡片样式
    cardStyle: {
      type: String,
      value: ''
    }
  },

  data: {
    isFavorited: false,
    isSharing: false
  },

  lifetimes: {
    attached() {
      this.checkFavoriteStatus();
    }
  },

  observers: {
    'joke.id': function(jokeId) {
      if (jokeId) {
        this.checkFavoriteStatus();
      }
    }
  },

  methods: {
    // 检查收藏状态
    checkFavoriteStatus() {
      const joke = this.data.joke;
      if (!joke.id) return;

      const favoriteJokes = util.storage.get('favoriteJokes', []);
      const isFavorited = favoriteJokes.some(item => item.id === joke.id);
      this.setData({ isFavorited });
    },

    // 点击笑话内容
    onJokeClick() {
      // 震动反馈
      util.vibrateShort('light');
      
      // 触发父组件事件
      this.triggerEvent('jokeclick', {
        joke: this.data.joke
      });
    },

    // 复制笑话
    async onCopy() {
      const joke = this.data.joke;
      if (!joke.content) return;

      try {
        const success = await util.copyToClipboard(joke.content);
        if (success) {
          // 震动反馈
          util.vibrateShort('medium');
          
          // 触发复制事件
          this.triggerEvent('copy', {
            joke: joke
          });
        }
      } catch (error) {
        console.error('复制失败:', error);
        util.showError('复制失败');
      }
    },

    // 收藏/取消收藏
    async onFavorite() {
      const joke = this.data.joke;
      if (!joke.id) return;

      try {
        let favoriteJokes = util.storage.get('favoriteJokes', []);
        const isFavorited = this.data.isFavorited;

        if (isFavorited) {
          // 取消收藏
          favoriteJokes = favoriteJokes.filter(item => item.id !== joke.id);
          util.showSuccess('已取消收藏');
        } else {
          // 添加收藏
          const favoriteJoke = {
            ...joke,
            favoriteTime: new Date().toISOString()
          };
          favoriteJokes.unshift(favoriteJoke);
          
          // 限制收藏数量
          if (favoriteJokes.length > 50) {
            favoriteJokes = favoriteJokes.slice(0, 50);
          }
          
          util.showSuccess('收藏成功');
        }

        // 保存到本地存储
        util.storage.set('favoriteJokes', favoriteJokes);
        
        // 更新状态
        this.setData({ isFavorited: !isFavorited });
        
        // 震动反馈
        util.vibrateShort('medium');

        // 触发收藏事件
        this.triggerEvent('favorite', {
          joke: joke,
          isFavorited: !isFavorited
        });

        // 如果有用户ID，同步到服务器
        const app = getApp();
        if (app.globalData.userInfo && app.globalData.userInfo.id) {
          try {
            await ApiClient.favoriteJoke(joke.id);
          } catch (error) {
            console.error('同步收藏状态失败:', error);
          }
        }

      } catch (error) {
        console.error('收藏操作失败:', error);
        util.showError('操作失败');
      }
    },

    // 分享笑话
    async onShare() {
      const joke = this.data.joke;
      if (!joke.content) return;

      this.setData({ isSharing: true });

      try {
        // 记录分享行为
        await this.recordShare();
        
        // 震动反馈
        util.vibrateShort('medium');
        
        // 触发分享事件
        this.triggerEvent('share', {
          joke: joke
        });

      } catch (error) {
        console.error('分享失败:', error);
        util.showError('分享失败');
      } finally {
        this.setData({ isSharing: false });
      }
    },

    // 记录分享
    async recordShare() {
      const joke = this.data.joke;
      const app = getApp();
      
      try {
        // 本地记录
        let shareCount = util.storage.get('shareCount', 0);
        shareCount++;
        util.storage.set('shareCount', shareCount);

        // 服务器记录
        const shareData = {
          joke_id: joke.id,
          share_to: 'wechat',
          device_info: JSON.stringify(util.getDeviceInfo())
        };

        if (app.globalData.userInfo && app.globalData.userInfo.id) {
          shareData.user_id = app.globalData.userInfo.id;
        }

        await ApiClient.recordShare(shareData);
        
      } catch (error) {
        console.error('记录分享失败:', error);
      }
    },

    // 格式化时间
    formatTime(time) {
      return util.getRelativeTime(time);
    },

    // 获取分类信息
    getCategoryInfo(category) {
      const constants = require('../../utils/constants.js');
      const categoryInfo = constants.JOKE_CATEGORIES.find(item => item.id === category);
      return categoryInfo || { name: category, icon: '😄', color: '#4A90E2' };
    }
  }
});