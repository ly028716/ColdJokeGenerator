// 测试工具函数

/**
 * 模拟微信API
 */
const mockWxAPI = {
  // 模拟存储API
  setStorageSync: (key, data) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(key, JSON.stringify(data));
    }
  },
  
  getStorageSync: (key) => {
    if (typeof window !== 'undefined') {
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : null;
    }
    return null;
  },
  
  removeStorageSync: (key) => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(key);
    }
  },
  
  clearStorageSync: () => {
    if (typeof window !== 'undefined') {
      localStorage.clear();
    }
  },
  
  // 模拟网络请求
  request: (options) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (options.url.includes('/api/')) {
          resolve({
            statusCode: 200,
            data: {
              code: 200,
              message: 'success',
              data: mockData[options.url] || {}
            }
          });
        } else {
          reject({
            statusCode: 404,
            errMsg: 'request:fail'
          });
        }
      }, 100);
    });
  },
  
  // 模拟显示提示
  showToast: (options) => {
    console.log('Toast:', options.title);
  },
  
  showModal: (options) => {
    console.log('Modal:', options.title, options.content);
    return Promise.resolve({ confirm: true });
  },
  
  // 模拟震动
  vibrateShort: (options) => {
    console.log('Vibrate:', options);
  },
  
  // 模拟系统信息
  getSystemInfoSync: () => ({
    platform: 'devtools',
    version: '8.0.5',
    SDKVersion: '2.19.4',
    windowWidth: 375,
    windowHeight: 667
  })
};

// 模拟数据
const mockData = {
  '/api/v1/jokes/generate': {
    id: 'joke_001',
    content: '为什么程序员喜欢用暗色主题？因为光亮会吸引bug！',
    category: 'tech',
    tags: ['程序员', '技术'],
    created_at: new Date().toISOString()
  },
  
  '/api/v1/jokes/': {
    items: [
      {
        id: 'joke_001',
        content: '为什么程序员喜欢用暗色主题？因为光亮会吸引bug！',
        category: 'tech',
        tags: ['程序员', '技术'],
        created_at: new Date().toISOString()
      },
      {
        id: 'joke_002',
        content: '医生对病人说："我有好消息和坏消息。"病人说："先说坏消息。"医生说："你只能活24小时了。"病人说："那好消息呢？"医生说："我昨天就想告诉你了。"',
        category: 'life',
        tags: ['医生', '生活'],
        created_at: new Date().toISOString()
      }
    ],
    total: 2,
    page: 1,
    size: 10
  }
};

/**
 * 创建测试页面实例
 */
function createPageInstance(pageConfig) {
  const page = {
    data: pageConfig.data || {},
    setData: function(newData) {
      Object.assign(this.data, newData);
    },
    ...pageConfig
  };
  
  // 模拟页面生命周期
  if (page.onLoad) {
    page.onLoad({});
  }
  
  return page;
}

/**
 * 创建组件实例
 */
function createComponentInstance(componentConfig) {
  const component = {
    data: componentConfig.data || {},
    properties: componentConfig.properties || {},
    setData: function(newData) {
      Object.assign(this.data, newData);
    },
    triggerEvent: function(eventName, detail) {
      console.log('Component event:', eventName, detail);
    },
    ...componentConfig
  };
  
  // 模拟组件生命周期
  if (component.lifetimes && component.lifetimes.attached) {
    component.lifetimes.attached.call(component);
  }
  
  return component;
}

/**
 * 模拟事件对象
 */
function createMockEvent(type, detail = {}, target = {}) {
  return {
    type,
    detail,
    target,
    currentTarget: target,
    timeStamp: Date.now()
  };
}

/**
 * 测试工具函数
 */
const testUtils = {
  // 等待异步操作
  wait: (ms = 100) => new Promise(resolve => setTimeout(resolve, ms)),
  
  // 模拟用户点击
  mockTap: (handler, data = {}) => {
    const event = createMockEvent('tap', {}, { dataset: data });
    return handler.call(this, event);
  },
  
  // 模拟用户输入
  mockInput: (handler, value) => {
    const event = createMockEvent('input', { value });
    return handler.call(this, event);
  },
  
  // 模拟选择器改变
  mockPickerChange: (handler, value) => {
    const event = createMockEvent('change', { value });
    return handler.call(this, event);
  },
  
  // 断言函数
  assert: {
    equal: (actual, expected, message) => {
      if (actual !== expected) {
        throw new Error(message || `Expected ${expected}, but got ${actual}`);
      }
    },
    
    deepEqual: (actual, expected, message) => {
      if (JSON.stringify(actual) !== JSON.stringify(expected)) {
        throw new Error(message || `Expected ${JSON.stringify(expected)}, but got ${JSON.stringify(actual)}`);
      }
    },
    
    truthy: (value, message) => {
      if (!value) {
        throw new Error(message || `Expected truthy value, but got ${value}`);
      }
    },
    
    falsy: (value, message) => {
      if (value) {
        throw new Error(message || `Expected falsy value, but got ${value}`);
      }
    }
  }
};

// 导出
module.exports = {
  mockWxAPI,
  mockData,
  createPageInstance,
  createComponentInstance,
  createMockEvent,
  testUtils
};