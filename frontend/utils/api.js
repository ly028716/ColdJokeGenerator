// API工具类
const app = getApp();

class ApiClient {
  // 基础请求方法
  static request(options) {
    return new Promise((resolve, reject) => {
      // 显示加载提示
      if (options.showLoading !== false) {
        wx.showLoading({
          title: options.loadingText || '请求中...',
          mask: true
        });
      }

      wx.request({
        url: app.globalData.apiUrl + options.url,
        method: options.method || 'GET',
        data: options.data || {},
        header: {
          'Content-Type': 'application/json',
          'X-Request-ID': this.generateRequestId(),
          ...options.header
        },
        timeout: options.timeout || 15000,
        success(res) {
          console.log('API请求成功:', options.url, res);
          
          // 隐藏加载提示
          if (options.showLoading !== false) {
            wx.hideLoading();
          }

          if (res.statusCode === 200) {
            if (res.data.code === 200) {
              resolve(res.data);
            } else {
              // 业务错误
              reject({
                type: 'business',
                code: res.data.code,
                message: res.data.message || '请求失败'
              });
            }
          } else {
            // HTTP错误
            reject({
              type: 'http',
              code: res.statusCode,
              message: `HTTP ${res.statusCode} 错误`
            });
          }
        },
        fail(err) {
          console.error('API请求失败:', options.url, err);
          
          // 隐藏加载提示
          if (options.showLoading !== false) {
            wx.hideLoading();
          }

          // 网络错误
          reject({
            type: 'network',
            code: -1,
            message: '网络连接失败，请检查网络设置'
          });
        }
      });
    });
  }

  // 生成请求ID
  static generateRequestId() {
    return 'req_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  // 处理API错误
  static handleError(error, showToast = true) {
    let message = '未知错误';
    
    switch (error.type) {
      case 'network':
        message = '网络连接失败，请检查网络设置';
        break;
      case 'http':
        message = `服务器错误 (${error.code})`;
        break;
      case 'business':
        message = error.message;
        break;
      default:
        message = error.message || '请求失败';
    }

    if (showToast) {
      wx.showToast({
        title: message,
        icon: 'none',
        duration: 2000
      });
    }

    return message;
  }

  // 生成冷笑话
  static generateJoke(params = {}) {
    return this.request({
      url: '/jokes/generate',
      method: 'POST',
      data: params,
      loadingText: '正在生成笑话...'
    });
  }

  // 批量生成笑话
  static generateBatchJokes(params = {}) {
    return this.request({
      url: '/jokes/batch',
      method: 'POST',
      data: params,
      loadingText: '正在批量生成...'
    });
  }

  // 按分类生成笑话
  static generateJokeByCategory(category, params = {}) {
    return this.request({
      url: `/jokes/category/${category}`,
      method: 'GET',
      data: params,
      loadingText: '正在生成笑话...'
    });
  }

  // 获取笑话列表
  static getJokeList(params = {}) {
    return this.request({
      url: '/jokes/',
      method: 'GET',
      data: params,
      showLoading: false
    });
  }

  // 获取单个笑话
  static getJoke(jokeId) {
    return this.request({
      url: `/jokes/${jokeId}`,
      method: 'GET',
      showLoading: false
    });
  }

  // 收藏笑话
  static favoriteJoke(jokeId) {
    return this.request({
      url: `/jokes/${jokeId}/favorite`,
      method: 'POST',
      loadingText: '收藏中...'
    });
  }

  // 获取用户历史
  static getUserHistory(userId, params = {}) {
    return this.request({
      url: `/jokes/user/${userId}/history`,
      method: 'GET',
      data: params,
      showLoading: false
    });
  }

  // 记录分享
  static recordShare(data) {
    return this.request({
      url: '/jokes/share',
      method: 'POST',
      data: data,
      showLoading: false
    });
  }

  // 获取分享统计
  static getShareStats(params = {}) {
    return this.request({
      url: '/jokes/share/stats',
      method: 'GET',
      data: params,
      showLoading: false
    });
  }

  // 创建用户
  static createUser(userData) {
    return this.request({
      url: '/users/',
      method: 'POST',
      data: userData,
      loadingText: '注册中...'
    });
  }

  // 获取用户信息
  static getUser(userId) {
    return this.request({
      url: `/users/${userId}`,
      method: 'GET',
      showLoading: false
    });
  }

  // 通过openid获取用户信息
  static getUserByOpenid(openid) {
    return this.request({
      url: `/users/openid/${openid}`,
      method: 'GET',
      showLoading: false
    });
  }

  // 更新用户信息
  static updateUser(userId, userData) {
    return this.request({
      url: `/users/${userId}`,
      method: 'PUT',
      data: userData,
      loadingText: '更新中...'
    });
  }

  // 用户登录
  static userLogin(userId) {
    return this.request({
      url: `/users/${userId}/login`,
      method: 'POST',
      showLoading: false
    });
  }

  // 获取用户统计
  static getUserStats() {
    return this.request({
      url: '/users/stats/overview',
      method: 'GET',
      showLoading: false
    });
  }

  // 健康检查
  static healthCheck() {
    return this.request({
      url: '/health',
      method: 'GET',
      showLoading: false,
      timeout: 8000
    });
  }

  // 测试API连接
  static testConnection() {
    return this.request({
      url: '/test',
      method: 'GET',
      showLoading: false,
      timeout: 8000
    });
  }
}

module.exports = ApiClient;