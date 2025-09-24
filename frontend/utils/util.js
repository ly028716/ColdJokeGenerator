// 工具函数库

/**
 * 格式化时间
 * @param {Date|string|number} date 时间
 * @param {string} format 格式化字符串
 * @returns {string} 格式化后的时间字符串
 */
function formatTime(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return '';
  
  const d = new Date(date);
  if (isNaN(d.getTime())) return '';

  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hour = String(d.getHours()).padStart(2, '0');
  const minute = String(d.getMinutes()).padStart(2, '0');
  const second = String(d.getSeconds()).padStart(2, '0');

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hour)
    .replace('mm', minute)
    .replace('ss', second);
}

/**
 * 获取相对时间
 * @param {Date|string|number} date 时间
 * @returns {string} 相对时间字符串
 */
function getRelativeTime(date) {
  if (!date) return '';
  
  const now = new Date();
  const target = new Date(date);
  const diff = now.getTime() - target.getTime();
  
  const minute = 60 * 1000;
  const hour = 60 * minute;
  const day = 24 * hour;
  const week = 7 * day;
  const month = 30 * day;
  
  if (diff < minute) {
    return '刚刚';
  } else if (diff < hour) {
    return Math.floor(diff / minute) + '分钟前';
  } else if (diff < day) {
    return Math.floor(diff / hour) + '小时前';
  } else if (diff < week) {
    return Math.floor(diff / day) + '天前';
  } else if (diff < month) {
    return Math.floor(diff / week) + '周前';
  } else {
    return formatTime(date, 'YYYY-MM-DD');
  }
}

/**
 * 防抖函数
 * @param {Function} func 要防抖的函数
 * @param {number} wait 等待时间
 * @returns {Function} 防抖后的函数
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * 节流函数
 * @param {Function} func 要节流的函数
 * @param {number} limit 时间间隔
 * @returns {Function} 节流后的函数
 */
function throttle(func, limit) {
  let inThrottle;
  return function executedFunction(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * 深拷贝对象
 * @param {any} obj 要拷贝的对象
 * @returns {any} 拷贝后的对象
 */
function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj.getTime());
  if (obj instanceof Array) return obj.map(item => deepClone(item));
  if (typeof obj === 'object') {
    const clonedObj = {};
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key]);
      }
    }
    return clonedObj;
  }
}

/**
 * 生成随机字符串
 * @param {number} length 字符串长度
 * @returns {string} 随机字符串
 */
function generateRandomString(length = 8) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * 验证手机号
 * @param {string} phone 手机号
 * @returns {boolean} 是否有效
 */
function validatePhone(phone) {
  const phoneRegex = /^1[3-9]\d{9}$/;
  return phoneRegex.test(phone);
}

/**
 * 验证邮箱
 * @param {string} email 邮箱
 * @returns {boolean} 是否有效
 */
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * 获取文件大小的可读格式
 * @param {number} bytes 字节数
 * @returns {string} 可读的文件大小
 */
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * 获取设备信息
 * @returns {Object} 设备信息
 */
function getDeviceInfo() {
  const systemInfo = wx.getSystemInfoSync();
  return {
    brand: systemInfo.brand,
    model: systemInfo.model,
    system: systemInfo.system,
    platform: systemInfo.platform,
    version: systemInfo.version,
    SDKVersion: systemInfo.SDKVersion,
    screenWidth: systemInfo.screenWidth,
    screenHeight: systemInfo.screenHeight,
    windowWidth: systemInfo.windowWidth,
    windowHeight: systemInfo.windowHeight,
    pixelRatio: systemInfo.pixelRatio,
    statusBarHeight: systemInfo.statusBarHeight,
    safeArea: systemInfo.safeArea
  };
}

/**
 * 显示成功提示
 * @param {string} title 提示内容
 * @param {number} duration 显示时长
 */
function showSuccess(title, duration = 2000) {
  wx.showToast({
    title: title,
    icon: 'success',
    duration: duration
  });
}

