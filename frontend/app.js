App({
  onLaunch() {
    // 小程序初始化时执行
    console.log('AI冷笑话生成器小程序启动');
    
    // 检查更新
    this.checkForUpdate();
    
    // 初始化用户信息
    this.initUserInfo();
    
    // 设置API基础URL
    this.setApiUrl();
  },

  onShow() {
    // 小程序显示时执行
    console.log('小程序显示');
  },

  onHide() {
    // 小程序隐藏时执行
    console.log('小程序隐藏');
  },

  // 检查小程序更新
  checkForUpdate() {
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager();
      
      updateManager.onCheckForUpdate((res) => {
        console.log('检查更新结果:', res.hasUpdate);
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
        wx.showToast({
          title: '更新失败',
          icon: 'none'
        });
      });
    }
  },

  // 初始化用户信息
  initUserInfo() {
    // 获取用户信息
    wx.getSetting({
      success: (res) => {
        if (res.authSetting['scope.userInfo']) {
          wx.getUserInfo({
            success: (res) => {
              this.globalData.userInfo = res.userInfo;
              console.log('用户信息:', res.userInfo);
            }
          });
        }
      }
    });
  },

  // 设置API基础URL
  setApiUrl() {
    // 根据环境设置不同的API地址
    const accountInfo = wx.getAccountInfoSync();
    if (accountInfo.miniProgram.envVersion === 'develop') {
      // 开发版
      this.globalData.apiUrl = "http://localhost:8000/api/v1";
    } else if (accountInfo.miniProgram.envVersion === 'trial') {
      // 体验版
      this.globalData.apiUrl = "https://test-api.example.com/api/v1";
    } else {
      // 正式版
      this.globalData.apiUrl = "https://api.example.com/api/v1";
    }
    console.log('API地址:', this.globalData.apiUrl);
  },

  // 显示网络错误提示
  showNetworkError() {
    wx.showToast({
      title: '网络连接失败',
      icon: 'none',
      duration: 2000
    });
  },

  // 显示加载提示
  showLoading(title = '加载中...') {
    wx.showLoading({
      title: title,
      mask: true
    });
  },

  // 隐藏加载提示
  hideLoading() {
    wx.hideLoading();
  },
  
  globalData: {
    userInfo: null,
    apiUrl: "",
    jokeHistory: [], // 笑话历史记录
    favoriteJokes: [], // 收藏的笑话
    userStats: {
      totalGenerated: 0,
      totalShared: 0
    }
  }
})