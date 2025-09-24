const ApiClient = require('../../utils/api.js');
const util = require('../../utils/util.js');
const constants = require('../../utils/constants.js');

Page({
  data: {
    // 用户信息
    userInfo: null,
    // 用户统计
    userStats: {
      totalGenerated: 0,
      totalViewed: 0,
      totalFavorited: 0,
      totalShared: 0,
      joinDays: 0,
      todayGenerated: 0
    },
    // 用户偏好设置
    preferences: {
      length: 'medium',
      temperature: 0.7,
      autoSave: true,
      vibration: true,
      darkMode: false,
      fontSize: 'medium'
    },
    // 功能菜单
    menuItems: [
      {
        id: 'history',
        icon: '📖',
        title: '浏览历史',
        path: '/pages/history/history?tab=0'
      },
      {
        id: 'favorites',
        icon: '❤️',
        title: '我的收藏',
        path: '/pages/history/history?tab=1'
      },
      {
        id: 'settings',
        icon: '⚙️',
        title: '偏好设置',
        action: 'showSettings'
      },
      {
        id: 'feedback',
        icon: '💬',
        title: '意见反馈',
        action: 'showFeedback'
      },
      {
        id: 'about',
        icon: 'ℹ️',
        title: '关于我们',
        action: 'showAbout'
      }
    ],
    // 显示设置面板
    showSettingsPanel: false,
    // 显示反馈面板
    showFeedbackPanel: false,
    // 显示关于面板
    showAboutPanel: false,
    // 反馈内容
    feedbackContent: '',
    // 反馈类型
    feedbackType: 'suggestion',
    feedbackTypes: [
      { value: 'suggestion', label: '功能建议' },
      { value: 'bug', label: '问题反馈' },
      { value: 'other', label: '其他' }
    ],
    // 应用信息
    appInfo: {
      version: '1.0.0',
      buildTime: '2024-01-01',
      developer: 'AI冷笑话团队'
    }
  },

  onLoad(options) {
    console.log('个人中心页面加载', options);
    this.initPage();
  },

  onShow() {
    console.log('个人中心页面显示');
    this.loadUserData();
  },

  onReady() {
    wx.setNavigationBarTitle({
      title: '个人中心'
    });
  },

  // 初始化页面
  initPage() {
    this.loadUserInfo();
    this.loadUserPreferences();
    this.loadUserData();
  },

  // 加载用户信息
  loadUserInfo() {
    // 获取微信用户信息
    const userInfo = util.storage.get(constants.STORAGE_KEYS.USER_INFO, null);
    this.setData({ userInfo });
  },

  // 获取用户信息授权
  getUserProfile() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        console.log('获取用户信息成功:', res.userInfo);
        this.setData({ userInfo: res.userInfo });
        util.storage.set(constants.STORAGE_KEYS.USER_INFO, res.userInfo);
        
        // 震动反馈
        util.vibrateShort('success');
        util.showSuccess('授权成功');
      },
      fail: (err) => {
        console.error('获取用户信息失败:', err);
        util.showError('授权失败');
      }
    });
  },

  // 加载用户偏好
  loadUserPreferences() {
    const preferences = util.storage.get(constants.STORAGE_KEYS.USER_PREFERENCES, constants.DEFAULT_PREFERENCES);
    this.setData({ preferences });
  },

  // 加载用户数据统计
  loadUserData() {
    try {
      // 加载历史记录，确保返回数组
      const historyList = util.storage.get(constants.STORAGE_KEYS.JOKE_HISTORY, []) || [];
      const favoriteList = util.storage.get(constants.STORAGE_KEYS.FAVORITE_JOKES, []) || [];
      const generatedList = util.storage.get(constants.STORAGE_KEYS.GENERATED_JOKES, []) || [];
      const sharedList = util.storage.get(constants.STORAGE_KEYS.SHARED_JOKES, []) || [];
      
      // 计算今日生成数量
      const today = new Date();
      const todayStr = util.formatTime(today, 'YYYY-MM-DD');
      const todayGenerated = generatedList.filter(item => {
        if (!item || !item.createTime) return false;
        const createDate = new Date(item.createTime);
        return util.formatTime(createDate, 'YYYY-MM-DD') === todayStr;
      }).length;
      
      // 计算加入天数
      const firstUseTime = util.storage.get(constants.STORAGE_KEYS.FIRST_USE_TIME, new Date().toISOString());
      const joinDays = Math.ceil((today - new Date(firstUseTime)) / (1000 * 60 * 60 * 24));
      
      const userStats = {
        totalGenerated: Array.isArray(generatedList) ? generatedList.length : 0,
        totalViewed: Array.isArray(historyList) ? historyList.length : 0,
        totalFavorited: Array.isArray(favoriteList) ? favoriteList.length : 0,
        totalShared: Array.isArray(sharedList) ? sharedList.length : 0,
        joinDays: Math.max(1, joinDays),
        todayGenerated
      };
      
      this.setData({ userStats });
      
    } catch (error) {
      console.error('加载用户数据失败:', error);
      // 设置默认统计数据
      this.setData({
        userStats: {
          totalGenerated: 0,
          totalViewed: 0,
          totalFavorited: 0,
          totalShared: 0,
          joinDays: 1,
          todayGenerated: 0
        }
      });
    }
  },

  // 菜单项点击
  onMenuItemTap(e) {
    const item = e.currentTarget.dataset.item;
    
    // 震动反馈
    util.vibrateShort('light');
    
    if (item.path) {
      // 跳转页面
      wx.navigateTo({
        url: item.path,
        fail: () => {
          wx.switchTab({ url: item.path });
        }
      });
    } else if (item.action) {
      // 执行动作
      this[item.action]();
    }
  },

  // 显示设置面板
  showSettings() {
    this.setData({ showSettingsPanel: true });
  },

  // 隐藏设置面板
  hideSettings() {
    this.setData({ showSettingsPanel: false });
  },

  // 偏好设置改变
  onPreferenceChange(e) {
    const { key, value } = e.currentTarget.dataset;
    const preferences = { ...this.data.preferences };
    preferences[key] = value;
    
    this.setData({ preferences });
    this.savePreferences();
    
    // 震动反馈
    if (preferences.vibration) {
      util.vibrateShort('light');
    }
  },

  // 长度设置改变
  onLengthChange(e) {
    const value = e.detail.value;
    const lengths = constants.JOKE_LENGTHS;
    const selectedLength = lengths[value];
    
    const preferences = { ...this.data.preferences };
    preferences.length = selectedLength.value;
    
    this.setData({ preferences });
    this.savePreferences();
  },

  // 温度设置改变
  onTemperatureChange(e) {
    const value = parseFloat(e.detail.value);
    const preferences = { ...this.data.preferences };
    preferences.temperature = value;
    
    this.setData({ preferences });
    this.savePreferences();
  },

  // 字体大小改变
  onFontSizeChange(e) {
    const value = e.detail.value;
    const fontSizes = constants.FONT_SIZES;
    const selectedSize = fontSizes[value];
    
    const preferences = { ...this.data.preferences };
    preferences.fontSize = selectedSize.value;
    
    this.setData({ preferences });
    this.savePreferences();
    
    // 应用字体大小到全局
    this.applyFontSize(selectedSize.value);
  },

  // 应用字体大小
  applyFontSize(fontSize) {
    const app = getApp();
    app.globalData.fontSize = fontSize;
    
    // 这里可以实现全局字体大小的应用逻辑
    console.log('应用字体大小:', fontSize);
  },

  // 保存偏好设置
  savePreferences() {
    util.storage.set(constants.STORAGE_KEYS.USER_PREFERENCES, this.data.preferences);
  },

  // 显示反馈面板
  showFeedback() {
    this.setData({ 
      showFeedbackPanel: true,
      feedbackContent: '',
      feedbackType: 'suggestion'
    });
  },

  // 隐藏反馈面板
  hideFeedback() {
    console.log('hideFeedback被调用');
    this.setData({ showFeedbackPanel: false });
  },

  // 反馈类型改变
  onFeedbackTypeChange(e) {
    const value = e.detail.value;
    const feedbackType = this.data.feedbackTypes[value].value;
    
    console.log('反馈类型改变:', {
      selectedIndex: value,
      selectedType: feedbackType,
      allTypes: this.data.feedbackTypes,
      showFeedbackPanelBefore: this.data.showFeedbackPanel
    });
    
    this.setData({ 
      feedbackType: feedbackType
    });
    
    console.log('setData后的状态:', {
      feedbackType: this.data.feedbackType,
      showFeedbackPanelAfter: this.data.showFeedbackPanel
    });
  },

  // 获取反馈类型标签
  getFeedbackTypeLabel(value) {
    const type = this.data.feedbackTypes.find(item => item.value === value);
    return type ? type.label : '';
  },

  // 反馈内容输入
  onFeedbackInput(e) {
    const content = e.detail.value;
    this.setData({ feedbackContent: content });
  },

  // 提交反馈
  async submitFeedback() {
    const { feedbackContent, feedbackType } = this.data;
    
    if (!feedbackContent.trim()) {
      util.showError('请输入反馈内容');
      return;
    }
    
    try {
      // 这里可以调用反馈API
      const feedbackData = {
        type: feedbackType,
        content: feedbackContent.trim(),
        userInfo: this.data.userInfo,
        deviceInfo: {
          platform: wx.getSystemInfoSync().platform,
          version: wx.getSystemInfoSync().version
        },
        timestamp: new Date().toISOString()
      };
      
      console.log('提交反馈:', feedbackData);
      
      // 保存到本地（实际应该发送到服务器）
      let feedbackList = util.storage.get(constants.STORAGE_KEYS.FEEDBACK_LIST, []);
      feedbackList.unshift(feedbackData);
      util.storage.set(constants.STORAGE_KEYS.FEEDBACK_LIST, feedbackList);
      
      this.hideFeedback();
      util.showSuccess('反馈提交成功，感谢您的建议！');
      
      // 震动反馈
      util.vibrateShort('success');
      
    } catch (error) {
      console.error('提交反馈失败:', error);
      util.showError('提交失败，请稍后重试');
    }
  },

  // 显示关于面板
  showAbout() {
    this.setData({ showAboutPanel: true });
  },

  // 隐藏关于面板
  hideAbout() {
    this.setData({ showAboutPanel: false });
  },

  // 清除缓存
  clearCache() {
    wx.showModal({
      title: '清除缓存',
      content: '确定要清除所有缓存数据吗？这将删除浏览历史、收藏等数据。',
      confirmColor: '#FF4444',
      success: (res) => {
        if (res.confirm) {
          this.performClearCache();
        }
      }
    });
  },

  // 执行清除缓存
  performClearCache() {
    try {
      // 保留用户信息和偏好设置
      const userInfo = this.data.userInfo;
      const preferences = this.data.preferences;
      const firstUseTime = util.storage.get(constants.STORAGE_KEYS.FIRST_USE_TIME);
      
      // 清除所有存储
      wx.clearStorageSync();
      
      // 恢复重要数据
      if (userInfo) {
        util.storage.set(constants.STORAGE_KEYS.USER_INFO, userInfo);
      }
      util.storage.set(constants.STORAGE_KEYS.USER_PREFERENCES, preferences);
      if (firstUseTime) {
        util.storage.set(constants.STORAGE_KEYS.FIRST_USE_TIME, firstUseTime);
      }
      
      // 重新加载数据
      this.loadUserData();
      
      util.showSuccess('缓存清除成功');
      
      // 震动反馈
      util.vibrateShort('success');
      
    } catch (error) {
      console.error('清除缓存失败:', error);
      util.showError('清除失败');
    }
  },

  // 检查更新
  checkUpdate() {
    const updateManager = wx.getUpdateManager();
    
    updateManager.onCheckForUpdate((res) => {
      console.log('检查更新结果:', res.hasUpdate);
      if (!res.hasUpdate) {
        util.showSuccess('当前已是最新版本');
      }
    });
    
    updateManager.onUpdateReady(() => {
      wx.showModal({
        title: '更新提示',
        content: '新版本已经准备好，是否重启应用？',
        success: (res) => {
          if (res.confirm) {
            updateManager.applyUpdate();
          }
        }
      });
    });
    
    updateManager.onUpdateFailed(() => {
      util.showError('更新失败，请稍后重试');
    });
  },

  // 联系客服
  contactService() {
    wx.showModal({
      title: '联系客服',
      content: '如需帮助，请通过意见反馈功能联系我们，我们会尽快回复。',
      showCancel: false,
      confirmText: '知道了'
    });
  },

  // 分享应用
  shareApp() {
    const stats = this.data.userStats;
    return {
      title: `我在AI冷笑话生成器已经看了${stats.totalViewed}个笑话，快来一起乐一乐！`,
      path: '/pages/index/index'
    };
  },

  // 分享配置
  onShareAppMessage() {
    return this.shareApp();
  },

  onShareTimeline() {
    const stats = this.data.userStats;
    return {
      title: `AI冷笑话生成器 - 已看过${stats.totalViewed}个笑话`
    };
  }
});