/**
 * 显示错误提示
 * @param {string} title 提示内容
 * @param {number} duration 显示时长
 */
function showError(title, duration = 2000) {
  wx.showToast({
    title: title,
    icon: 'none',
    duration: duration
  });
}

/**
 * 显示确认对话框
 * @param {string} content 对话框内容
 * @param {string} title 对话框标题
 * @returns {Promise<boolean>} 用户选择结果
 */
function showConfirm(content, title = '提示') {
  return new Promise((resolve) => {
    wx.showModal({
      title: title,
      content: content,
      success: (res) => {
        resolve(res.confirm);
      },
      fail: () => {
        resolve(false);
      }
    });
  });
}

/**
 * 复制文本到剪贴板
 * @param {string} text 要复制的文本
 * @returns {Promise<boolean>} 复制结果
 */
function copyToClipboard(text) {
  return new Promise((resolve) => {
    wx.setClipboardData({
      data: text,
      success: () => {
        showSuccess('复制成功');
        resolve(true);
      },
      fail: () => {
        showError('复制失败');
        resolve(false);
      }
    });
  });
}

/**
 * 保存图片到相册
 * @param {string} filePath 图片路径
 * @returns {Promise<boolean>} 保存结果
 */
function saveImageToPhotosAlbum(filePath) {
  return new Promise((resolve) => {
    wx.saveImageToPhotosAlbum({
      filePath: filePath,
      success: () => {
        showSuccess('保存成功');
        resolve(true);
      },
      fail: (err) => {
        if (err.errMsg.includes('auth deny')) {
          wx.showModal({
            title: '提示',
            content: '需要您授权保存相册',
            showCancel: false,
            confirmText: '去设置',
            success: () => {
              wx.openSetting();
            }
          });
        } else {
          showError('保存失败');
        }
        resolve(false);
      }
    });
  });
}

/**
 * 获取网络状态
 * @returns {Promise<Object>} 网络状态信息
 */
function getNetworkType() {
  return new Promise((resolve) => {
    wx.getNetworkType({
      success: (res) => {
        resolve({
          networkType: res.networkType,
          isConnected: res.networkType !== 'none'
        });
      },
      fail: () => {
        resolve({
          networkType: 'unknown',
          isConnected: false
        });
      }
    });
  });
}

/**
 * 震动反馈
 * @param {string} type 震动类型：light, medium, heavy
 */
function vibrateShort(type = 'light') {
  if (wx.canIUse('vibrateShort')) {
    wx.vibrateShort({
      type: type
    });
  }
}

/**
 * 本地存储操作
 */
const storage = {
  // 设置存储
  set(key, value) {
    try {
      wx.setStorageSync(key, value);
      return true;
    } catch (e) {
      console.error('存储失败:', e);
      return false;
    }
  },
  
  // 获取存储
  get(key, defaultValue = null) {
    try {
      const value = wx.getStorageSync(key);
      return value !== '' ? value : defaultValue;
    } catch (e) {
      console.error('读取存储失败:', e);
      return defaultValue;
    }
  },
  
  // 删除存储
  remove(key) {
    try {
      wx.removeStorageSync(key);
      return true;
    } catch (e) {
      console.error('删除存储失败:', e);
      return false;
    }
  },
  
  // 清空存储
  clear() {
    try {
      wx.clearStorageSync();
      return true;
    } catch (e) {
      console.error('清空存储失败:', e);
      return false;
    }
  }
};

module.exports = {
  formatTime,
  getRelativeTime,
  debounce,
  throttle,
  deepClone,
  generateRandomString,
  validatePhone,
  validateEmail,
  formatFileSize,
  getDeviceInfo,
  showSuccess,
  showError,
  showConfirm,
  copyToClipboard,
  saveImageToPhotosAlbum,
  getNetworkType,
  vibrateShort,
  storage
};