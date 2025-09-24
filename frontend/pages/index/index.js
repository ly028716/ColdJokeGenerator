const ApiClient = require('../../utils/api.js');
const util = require('../../utils/util.js');
const constants = require('../../utils/constants.js');

Page({
  data: {
    // 当前笑话
    currentJoke: null,
    // 加载状态
    isLoading: false,
    // 统计信息
    todayCount: 0,
    totalCount: 0,
    favoriteCount: 0,
    shareCount: 0,
    // 动画状态
    jokeAnimation: {},
    // 设置选项
    lengthValue: 1, // 0: 短, 1: 中等, 2: 长
    lengthLabels: ['短', '中等', '长'],
    categoryOptions: [
      { id: 'random', name: '随机' },
      ...constants.JOKE_CATEGORIES
    ],
    selectedCategoryIndex: 0
  },

  onLoad() {
    console.log('首页加载');
    this.initPage();
  },

  onShow() {
    console.log('首页显示');
    
    // 检查全局数据
    const app = getApp();
    console.log('onShow时的全局数据:', {
      selectedCategory: app.globalData.selectedCategory
    });
    
    this.updateStats();
    
    // 延迟检查分类信息，确保数据传递完成
    setTimeout(() => {
      this.checkSelectedCategory();
    }, 100);
  },

  onReady() {
    // 创建动画实例
    this.jokeAnimation = wx.createAnimation({
      duration: 300,
      timingFunction: 'ease-in-out'
    });
  },

  // 初始化页面
  async initPage() {
    try {
      // 加载用户偏好
      this.loadUserPreferences();
      
      // 更新统计信息
      this.updateStats();
      
      // 检查网络状态
      await this.checkNetworkStatus();
      
    } catch (error) {
      console.error('页面初始化失败:', error);
    }
  },

  // 加载用户偏好
  loadUserPreferences() {
    const preferences = util.storage.get(constants.STORAGE_KEYS.USER_PREFERENCES, {
      lengthValue: 1,
      selectedCategoryIndex: 0
    });
    this.setData({
      lengthValue: preferences.lengthValue || 1,
      selectedCategoryIndex: preferences.selectedCategoryIndex || 0
    });
  },

  // 更新统计信息
  updateStats() {
    const totalCount = util.storage.get(constants.STORAGE_KEYS.GENERATION_COUNT, 0);
    const today = new Date().toDateString();
    const todayKey = `generation_count_${today}`;
    const todayCount = util.storage.get(todayKey, 0);
    const favoriteCount = util.storage.get(constants.STORAGE_KEYS.FAVORITE_COUNT, 0);
    const shareCount = util.storage.get(constants.STORAGE_KEYS.SHARE_COUNT, 0);
    
    this.setData({
      totalCount,
      todayCount,
      favoriteCount,
      shareCount
    });
  },

  // 检查选中的分类
  checkSelectedCategory() {
    const app = getApp();
    console.log('checkSelectedCategory调用，全局数据:', {
      selectedCategory: app.globalData.selectedCategory,
      hasSelectedCategory: !!app.globalData.selectedCategory
    });
    
    if (app.globalData.selectedCategory) {
      const selectedCategory = app.globalData.selectedCategory;
      console.log('检测到选中分类:', selectedCategory);
      
      // 查找对应的分类索引
      const categoryIndex = this.data.categoryOptions.findIndex(
        option => option.id === selectedCategory.id
      );
      
      console.log('分类匹配查找:', {
        selectedCategoryId: selectedCategory.id,
        selectedCategoryName: selectedCategory.name,
        categoryOptions: this.data.categoryOptions,
        foundIndex: categoryIndex
      });
      
      if (categoryIndex >= 0) {
        // 更新选中的分类
        this.setData({
          selectedCategoryIndex: categoryIndex
        });
        
        // 保存用户偏好
        this.saveUserPreferences();
        
        console.log(`已切换到分类: ${selectedCategory.name}`);
      } else {
        // 如果没找到对应分类，添加到选项中
        const newCategoryOption = {
          id: selectedCategory.id,
          name: selectedCategory.name
        };
        
        const updatedOptions = [...this.data.categoryOptions, newCategoryOption];
        this.setData({
          categoryOptions: updatedOptions,
          selectedCategoryIndex: updatedOptions.length - 1
        });
        
        this.saveUserPreferences();
        console.log(`已添加新分类: ${selectedCategory.name}`);
      }
      
      // 清除全局数据，避免重复处理
      app.globalData.selectedCategory = null;
    }
  },

  // 检查网络状态
  async checkNetworkStatus() {
    try {
      // 先检查网络连接
      const networkInfo = await util.getNetworkType();
      if (!networkInfo.isConnected) {
        console.warn('网络连接异常');
        return false;
      }
      
      // 测试API连接
      try {
        await ApiClient.testConnection();
        console.log('API连接正常');
        return true;
      } catch (apiError) {
        console.warn('API连接测试失败，尝试健康检查:', apiError);
        try {
          await ApiClient.healthCheck();
          console.log('健康检查通过');
          return true;
        } catch (healthError) {
          console.warn('健康检查失败:', healthError);
          return false;
        }
      }
    } catch (error) {
      console.error('网络检查失败:', error);
      return false;
    }
  },

  // 生成冷笑话
  async generateJoke() {
    if (this.data.isLoading) return;

    // 震动反馈
    util.vibrateShort && util.vibrateShort('light');

    this.setData({
      isLoading: true
    });

    try {
      // 准备请求参数
      const category = this.data.categoryOptions[this.data.selectedCategoryIndex];
      const params = {
        category: category.id,
        length: this.data.lengthLabels[this.data.lengthValue],
        temperature: 0.7
      };

      // 调用API生成笑话
      const response = await ApiClient.generateJoke(params);
      const joke = response.data;

      // 添加标签
      joke.tags = [category.name, this.data.lengthLabels[this.data.lengthValue]];

      // 播放笑话出现动画
      this.playJokeAnimation();

      // 更新当前笑话
      this.setData({
        currentJoke: joke
      });

      // 保存到历史记录
      this.saveToHistory(joke);

      // 更新统计
      this.updateGenerationStats();

      // 震动反馈
      util.vibrateShort && util.vibrateShort('medium');

    } catch (error) {
      console.error('生成笑话失败:', error);
      
      // 显示备用笑话
      this.showFallbackJoke();
    } finally {
      this.setData({
        isLoading: false
      });
    }
  },

  // 播放笑话动画
  playJokeAnimation() {
    // 确保动画对象存在
    if (!this.jokeAnimation) {
      this.jokeAnimation = wx.createAnimation({
        duration: 300,
        timingFunction: 'ease-in-out'
      });
    }
    
    const animation = this.jokeAnimation;
    
    // 淡出
    animation.opacity(0).step();
    this.setData({
      jokeAnimation: animation.export()
    });

    // 延迟后淡入
    setTimeout(() => {
      animation.opacity(1).step();
      this.setData({
        jokeAnimation: animation.export()
      });
    }, 150);
  },

  // 显示备用笑话
  showFallbackJoke() {
    const fallbackJokes = [
      '为什么程序员喜欢冷笑话？因为它们像代码一样冷！',
      '有一天，一个程序员对他的妻子说："去超市买一斤苹果，如果有鸡蛋的话，买十个。"程序员回来了，手里拿着十斤苹果。妻子问："你怎么买了这么多苹果？"程序员："因为他们有鸡蛋。"',
      '为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 == Dec 25！'
    ];
    
    const randomJoke = fallbackJokes[Math.floor(Math.random() * fallbackJokes.length)];
    const fallbackJokeData = {
      id: Date.now(),
      content: randomJoke,
      category: 'programmer',
      tags: ['程序员', '中等'],
      created_at: new Date().toISOString(),
      is_fallback: true
    };

    this.setData({
      currentJoke: fallbackJokeData
    });

    this.saveToHistory(fallbackJokeData);
  },

  // 保存到历史记录
  saveToHistory(joke) {
    try {
      let history = util.storage.get(constants.STORAGE_KEYS.JOKE_HISTORY, []);
      console.log('保存历史记录前:', {
        storageKey: constants.STORAGE_KEYS.JOKE_HISTORY,
        currentHistoryLength: history ? history.length : 0,
        joke: joke
      });
      
      // 确保history是数组
      if (!Array.isArray(history)) {
        history = [];
      }
      
      // 添加到历史记录开头
      const historyItem = {
        ...joke,
        viewTime: new Date().toISOString()
      };
      
      history.unshift(historyItem);
      
      // 限制历史记录数量
      const maxCount = constants.PAGE_CONFIG?.MAX_HISTORY_COUNT || 100;
      if (history.length > maxCount) {
        history = history.slice(0, maxCount);
      }
      
      util.storage.set(constants.STORAGE_KEYS.JOKE_HISTORY, history);
      
      console.log('保存历史记录后:', {
        newHistoryLength: history.length,
        savedItem: historyItem
      });
      
    } catch (error) {
      console.error('保存历史记录失败:', error);
    }
  },

  // 更新生成统计
  updateGenerationStats() {
    // 总计数
    let totalCount = util.storage.get(constants.STORAGE_KEYS.GENERATION_COUNT, 0);
    totalCount++;
    util.storage.set(constants.STORAGE_KEYS.GENERATION_COUNT, totalCount);

    // 今日计数
    const today = new Date().toDateString();
    const todayKey = `generation_count_${today}`;
    let todayCount = util.storage.get(todayKey, 0);
    todayCount++;
    util.storage.set(todayKey, todayCount);

    this.setData({
      totalCount,
      todayCount
    });
  },

  // 长度改变
  onLengthChange(e) {
    const lengthValue = parseInt(e.detail.value);
    this.setData({ lengthValue });
    this.saveUserPreferences();
  },

  // 分类改变
  onCategoryChange(e) {
    const selectedCategoryIndex = parseInt(e.detail.value);
    this.setData({ selectedCategoryIndex });
    this.saveUserPreferences();
  },

  // 保存用户偏好
  saveUserPreferences() {
    const preferences = {
      lengthValue: this.data.lengthValue,
      selectedCategoryIndex: this.data.selectedCategoryIndex
    };
    
    util.storage.set(constants.STORAGE_KEYS.USER_PREFERENCES, preferences);
  },

  // 收藏笑话
  onJokeFavorite() {
    if (!this.data.currentJoke) return;
    
    const joke = this.data.currentJoke;
    let favorites = util.storage.get(constants.STORAGE_KEYS.FAVORITE_JOKES, []);
    
    console.log('收藏操作:', {
      joke: joke,
      currentFavorites: favorites,
      favoritesLength: favorites.length
    });
    
    // 检查是否已收藏
    const existIndex = favorites.findIndex(item => item.id === joke.id);
    
    if (existIndex >= 0) {
      // 取消收藏
      favorites.splice(existIndex, 1);
      wx.showToast({
        title: '已取消收藏',
        icon: 'none'
      });
      console.log('取消收藏后:', favorites);
    } else {
      // 添加收藏
      const favoriteJoke = {
        ...joke,
        favoriteTime: new Date().toISOString()
      };
      favorites.unshift(favoriteJoke);
      wx.showToast({
        title: '收藏成功',
        icon: 'success'
      });
      
      // 更新收藏统计
      let favoriteCount = util.storage.get(constants.STORAGE_KEYS.FAVORITE_COUNT, 0);
      favoriteCount++;
      util.storage.set(constants.STORAGE_KEYS.FAVORITE_COUNT, favoriteCount);
      this.setData({ favoriteCount });
      
      console.log('添加收藏后:', favorites);
    }
    
    util.storage.set(constants.STORAGE_KEYS.FAVORITE_JOKES, favorites);
  },

  // 分享笑话
  onJokeShare() {
    if (!this.data.currentJoke) return;
    
    const joke = this.data.currentJoke;
    
    // 复制到剪贴板
    wx.setClipboardData({
      data: joke.content,
      success: () => {
        wx.showToast({
          title: '已复制到剪贴板',
          icon: 'success'
        });
        
        // 更新分享统计
        let shareCount = util.storage.get(constants.STORAGE_KEYS.SHARE_COUNT, 0);
        shareCount++;
        util.storage.set(constants.STORAGE_KEYS.SHARE_COUNT, shareCount);
        this.setData({ shareCount });
      }
    });
  },

  // 下拉刷新
  async onPullDownRefresh() {
    try {
      await this.checkNetworkStatus();
      this.loadRecentJokes();
      this.updateStats();
    } catch (error) {
      console.error('刷新失败:', error);
    } finally {
      wx.stopPullDownRefresh();
    }
  },

  // 分享配置
  onShareAppMessage() {
    const joke = this.data.currentJoke;
    if (joke && joke.content) {
      return {
        title: joke.content,
        path: '/pages/index/index',
        imageUrl: '' // 可以设置分享图片
      };
    }
    return {
      title: 'AI冷笑话生成器 - 让生活更有趣',
      path: '/pages/index/index'
    };
  },

  onShareTimeline() {
    const joke = this.data.currentJoke;
    if (joke && joke.content) {
      return {
        title: joke.content,
        query: '',
        imageUrl: ''
      };
    }
    return {
      title: 'AI冷笑话生成器 - 让生活更有趣'
    };
  }
});