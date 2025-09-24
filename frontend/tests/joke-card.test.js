// 笑话卡片组件测试

const { createComponentInstance, testUtils, mockWxAPI } = require('./test-utils.js');

// 模拟全局wx对象
global.wx = mockWxAPI;

// 导入组件配置（实际项目中需要适配）
const jokeCardConfig = {
  properties: {
    joke: {
      type: Object,
      value: {}
    },
    showTime: {
      type: Boolean,
      value: false
    },
    timeField: {
      type: String,
      value: 'created_at'
    }
  },
  
  data: {
    isFavorited: false,
    isExpanded: false
  },
  
  methods: {
    onJokeTap() {
      this.triggerEvent('jokeclick', { joke: this.properties.joke });
    },
    
    onCopyTap() {
      // 模拟复制功能
      console.log('复制笑话:', this.properties.joke.content);
      this.triggerEvent('copy', { joke: this.properties.joke });
    },
    
    onFavoriteTap() {
      const isFavorited = !this.data.isFavorited;
      this.setData({ isFavorited });
      this.triggerEvent('favorite', { 
        joke: this.properties.joke, 
        isFavorited 
      });
    },
    
    onShareTap() {
      this.triggerEvent('share', { joke: this.properties.joke });
    },
    
    toggleExpand() {
      this.setData({
        isExpanded: !this.data.isExpanded
      });
    }
  }
};

// 测试用例
describe('JokeCard Component', () => {
  let component;
  const mockJoke = {
    id: 'joke_001',
    content: '为什么程序员喜欢用暗色主题？因为光亮会吸引bug！',
    category: 'tech',
    tags: ['程序员', '技术'],
    created_at: '2024-01-01T12:00:00Z'
  };
  
  beforeEach(() => {
    component = createComponentInstance(jokeCardConfig);
    component.properties.joke = mockJoke;
  });
  
  test('应该正确初始化组件', () => {
    testUtils.assert.equal(component.data.isFavorited, false);
    testUtils.assert.equal(component.data.isExpanded, false);
    testUtils.assert.deepEqual(component.properties.joke, mockJoke);
  });
  
  test('应该正确处理点击事件', () => {
    let eventTriggered = false;
    let eventDetail = null;
    
    // 模拟事件监听
    component.triggerEvent = (eventName, detail) => {
      if (eventName === 'jokeclick') {
        eventTriggered = true;
        eventDetail = detail;
      }
    };
    
    component.onJokeTap();
    
    testUtils.assert.truthy(eventTriggered);
    testUtils.assert.deepEqual(eventDetail.joke, mockJoke);
  });
  
  test('应该正确处理收藏功能', () => {
    let favoriteEventTriggered = false;
    let favoriteDetail = null;
    
    component.triggerEvent = (eventName, detail) => {
      if (eventName === 'favorite') {
        favoriteEventTriggered = true;
        favoriteDetail = detail;
      }
    };
    
    // 初始状态应该是未收藏
    testUtils.assert.equal(component.data.isFavorited, false);
    
    // 点击收藏
    component.onFavoriteTap();
    
    // 检查状态变化
    testUtils.assert.equal(component.data.isFavorited, true);
    testUtils.assert.truthy(favoriteEventTriggered);
    testUtils.assert.equal(favoriteDetail.isFavorited, true);
    testUtils.assert.deepEqual(favoriteDetail.joke, mockJoke);
  });
  
  test('应该正确处理展开/收起功能', () => {
    // 初始状态应该是收起的
    testUtils.assert.equal(component.data.isExpanded, false);
    
    // 点击展开
    component.toggleExpand();
    testUtils.assert.equal(component.data.isExpanded, true);
    
    // 再次点击收起
    component.toggleExpand();
    testUtils.assert.equal(component.data.isExpanded, false);
  });
  
  test('应该正确处理复制功能', () => {
    let copyEventTriggered = false;
    let copyDetail = null;
    
    component.triggerEvent = (eventName, detail) => {
      if (eventName === 'copy') {
        copyEventTriggered = true;
        copyDetail = detail;
      }
    };
    
    component.onCopyTap();
    
    testUtils.assert.truthy(copyEventTriggered);
    testUtils.assert.deepEqual(copyDetail.joke, mockJoke);
  });
  
  test('应该正确处理分享功能', () => {
    let shareEventTriggered = false;
    let shareDetail = null;
    
    component.triggerEvent = (eventName, detail) => {
      if (eventName === 'share') {
        shareEventTriggered = true;
        shareDetail = detail;
      }
    };
    
    component.onShareTap();
    
    testUtils.assert.truthy(shareEventTriggered);
    testUtils.assert.deepEqual(shareDetail.joke, mockJoke);
  });
});

// 简单的测试运行器
function describe(name, fn) {
  console.log(`\n=== ${name} ===`);
  fn();
}

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
  } catch (error) {
    console.error(`✗ ${name}: ${error.message}`);
  }
}

function beforeEach(fn) {
  // 在实际测试框架中，这会在每个测试前运行
  // 这里简化处理
}

// 运行测试
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { describe, test, beforeEach };
} else {
  // 浏览器环境下直接运行测试
  describe('JokeCard Component', () => {
    // 测试代码...
  });
}